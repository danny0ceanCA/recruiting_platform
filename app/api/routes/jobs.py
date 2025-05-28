from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import SessionLocal
from app.models.job import Job
from app.schemas.job import JobCreate, JobOut
from app.api.dependencies import get_current_user
from app.models.user import User

# Debug confirmation that this route file was loaded
print("✅ jobs.py loaded")

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new job posting
@router.post("/jobs/", response_model=JobOut)
def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_job = Job(**job_data.dict())
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    print(f"📌 New job created: {new_job.title} (ID: {new_job.id})")  # Optional debug
    return new_job

# Get a list of all job postings
@router.get("/jobs/", response_model=List[JobOut])
def list_jobs(db: Session = Depends(get_db)):
    return db.query(Job).order_by(Job.created_at.desc()).all()
