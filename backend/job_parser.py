import requests 
from bs4 import BeautifulSoup 
import re 
import json 
from fake_useragent import UserAgent

def parse_indeed_job(url): 
    # ua = UserAgent() 
    # headers = {"User-Agent": ua.random} 
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
}
    response = requests.get(url, headers=headers) 

    if response.status_code != 200: 
        raise Exception(f"Failed to fetch page: {response.status_code}") 
    
    soup = BeautifulSoup(response.text, "lxml") 

    #Extract Job Title 
    title_tag = soup.find("h2", class_="jobsearch-JobInfoHeader-title") 
    title = title_tag.get_text(strip=True) if title_tag else None 

    #Extract company name 
    company_tag = soup.find("a", href = lambda href: href and "/cmp/" in href) 
    company = company_tag.get_text(strip=True) if company_tag else None 

    #Extract location 
    location_tag = soup.find("div", {"data-testid": "inlineHeader-companyLocation"}) 
    location = location_tag.get_text(strip=True) if location_tag else None 

    #Extract job description 
    desc_tag = soup.find("div", id="jobDescriptionText") 
    description = desc_tag.get_text(separator=" ", strip=True) if desc_tag else None 

    #Extract skills(simple keyword matching) 
    predefined_skills = ["Python", "Java", "SQL", "JavaScript", "C++", "HTML", "CSS", "React", "Node.js", "Django"] 
    skills_found = [skill for skill in predefined_skills if re.search(rf"\b{skill}\b", description, re.IGNORECASE)] 

    #Responsibilities (split by bullet points) 
    responsibilities = [] 
    if desc_tag: 
        bullet_points = desc_tag.find_all("li") 
        responsibilities = [li.get_text(strip=True) for li in bullet_points] 
    #map responsibilities to job data
    job_data = {
        "title":title,
        "company":company, 
        "location":location,
        "skills":skills_found, 
        "responsibilities":responsibilities
    } 

    return job_data 

if __name__ == "__main__": 
    job_url = "https://in.indeed.com/?advn=7831672186689475&vjk=e6c2a7ff58de9383" 
    data = parse_indeed_job(job_url)
    print(json.dumps(data,indent=2)) 


