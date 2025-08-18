import pdfplumber
import json 
import re
import os  

#predefined list of common technical & soft skills 
SKILLS_LIST = [
    "Python", "Java", "C++", "C#", "JavaScript", "SQL", "HTML", "CSS",
    "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Machine Learning",
    "Deep Learning", "Data Analysis", "NLP", "TensorFlow", "PyTorch",
    "Communication", "Leadership", "Teamwork", "Problem Solving",
    "Time Management", "Creativity", "Critical Thinking"
] 

#for extract skills form resume

def extract_resume_skills(pdf_path): 
    """
    Extract text from a PDF resume and identify skills. 

    args:
        pdf_path(str): Path to the PDF file. 

    Returns: 
        dict: Contains extracted text and list of identified skills. 


    """
    extracted_text =""
    if not os.path.exists(pdf_path): 
        raise FileNotFoundError(f"File not found: {pdf_path}") 
    
    #Use pdfplumber for reliable text extraction  
    with pdfplumber.open(pdf_path) as pdf: 
        for page in pdf.pages: 
            page_text = page.extract_text() or "" 
            extracted_text += page_text + " " 

    
    #Clean text: remove excessive whitespace & newlines 
    clean_text = re.sub(r'\s+', ' ', extracted_text).strip() 

    #case-insensitive skill matching 
    found_skills = set() 
    for skill in SKILLS_LIST: 
        if re.search(r'\b' + re.escape(skill) + r'\b', clean_text, flags=re.IGNORECASE): 
            found_skills.add(skill) 

    #prepare result 
    result = {
        "extracted_text":clean_text, 
        "skills":sorted(found_skills) #sorted for consistency

    }

    return result 

if __name__ == "__main__": 
    #Example usage 
    resume_path = "JOSEPH VARGHESE - Resume.pdf" 

    try:
        data = extract_resume_skills(resume_path) 
        #print JSON-formatted output 
        print(json.dumps(data, indent=4)) 
    except Exception as e: 
        print(f"Error:{e}")
