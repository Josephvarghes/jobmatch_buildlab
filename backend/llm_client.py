import os 
import requests 
from dotenv import load_dotenv 

#Load API Key from .env file 
load_dotenv () 
HF_API_KEY = os.getenv("HF_API_KEY") 

if not HF_API_KEY: 
    raise ValueError("❌Hugging Face API Key not found. Please set HF_API_KEY in .env") 

HF_API_KEY = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2" 

def query_huggingface(prompt: str, max_new_tokens:int = 512) -> str: 
    """ 
    Send a prompt 

    """