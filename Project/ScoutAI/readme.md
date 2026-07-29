# SmartScout

> **AI-Powered Job Discovery & Career Intelligence Platform**

SmartScout is an AI-powered job discovery platform that automatically finds jobs across the web, analyses how well they match your resume using LLMs, identifies skill gaps, generates personalised learning roadmaps, and provides actionable career insights through an interactive dashboard.

---

## Features

### AI Resume Analysis

- Upload PDF resumes
- Extract skills, education, projects and experience
- ATS-style resume parsing
- Resume summarisation

### Intelligent Job Discovery

- Google Custom Search integration
- Automatic job scraping
- Duplicate job removal
- Company metadata extraction
- Structured job information

### AI Job Matching

- Overall match score
- Skill match analysis
- Experience match analysis
- Project relevance
- Education relevance
- Missing skills detection
- Priority recommendation
- AI-generated explanation

### Career Intelligence

- Personalised learning roadmap
- Interview question generation
- Company summaries
- Career insights
- Job recommendations

### Analytics Dashboard

- Total jobs discovered
- Average match score
- High priority jobs
- Top hiring companies
- Most demanded skills
- Missing skills analysis
- Remote vs onsite distribution
- Match score distribution
- Experience level distribution

---

## Tech Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite

### AI

- Groq API
- Llama 3.3 70B

### Web Scraping

- Requests
- BeautifulSoup
- Trafilatura
- Readability-LXML

### Resume Parsing

- PDFPlumber

### Frontend

- HTML
- CSS
- JavaScript
- Chart.js

---

## Project Structure

```
SmartScout/
│
├── app.py
├── config.py
├── database.py
├── scraper.py
├── ai_engine.py
├── analytics.py
├── utils.py
├── prompts.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── data/
│   ├── cache/
│   ├── resumes/
│   └── jobs.db
│
├── .env
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/yourusername/SmartScout.git

cd SmartScout
```

Create a virtual environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key

GROQ_MODEL=llama-3.3-70b-versatile

GOOGLE_API_KEY=your_google_api_key

GOOGLE_CSE_ID=your_custom_search_engine_id

DATABASE_URL=sqlite:///data/jobs.db
```

---

## Running the Project

Start the FastAPI server

```bash
uvicorn app:app --reload
```

Open the frontend

```
frontend/index.html
```

or

```
http://127.0.0.1:8000
```

if the frontend is served through FastAPI.

---

## Workflow

```
                 Resume Upload
                       │
                       ▼
               Resume Parser (AI)
                       │
                       ▼
               Structured Resume
                       │
                       ▼
         Google Custom Search API
                       │
                       ▼
               Job Web Scraper
                       │
                       ▼
              Structured Job Data
                       │
                       ▼
            LLM Job Match Analysis
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
   Skill Gaps     Match Score    Recommendations
        │
        ▼
 Learning Roadmap
        │
        ▼
 Analytics Dashboard
```

---

## API Endpoints

### Upload Resume

```
POST /upload_resume
```

Uploads and parses a PDF resume.

---

### Search Jobs

```
POST /search_jobs
```

Searches, scrapes and analyses jobs.

---

### Dashboard

```
GET /dashboard
```

Returns dashboard analytics.

---

## Example Response

```json
{
    "overall_score": 91,
    "priority": "High",
    "strengths": [
        "Python",
        "FastAPI",
        "SQL",
        "Docker"
    ],
    "missing_skills": [
        "Kubernetes",
        "AWS"
    ],
    "explanation": "Excellent overall match with minor cloud skill gaps."
}
```

---

## Future Improvements

- LinkedIn integration
- Indeed integration
- Glassdoor integration
- Salary prediction
- Cover letter generation
- Resume optimisation
- Email application automation
- Multi-agent workflow
- LangGraph integration
- Playwright support
- Semantic job search
- Vector database
- RAG-powered company research
- React frontend
- Authentication
- Docker deployment
- Cloud deployment

---

## Skills Demonstrated

- FastAPI
- REST API Development
- Prompt Engineering
- LLM Integration
- Groq API
- Resume Parsing
- Information Extraction
- Web Scraping
- SQLAlchemy
- SQLite
- Python
- JSON Processing
- Dashboard Analytics
- Data Cleaning
- AI-powered Recommendation Systems

---

## License

This project is licensed under the MIT License.

---

## Author

**Vimal Barik**

AI Engineer | Machine Learning | Generative AI | LLM Applications

---

## Acknowledgements

- Groq
- FastAPI
- SQLAlchemy
- Chart.js
- BeautifulSoup
- Trafilatura
- PDFPlumber
- Open Source Community
