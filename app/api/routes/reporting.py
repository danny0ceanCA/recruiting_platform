from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import SessionLocal
from app.models.student import Student
from app.models.placement import Placement
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
    students_query = db.query(Student).filter(Student.school == school)
    total_students = students_query.count()

    if total_students == 0:
        raise HTTPException(status_code=404, detail=f"No students found for school '{school}'")

    total_placed = db.query(func.count(Placement.id))\
        .join(Student, Student.id == Placement.student_id)\
        .filter(Student.school == school, Placement.status == "placed")\
        .scalar()

    interviews = db.query(Placement.employer, func.count(Placement.id))\
        .join(Student, Student.id == Placement.student_id)\
        .filter(Student.school == school, Placement.status == "interview")\
        .group_by(Placement.employer)\
        .all()

    interviews_by_employer = {emp: count for emp, count in interviews}

    placements_by_school = {
        school: total_placed
    }

    return {
        "total_students": total_students,
        "total_placed": total_placed,
        "placements_by_school": placements_by_school,
        "interviews_by_employer": interviews_by_employer
    }
