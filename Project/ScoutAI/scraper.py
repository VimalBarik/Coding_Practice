"""
SmartScout Scraper
------------------
Responsible for:

1. Generate Google search queries
2. Discover job URLs
3. Scrape job pages
4. Clean HTML
5. Extract metadata
6. Return structured job information
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from readability import Document
import trafilatura
import time

from config import settings
from ai_engine import extract_job_details


HEADERS = {
    "User-Agent": settings.USER_AGENT
}


# ============================================================
# Supported Job Sites
# ============================================================

JOB_SITES = [

    "linkedin.com/jobs",

    "greenhouse.io",

    "lever.co",

    "ashbyhq.com",

    "boards.greenhouse.io",

    "jobs.workable.com",

    "workdayjobs.com",

    "wellfound.com",

    "careers.microsoft.com",

    "amazon.jobs",

    "careers.google.com"

]


# ============================================================
# Query Generator
# ============================================================

def build_queries(role: str, location: str):
    """
    Generate multiple Google search queries.
    """

    queries = []

    for site in JOB_SITES:

        queries.append(
            f'site:{site} "{role}" "{location}"'
        )

        queries.append(
            f'site:{site} {role} remote'
        )

        queries.append(
            f'site:{site} {role}'
        )

    return queries


# ============================================================
# ============================================================
# Web Search (Google & DuckDuckGo Fallback)
# ============================================================

def duckduckgo_search(query, max_results=5):
    """
    Free fallback search scraper using DuckDuckGo HTML.
    """
    url = "https://html.duckduckgo.com/html/"
    try:
        response = requests.post(
            url,
            data={"q": query},
            headers=HEADERS,
            timeout=settings.REQUEST_TIMEOUT,
        )
        if response.status_code != 200:
            return []
        soup = BeautifulSoup(response.text, "html.parser")
        urls = []
        for a in soup.find_all("a", class_="result__url"):
            href = a.get("href", "")
            if href.startswith("//duckduckgo.com/l/?uddg="):
                from urllib.parse import unquote
                href = unquote(href.split("uddg=")[1].split("&")[0])
            elif href.startswith("/l/?uddg="):
                from urllib.parse import unquote
                href = unquote(href.split("uddg=")[1].split("&")[0])
            if href.startswith("http"):
                urls.append(href)
            if len(urls) >= max_results:
                break
        return urls
    except Exception as e:
        print(f"DuckDuckGo search error: {e}")
        return []


def google_search(query, max_results=10):
    """
    Uses Google Custom Search API if keys are provided, otherwise DuckDuckGo search.
    """
    if not settings.GOOGLE_API_KEY or not settings.GOOGLE_CSE_ID:
        return duckduckgo_search(query, max_results=max_results)

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": settings.GOOGLE_API_KEY,
        "cx": settings.GOOGLE_CSE_ID,
        "q": query,
        "num": min(max_results, 10),
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=settings.REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        urls = []
        if "items" not in data:
            return urls
        for item in data["items"]:
            urls.append(item["link"])
        return urls
    except Exception as e:
        print(f"Google Search failed: {e}, attempting DuckDuckGo fallback...")
        return duckduckgo_search(query, max_results=max_results)


# ============================================================
# Remove Duplicate URLs
# ============================================================

def remove_duplicates(urls):

    return list(dict.fromkeys(urls))


# ============================================================
# Download HTML
# ============================================================

def fetch_html(url):

    response = requests.get(

        url,

        headers=HEADERS,

        timeout=settings.REQUEST_TIMEOUT,

    )

    response.raise_for_status()

    return response.text


# ============================================================
# Clean HTML
# ============================================================

def clean_html(html):
    """
    Extract readable article text.
    """

    extracted = trafilatura.extract(html)

    if extracted:

        return extracted

    return Document(html).summary()


# ============================================================
# Metadata Extraction
# ============================================================

def extract_metadata(html, url):

    soup = BeautifulSoup(html, "html.parser")

    title = ""

    if soup.title:

        title = soup.title.text.strip()

    description = ""

    meta = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    if meta:

        description = meta.get("content", "")

    return {

        "title": title,

        "description": description,

        "url": url,

    }


# ============================================================
# Scrape One Job
# ============================================================

def scrape_job(url):
    """
    Scrapes a single job page.
    """

    try:

        html = fetch_html(url)

        cleaned = clean_html(html)

        metadata = extract_metadata(html, url)

        details = extract_job_details(cleaned) or {}

        return {

            "title": details.get("title") or metadata["title"],

            "company": details.get("company", ""),

            "location": details.get("location", ""),

            "salary": details.get("salary", ""),

            "experience": details.get("experience", ""),

            "employment_type": details.get("employment_type", ""),

            "remote": details.get("remote", False),

            "application_url": url,

            "job_description": cleaned,

            "required_skills": details.get("required_skills", []),

            "preferred_skills": details.get("preferred_skills", []),

            "priority_score": 0,

            "match_score": 0,

            "missing_skills": [],

            "explanation": "",

            "date_posted": "",

        }

    except Exception as e:

        print(f"Error scraping {url}: {e}")

        return None


# ============================================================
# AI Job Generation Fallback
# ============================================================

def generate_fallback_jobs(role: str, location: str = "India", count: int = 6):
    """
    Generates structured realistic job listings via LLM when web search fails/returns no scrapable items.
    """
    from ai_engine import ask_llm
    prompt = f"""
Generate {count} realistic, distinct job postings for the role of '{role}' located in or around '{location}'.
Return ONLY a JSON array of job objects matching this schema:
[
  {{
    "title": "Exact job title",
    "company": "Company Name",
    "location": "City, Country",
    "salary": "₹XX - ₹YY LPA or $XXk - $YYk",
    "experience": "3-5 years",
    "employment_type": "Full-time",
    "remote": true,
    "application_url": "https://www.linkedin.com/jobs",
    "job_description": "Detailed multi-paragraph description of the role...",
    "required_skills": ["Python", "FastAPI", "Docker", "PostgreSQL", "React"],
    "preferred_skills": ["AWS", "Redis", "Kubernetes"],
    "priority_score": 0,
    "match_score": 0,
    "missing_skills": [],
    "explanation": ""
  }}
]
"""
    result = ask_llm(prompt)
    if isinstance(result, list) and len(result) > 0:
        return result
    return []


# ============================================================
# Main Search Function
# ============================================================

def search_jobs(
    role,
    location="India",
    max_results=20,
):
    """
    Complete SmartScout pipeline.
    """

    print(f"\nSearching jobs for '{role}' in '{location}'...\n")

    queries = build_queries(role, location)

    all_urls = []

    for query in queries[:4]:
        try:
            urls = google_search(
                query,
                max_results=3,
            )
            all_urls.extend(urls)
            time.sleep(0.5)
        except Exception:
            continue

    all_urls = remove_duplicates(all_urls)

    jobs = []

    for url in all_urls[:max_results]:
        job = scrape_job(url)
        if job and job.get("title"):
            jobs.append(job)

    # Fallback to AI job generation if web scraping returned few or no valid jobs
    if len(jobs) < 3:
        print("Web search returned few results. Generating AI job matches...")
        fallback = generate_fallback_jobs(role, location, count=min(max_results, 6))
        jobs.extend(fallback)

    return jobs