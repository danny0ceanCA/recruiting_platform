from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.job import Job
from app.schemas.student import StudentMatchOut  # ✅ new schema
from app.services.matching import match_students_to_job
from app.api.dependencies import admin_required
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/match-now/", response_model=List[StudentMatchOut], dependencies=[Depends(admin_required)])  # ✅ update response model
def match_now(
    job_id: int,
    db: Session = Depends(get_db),
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    matches = match_students_to_job(job.description, db)
    return matches  # ✅ already returns list of {"student": ..., "match_score": ...}
