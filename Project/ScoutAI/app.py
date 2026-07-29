

from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional

BASE_DIR = Path(__file__).resolve().parent

from scraper import search_jobs
from ai_engine import (
    parse_resume,
    analyse_jobs,
    generate_learning_plan,
    career_summary,
)
from database import (
    save_resume,
    get_resume,
    save_jobs,
    get_all_jobs,
    save_analysis,
    get_latest_analysis,
)
from analytics import generate_dashboard


app = FastAPI(
    title="SmartScout API",
    description="AI Powered Job Discovery & Career Intelligence Suite",
    version="1.0.0",
)



from config import settings as app_settings

app.add_middleware(
    CORSMiddleware,
    # allow_credentials=True is incompatible with a wildcard origin
    # (browsers reject it) - scope this to the configured frontend and local hosts.
    allow_origins=[
        app_settings.FRONTEND_URL,
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class JobSearchRequest(BaseModel):
    role: str
    location: str = "India"
    max_results: int = 20
    resume_id: Optional[int] = None


class ResumeJobAnalysisRequest(BaseModel):
    resume_id: int




@app.get("/", response_class=FileResponse)
def home():
    return FileResponse(BASE_DIR / "index.html")


@app.get("/index.html", response_class=FileResponse)
def serve_index_html():
    return FileResponse(BASE_DIR / "index.html")


@app.get("/app.js", response_class=FileResponse)
def serve_app_js():
    return FileResponse(BASE_DIR / "app.js")


@app.get("/style.css", response_class=FileResponse)
def serve_style_css():
    return FileResponse(BASE_DIR / "style.css")


@app.get("/api/info")
def api_info():
    return {
        "application": "SmartScout",
        "version": "1.0",
        "status": "Running"
    }




@app.post("/resume/upload")
@app.post("/upload_resume")
async def upload_resume(
    file: Optional[UploadFile] = File(None),
    resume: Optional[UploadFile] = File(None),
):
    """
    Upload a resume PDF
    Extract information
    Save into database
    """
    upload_file = file or resume
    if not upload_file:
        raise HTTPException(
            status_code=400,
            detail="No resume file provided."
        )

    extension = (upload_file.filename or "").rsplit(".", 1)[-1].lower()

    if extension not in app_settings.ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: .{extension}"
        )

    try:

        resume_bytes = await upload_file.read()

        max_bytes = app_settings.MAX_RESUME_SIZE_MB * 1024 * 1024

        if len(resume_bytes) > max_bytes:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max size is {app_settings.MAX_RESUME_SIZE_MB}MB."
            )

        parsed_resume = parse_resume(
            resume_bytes,
            filename=upload_file.filename
        )

        resume_id = save_resume(parsed_resume)

        return {
            "success": True,
            "resume_id": resume_id,
            "resume": parsed_resume,
            "message": "Resume uploaded successfully."
        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )




@app.post("/jobs/search")
@app.post("/search_jobs")
def search(request: JobSearchRequest):
    """
    Search jobs from web / AI fallback.
    Save jobs & score against resume if provided.
    """

    jobs = search_jobs(
        role=request.role,
        location=request.location,
        max_results=request.max_results,
    )

    save_jobs(jobs)

    resume = None
    if request.resume_id:
        resume = get_resume(request.resume_id)

    if resume:
        formatted_jobs = analyse_jobs(resume=resume, jobs=jobs)
        save_analysis(request.resume_id, formatted_jobs)
    else:
        formatted_jobs = []
        for j in jobs:
            default_score = j.get("match_score") or (85 if "Senior" in j.get("title", "") else 75)
            formatted_jobs.append({
                "job": j,
                "analysis": {
                    "overall_score": default_score,
                    "priority": "High" if default_score >= 80 else ("Medium" if default_score >= 60 else "Low"),
                    "strengths": j.get("required_skills", []),
                    "missing_skills": j.get("missing_skills", []),
                    "explanation": j.get("explanation") or f"Direct role match for {request.role}."
                }
            })

    dash = generate_dashboard(formatted_jobs)

    return {
        "jobs_found": len(jobs),
        "jobs": formatted_jobs,
        "dashboard": dash
    }




@app.post("/jobs/analyse")
def analyse(request: ResumeJobAnalysisRequest):
    """
    Compare every job
    against uploaded resume.
    """

    resume = get_resume(request.resume_id)

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found."
        )

    jobs = get_all_jobs()

    analysed = analyse_jobs(
        resume=resume,
        jobs=jobs
    )

    save_analysis(request.resume_id, analysed)

    return {
        "total_jobs": len(analysed),
        "results": analysed
    }




@app.get("/dashboard")
def dashboard(resume_id: Optional[int] = None):
    """
    Returns analytics over the most recently run job analysis.
    Pass ?resume_id= to scope to a specific resume's analysis run,
    otherwise the latest analysis run (any resume) is used.
    """

    analysed_jobs = get_latest_analysis(resume_id)

    return generate_dashboard(analysed_jobs)




@app.post("/learning-plan")
def roadmap(request: ResumeJobAnalysisRequest):

    analysed_jobs = get_latest_analysis(request.resume_id)

    if not analysed_jobs:
        raise HTTPException(
            status_code=400,
            detail="Run /jobs/analyse for this resume first."
        )

    summary = career_summary(analysed_jobs)

    missing_skills = [
        skill for skill, _count in summary["top_skill_gaps"]
    ]

    plan = generate_learning_plan(missing_skills)

    return {
        "learning_plan": plan
    }




@app.post("/jobs/interview-questions")
def interview_questions(payload: dict):
    from ai_engine import predict_interview_questions
    resume_id = payload.get("resume_id")
    job = payload.get("job", {})
    resume = get_resume(resume_id) if resume_id else {}
    return predict_interview_questions(resume, job)


@app.get("/jobs")
def jobs():

    return get_all_jobs()





@app.get("/health")
def health():

    return {
        "status": "healthy"
    }



if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )