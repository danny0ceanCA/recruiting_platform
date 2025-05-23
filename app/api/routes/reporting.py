from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.student import Student
from typing import Dict

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/reporting/overview")
def get_reporting_metrics(
    school: str = Query(..., description="School name to filter metrics"),
    db: Session = Depends(get_db)
) -> Dict:
    students = db.query(Student).filter(Student.school == school).all()
    total_students = len(students)

    if total_students == 0:
        raise HTTPException(status_code=404, detail=f"No students found for school '{school}'")

    # Placeholder values for future placement/interview tracking
    total_placed = 0
    interviews_by_employer = {
        "Action Supportive Care": 0,
        "Always Home Nursing": 0
    }

    placements_by_school = {
        school: total_students
    }

    return {
        "total_students": total_students,
        "total_placed": total_placed,
        "placements_by_school": placements_by_school,
        "interviews_by_employer": interviews_by_employer
    }
