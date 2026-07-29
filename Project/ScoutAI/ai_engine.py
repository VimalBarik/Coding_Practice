"""
SmartScout AI Engine
--------------------
Handles all AI functionality:

- Resume Parsing
- Job Analysis
- Job Matching
- Skill Extraction
- Learning Roadmap
- Interview Questions
- Company Summary
"""

import json

from io import BytesIO

import pdfplumber

from groq import Groq

from config import settings
from prompts import PROMPTS


# ===========================================================
# Initialise Groq
# ===========================================================

client = Groq(
    api_key=settings.GROQ_API_KEY
)

MODEL = settings.GROQ_MODEL

# NOTE: prompts.py holds the single source of truth for all prompt
# templates now. This file used to define its own smaller PROMPTS
# dict with the same keys, which meant prompts.py was never actually
# used and features like richer resume fields (projects,
# certifications, languages) and job_extraction were dead code.


# ===========================================================
# Helper
# ===========================================================

def render_prompt(template, **kwargs):
    """
    Fills {placeholder} values into a prompt template using plain
    text substitution instead of str.format(). The templates in
    prompts.py embed literal JSON schema examples full of { } chars,
    which str.format() misreads as its own field syntax and raises
    KeyError on every call - silently swallowed by ask_llm's broad
    except, so every AI feature was returning {} on every request.
    """

    rendered = template

    for key, value in kwargs.items():

        rendered = rendered.replace("{" + key + "}", str(value))

    return rendered


def clean_json(text):
    """
    Removes markdown formatting from LLM responses.
    """

    text = text.replace("```json", "")
    text = text.replace("```", "")

    return text.strip()


# ===========================================================
# LLM
# ===========================================================

