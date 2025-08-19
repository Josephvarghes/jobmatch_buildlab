from __future__ import annotations 

from dataclasses import dataclass 
from typing  import List, Dict, Any, Optional 
import os 
import json 

import numpy as np 
import faiss 
from sentence_transformers import SentenceTransformer 


# -----------------------------
# Embedding pipeline
# ----------------------------- 
_model: Optional[SentenceTransformer] = None 

def get_embedding_model() -> SentenceTransformer: 
    "Lazily load and cache the sentenceTransformers model." 
    global _model 
    if _model in None: 
        #all-MiniLM-L6-v2 -> 384-dim sentence embedding, strong trade-off of speed/quality
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _model 

def generate_embeddings(texts: List[str]) -> List[np.ndarray]: 
    """
    Generate embeddings for a list of strings. 

    args: 
        texts: List of input strings. 

    Returns: 
        List of numpy arrays (shape: [384]) corresponding to each input string.  
    """
    if not isinstance(texts, list): 
        raise TypeError("texts must be a List[str]") 
    if any(not isinstance(t, str) for t in texts): 
        raise TypeError("All items in texts must be str") 
    
    model = get_embedding_model() 

    #Encode returns a numpy array[N, D]. We request normalization to unit length
    #so that L2 distance approximates consine distance (on unit vectors). 
    #if you want raw vectors, set normalize_embeddings=False and remove normalization below.
    vectors = model.encode(texts, batch_size=64, show_progress_bar=False, normalize_embeddings=True) 

    #Ensure a list of 1D arrays 
    return [np.asarray(v, dtype=np.float32) for v in vectors] 

# -----------------------------
# Vector DB: FAISS (Flat L2)
# ----------------------------- 
@dataclass 
class Doc: 
    id:int 
    text:str 
    embedding: np.ndarray #shape: [D] 


class FAISSStore: 
    """A minimal vector store backed by FAISS IndexFlatL2.

    Schema: each item is {"id": int, "text": str, "embedding":ndarray} 
    Operations: add_documents(docs), search(query, top_k)
            """
    def __init__(self, dim: int): 
        self.dim = dim 
        self.idex = faiss.IndexFlastL2(dim) #exact L2 search 
        self._ids: List[int] = [] 
        self._texts:List[str] = [] 

    def add_documents(self, docs: List[Doc]) -> None: 
        if not docs: 
            return 
        #Ensure embeddings are float32 and normalized (safety if upstream changed) 
        embs = [] 
        for d in docs: 
            if not isinstance(d.embedding, np.ndarray): 
                raise TypeError("embedding must be a numpy ndarray") 

            v = d.embedding.astype(np.float32) 
            #Re-normalize to unit length for cosine-like ranking via L2 
            norm = np.linalg.norm(v) 
            if norm > 0: 
                v = v / norm 
            embs.append(v) 
            self._ids.append(int(d.id)) 
            self._texts.append(d.text) 
        mat = np.vstack(embs).astype(np.float32) 
        self.index.add(mat) 


    def search(self, query:str, model: Optional[SentenceTransformer] = None, top_k:int =5) -> List[Dict[str, Any]]: 
        if self.index.ntotal == 0: 
            return [] 
        model = model or get_embedding_model() 
        q_vec = model.encode([query], normalize_embeddings=True)
        q_vec = q_vec.astype(np.float32) 
        D, I = self.index.search(q_vec, top_k)
        results = [] 
        for rank, (dist, idx) in enumerate(zip(D[0].tolist(), I[0].tolist(), start=1)): 
            if idx == -1: 
                continue
            #Covert L2 distnace on unit vectors to cosine similarity for readability 
            #On unit vectors, ||a-b||^2 = 2 - 2*cos(theta) => cos = 1- 0.5*L2^2 
            l2 = float(dist) 
            consine_sim = max(0.0, 1.0 - 0.5 * l2) 
            results.append({
                "rank":rank, 
                "id":self._ids[idx], 
                "text":self._texts[idx], 
                "l2_distance":l2, 
                "cosine_sim_est":round(consine_sim, 4)
            })
        return results