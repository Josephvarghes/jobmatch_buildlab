import fitz 
import docx 
from fastapi import UploadFile 

async def parse_resume_text(file: UploadFile) -> str: 
      """Extract text from PDF or DOCX resume""" 
      content = await file.read() 
      filename = file.filename.lower() 

      if filename.endswith(".pdf"): 
            return extract_pdf_text(content) 
      elif filename.endswith(".docx"): 
            return extract_docx_text(content) 
      else: 
            raise ValueError("Unsupported file type. Please upload PDF or DOCX") 
    
def extract_pdf_text(file_bytes: bytes) -> str: 
      text ="" 
      pdf = fitz.open(stream=file_bytes, filetype="pdf") 
      for page in pdf: 
            text += page.get_text() 
      pdf.close() 
      return text.strip() 

def extract_docx_text(file_bytes: bytes) -> str: 
      text ="" 
      from io import BytesIO 
      doc = docx.Document(BytesIO(file_bytes)) 
      for para in doc.paragraphs: 
            text += para.text +"\n" 
      return text.strip() 