def ask_llm(prompt):
    """
    Generic helper for all Groq requests.
    """

    try:

        response = client.chat.completions.create(

            model=MODEL,

            messages=[

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0.2

        )

        answer = response.choices[0].message.content

        answer = clean_json(answer)

        return json.loads(answer)

    except Exception as e:

        print(e)

        return {}


# ===========================================================
# ===========================================================
# Resume Extraction
# ===========================================================

import zipfile
import xml.etree.ElementTree as ET
import re

def extract_resume_text(resume_bytes, filename="resume.pdf"):
    """
    Reads PDF, DOCX, or TXT content.
    """
    text = ""
    ext = (filename or "").rsplit(".", 1)[-1].lower()

    if ext == "docx":
        try:
            with zipfile.ZipFile(BytesIO(resume_bytes)) as z:
                xml_content = z.read("word/document.xml")
                tree = ET.fromstring(xml_content)
                texts = [node.text for node in tree.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t") if node.text]
                return "\n".join(texts)
        except Exception as e:
            print(f"DOCX extraction error: {e}")

    if ext in ["txt", "md"]:
        try:
            return resume_bytes.decode("utf-8", errors="ignore")
        except Exception:
            pass

    # PDF extraction using pdfplumber
    try:
        pdf = pdfplumber.open(BytesIO(resume_bytes))
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        pdf.close()
    except Exception as e:
        print(f"pdfplumber extraction error: {e}")

    # Regex string extraction fallback if pdfplumber returns empty or errors
    if not text.strip():
        try:
            text = " ".join(re.findall(r"[a-zA-Z0-9@._\-\s]{4,}", resume_bytes.decode("latin1", errors="ignore")))
        except Exception:
            pass

    return text.strip()


# ===========================================================
# Resume Parsing
# ===========================================================

def parse_resume(
    resume_bytes,
    filename="resume.pdf"
):
    """
    Extract structured resume via LLM.
    """

    text = extract_resume_text(resume_bytes, filename=filename)

    if not text or len(text) < 5:
        text = f"Candidate Resume ({filename})"

    prompt = render_prompt(PROMPTS["resume"], 
        resume=text
    )

    parsed = ask_llm(prompt)

    if not isinstance(parsed, dict):
        parsed = {
            "name": filename.rsplit(".", 1)[0].replace("_", " ").replace("-", " ").title(),
            "skills": ["Python", "Problem Solving"],
            "summary": "Extracted candidate profile."
        }

    parsed["filename"] = filename
    parsed["raw_text"] = text

    return parsed



# ===========================================================
# Job Extraction
# ===========================================================

def extract_job_details(job_description):
    """
    Uses the LLM to pull structured fields (company, location,
    salary, required_skills, etc.) out of raw scraped job text.
    Used by scraper.py, which previously left these fields empty.
    """

    if not job_description:
        return {}

    prompt = render_prompt(PROMPTS["job_extraction"], 
        job=job_description
    )

    return ask_llm(prompt)


# ===========================================================
# Resume Skills
# ===========================================================

def extract_resume_skills(resume):
    """
    Returns resume skills.
    """

    if isinstance(resume, dict):

        return resume.get(
            "skills",
            []
        )

    return []


# ===========================================================
# Pretty Printer
# ===========================================================

def pretty_resume(resume):

    print("\nResume\n")

    print("Name:", resume.get("name"))

    print("Email:", resume.get("email"))

    print("Phone:", resume.get("phone"))

    print()

    print("Skills")

    for skill in resume.get(
        "skills",
        []
    ):

        print("-", skill)


# ===========================================================
# Skill Matching
# ===========================================================

def basic_skill_match(
    resume_skills,
    job_skills
):
    """
    Basic percentage matching.

    Used before AI analysis.
    """

    if not resume_skills:

        return 0

    resume_set = {

        skill.lower()

        for skill in resume_skills

    }

    job_set = {

        skill.lower()

        for skill in job_skills

    }

    matched = resume_set.intersection(
        job_set
    )

    score = (

        len(matched)

        /

        len(job_set)

    ) * 100 if job_set else 0

    return round(score, 2)


# ===========================================================
# Missing Skills
# ===========================================================

def find_missing_skills(
    resume_skills,
    job_skills
):

    resume_set = {

        skill.lower()

        for skill in resume_skills

    }

    missing = []

    for skill in job_skills:

        if skill.lower() not in resume_set:

            missing.append(skill)

    return missing


# ===========================================================
# Utility
# ===========================================================

def resume_to_text(resume):
    """
    Converts parsed resume into
    readable text for prompts.
    """

    text = ""

    text += f"Name: {resume.get('name')}\n"

    text += f"Summary: {resume.get('summary')}\n\n"

    text += "Skills\n"

    for skill in resume.get(

        "skills",

        []

    ):

        text += f"- {skill}\n"

    text += "\nExperience\n"

    for exp in resume.get(

        "experience",

        []

    ):

        text += f"- {exp}\n"

    return text


def analyse_job(resume, job):
    if isinstance(resume, dict):
        resume = resume_to_text(resume)

    if isinstance(job, dict):
        job = json.dumps(job, indent=2)

    prompt = render_prompt(PROMPTS["job_analysis"], 
        resume=resume,
        job=job
    )

    result = ask_llm(prompt)

    if not result:
        return {
            "overall_score": 0,
            "skill_match": 0,
            "experience_match": 0,
            "missing_skills": [],
            "strengths": [],
            "priority": "Low",
            "explanation": "Analysis failed."
        }

    return result


def analyse_jobs(resume, jobs):
    analysed = []

    if isinstance(resume, dict):
        resume_skills = resume.get("skills", [])
    else:
        resume_skills = []

    for job in jobs:

        result = analyse_job(resume, job)

        job_skills = (
            job.get("required_skills", [])
            if isinstance(job, dict)
            else []
        )

        result["basic_score"] = basic_skill_match(
            resume_skills,
            job_skills
        )

        analysed.append({

            "job": job,

            "analysis": result

        })

    return analysed


def rank_jobs(analysed_jobs):

    return sorted(

        analysed_jobs,

        key=lambda x: (

            x["analysis"].get("overall_score", 0),

            x["analysis"].get("skill_match", 0),

            x["analysis"].get("experience_match", 0),

            x["analysis"].get("basic_score", 0),

        ),

        reverse=True

    )


def top_jobs(analysed_jobs, n=10):

    ranked = rank_jobs(analysed_jobs)

    return ranked[:n]


def filter_jobs(
    analysed_jobs,
    minimum_score=70
):

    filtered = []

    for job in analysed_jobs:

        score = job["analysis"].get(
            "overall_score",
            0
        )

        if score >= minimum_score:

            filtered.append(job)

    return filtered


def search_jobs_by_skill(
    analysed_jobs,
    skill
):

    results = []

    skill = skill.lower()

    for item in analysed_jobs:

        job = item["job"]

        skills = job.get(
            "required_skills",
            []
        )

        skills = [

            s.lower()

            for s in skills

        ]

        if skill in skills:

            results.append(item)

    return results


def search_jobs_by_company(
    analysed_jobs,
    company
):

    results = []

    company = company.lower()

    for item in analysed_jobs:

        job = item["job"]

        if job.get(
            "company",
            ""
        ).lower() == company:

            results.append(item)

    return results


def search_jobs_by_location(
    analysed_jobs,
    location
):

    results = []

    location = location.lower()

    for item in analysed_jobs:

        job = item["job"]

        if location in job.get(
            "location",
            ""
        ).lower():

            results.append(item)

    return results


def high_priority_jobs(analysed_jobs):

    results = []

    for item in analysed_jobs:

        if item["analysis"].get(
            "priority",
            ""
        ).lower() == "high":

            results.append(item)

    return results


def generate_explanation(result):

    explanation = []

    score = result.get(
        "overall_score",
        0
    )

    explanation.append(
        f"Overall Match: {score}%"
    )

    strengths = result.get(
        "strengths",
        []
    )

    if strengths:

        explanation.append("Strengths:")

        for s in strengths:

            explanation.append(
                f"✓ {s}"
            )

    missing = result.get(
        "missing_skills",
        []
    )

    if missing:

        explanation.append("Missing Skills:")

        for s in missing:

            explanation.append(
                f"✗ {s}"
            )

    explanation.append("")

    explanation.append(
        result.get(
            "explanation",
            ""
        )
    )

    return "\n".join(explanation)


def generate_learning_plan(missing_skills):

    if not missing_skills:
        return {
            "weeks": [],
            "summary": "Your resume already covers most required skills."
        }

    if isinstance(missing_skills, list):
        skills = ", ".join(missing_skills)
    else:
        skills = str(missing_skills)

    prompt = render_prompt(PROMPTS["learning"], 
        skills=skills
    )

    result = ask_llm(prompt)

    if not result:
        return {
            "weeks": []
        }

    return result


def predict_interview_questions(resume, job):

    if isinstance(resume, dict):
        resume = resume_to_text(resume)

    if isinstance(job, dict):
        job = json.dumps(job, indent=2)

    prompt = render_prompt(PROMPTS["interview"], 
        resume=resume,
        job=job
    )

    result = ask_llm(prompt)

    if not result:
        return {
            "technical": [],
            "behavioural": []
        }

    return result


def summarize_company(company):

    if isinstance(company, dict):
        company = json.dumps(company, indent=2)

    prompt = render_prompt(PROMPTS["company"], 
        company=company
    )

    result = ask_llm(prompt)

    if not result:
        return {
            "summary": "",
            "culture": "",
            "pros": [],
            "cons": []
        }

    return result


def recommend_jobs(analysed_jobs, limit=10):

    ranked = rank_jobs(analysed_jobs)

    recommendations = []

    for item in ranked[:limit]:

        recommendations.append({

            "title": item["job"].get("title"),

            "company": item["job"].get("company"),

            "location": item["job"].get("location"),

            "score": item["analysis"].get("overall_score"),

            "priority": item["analysis"].get("priority"),

            "explanation": item["analysis"].get("explanation"),

            "missing_skills": item["analysis"].get(
                "missing_skills",
                []
            )

        })

    return recommendations


def career_summary(analysed_jobs):

    if not analysed_jobs:

        return {
            "total_jobs": 0,
            "average_score": 0,
            "high_priority_jobs": 0,
            "top_skill_gaps": []
        }

    scores = []

    missing = []

    high_priority = 0

    for item in analysed_jobs:

        analysis = item["analysis"]

        scores.append(
            analysis.get(
                "overall_score",
                0
            )
        )

        if analysis.get(
            "priority",
            ""
        ).lower() == "high":

            high_priority += 1

        missing.extend(
            analysis.get(
                "missing_skills",
                []
            )
        )

    average_score = round(
        sum(scores) / len(scores),
        2
    )

    frequency = {}

    for skill in missing:

        frequency[skill] = frequency.get(skill, 0) + 1

    top_skill_gaps = sorted(

        frequency.items(),

        key=lambda x: x[1],

        reverse=True

    )[:10]

    return {

        "total_jobs": len(analysed_jobs),

        "average_score": average_score,

        "high_priority_jobs": high_priority,

        "top_skill_gaps": top_skill_gaps

    }


def print_job_report(job):

    analysis = job["analysis"]

    info = job["job"]

    print("=" * 60)

    print(info.get("title", ""))

    print(info.get("company", ""))

    print(info.get("location", ""))

    print()

    print("Match Score :", analysis.get("overall_score"))

    print("Priority    :", analysis.get("priority"))

    print()

    print("Strengths")

    for skill in analysis.get(
        "strengths",
        []
    ):
        print(f"  ✓ {skill}")

    print()

    print("Missing Skills")

    for skill in analysis.get(
        "missing_skills",
        []
    ):
        print(f"  ✗ {skill}")

    print()

    print("Explanation")

    print(analysis.get("explanation", ""))

    print("=" * 60)


def print_recommendations(recommendations):

    print()

    print("=" * 70)

    print("SMARTSCOUT RECOMMENDATIONS")

    print("=" * 70)

    for i, job in enumerate(recommendations, start=1):

        print(f"\n{i}. {job['title']}")

        print(f"Company : {job['company']}")

        print(f"Location: {job['location']}")

        print(f"Score   : {job['score']}%")

        print(f"Priority: {job['priority']}")

        print(f"Missing : {', '.join(job['missing_skills'])}")

        print(f"Reason  : {job['explanation']}")
        
        
        
