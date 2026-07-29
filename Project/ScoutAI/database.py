"""
SmartScout Database
--------------------
SQLite-backed storage for parsed resumes, scraped jobs, and
resume-vs-job analysis results (this file was imported by app.py
but did not exist in the project - added to make it runnable).
"""

import json
from datetime import datetime, timezone

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

from config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


class ResumeRecord(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, default="")
    data = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class JobRecord(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, default="")
    company = Column(String, default="")
    location = Column(String, default="")
    application_url = Column(String, default="")
    data = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AnalysisRecord(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, index=True)
    data = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


Base.metadata.create_all(bind=engine)


# ------------------------------------------------------------------
# Resumes
# ------------------------------------------------------------------

def save_resume(resume: dict) -> int:
    session = SessionLocal()
    try:
        record = ResumeRecord(
            filename=resume.get("filename", ""),
            data=json.dumps(resume, ensure_ascii=False),
        )
        session.add(record)
        session.commit()
        session.refresh(record)
        return record.id
    finally:
        session.close()


def get_resume(resume_id: int):
    session = SessionLocal()
    try:
        record = session.get(ResumeRecord, resume_id)
        if not record:
            return None
        return json.loads(record.data)
    finally:
        session.close()


# ------------------------------------------------------------------
# Jobs
# ------------------------------------------------------------------

def save_jobs(jobs: list) -> list:
    if not jobs:
        return []

    session = SessionLocal()
    try:
        saved_ids = []
        for job in jobs:
            record = JobRecord(
                title=job.get("title", ""),
                company=job.get("company", ""),
                location=job.get("location", ""),
                application_url=job.get("application_url", ""),
                data=json.dumps(job, ensure_ascii=False),
            )
            session.add(record)
            session.flush()
            saved_ids.append(record.id)
        session.commit()
        return saved_ids
    finally:
        session.close()


def get_all_jobs() -> list:
    session = SessionLocal()
    try:
        records = (
            session.query(JobRecord)
            .order_by(JobRecord.id.desc())
            .all()
        )
        jobs = []
        for record in records:
            job = json.loads(record.data)
            job["id"] = record.id
            jobs.append(job)
        return jobs
    finally:
        session.close()


# ------------------------------------------------------------------
# Analysis results (resume x job matches)
# ------------------------------------------------------------------

def save_analysis(resume_id: int, analysed_jobs: list) -> int:
    session = SessionLocal()
    try:
        record = AnalysisRecord(
            resume_id=resume_id,
            data=json.dumps(analysed_jobs, ensure_ascii=False),
        )
        session.add(record)
        session.commit()
        session.refresh(record)
        return record.id
    finally:
        session.close()


def get_latest_analysis(resume_id: int = None) -> list:
    """
    Returns the most recently saved analysis. If resume_id is given,
    scopes to that resume; otherwise returns the latest analysis run
    for any resume (used by the dashboard when no resume is specified).
    """
    session = SessionLocal()
    try:
        query = session.query(AnalysisRecord)
        if resume_id is not None:
            query = query.filter(AnalysisRecord.resume_id == resume_id)
        record = query.order_by(AnalysisRecord.id.desc()).first()
        if not record:
            return []
        return json.loads(record.data)
    finally:
        session.close()
