# JobMatch BuildLab

**AI-powered micro-project generator for job seekers.**  
Generates tailored, executable mini-projects based on a specific job posting and candidate skills using **RAG**, **context engineering**, and a **vector database**.

---

## 🚀 Overview
JobMatch BuildLab helps candidates stand out by:
- Parsing a job posting and your resume.
- Retrieving relevant company and tech context.
- Generating a role-specific micro-project brief.
- Providing starter code, README, and evaluation tests.
- Delivering a similarity score to ensure alignment with the job.

---

## ✨ Features
- **Job Posting Parser** – Extracts key requirements from a given URL.
- **Resume Skill Extractor** – Reads your PDF resume and detects core skills.
- **Vector DB Search** – Finds relevant docs and code snippets.
- **Context-Engineered Prompts** – Ensures accurate, grounded project generation.
- **Auto-Evaluation** – Runs tests and semantic scoring.
- **Downloadable Starter Repo** – Get all project files in one click.

---

## 🛠 Tech Stack
| Component       | Technology |
|-----------------|------------|
| Frontend        | Streamlit  |
| Backend         | FastAPI    |
| AI Model        | OpenAI GPT-4o-mini |
| Embeddings      | SentenceTransformers (all-MiniLM-L6-v2) |
| Vector Database | Chroma     |
| Parsing         | BeautifulSoup, pdfplumber |
| Deployment      | Render (backend), Vercel (frontend) |

---

## 📂 Project Structure (Initial)
