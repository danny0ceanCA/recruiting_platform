from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import SessionLocal
from app.models.student import Student
from app.models.placement import Placement
from app.models.user import User
from app.api.dependencies import get_current_user
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict:
    if current_user.role != "admin" and current_user.school != school:
        raise HTTPException(status_code=403, detail="Not authorized for this school")

    students_query = db.query(Student).filter(Student.school == school)
    total_students = students_query.count()

    if total_students == 0:
        raise HTTPException(status_code=404, detail=f"No students found for school '{school}'")

    total_placed = db.query(func.count(Placement.id)) \
        .join(Student, Student.id == Placement.student_id) \
        .filter(Student.school == school, Placement.status == "placed") \
        .scalar()

    placement_rate = (total_placed / total_students) * 100 if total_students else 0

    interviews = db.query(Placement.employer, func.count(Placement.id)) \
        .join(Student, Student.id == Placement.student_id) \
        .filter(Student.school == school, Placement.status == "interview") \
        .group_by(Placement.employer) \
        .all()

    interviews_by_employer = {emp: count for emp, count in interviews}

    avg_time_to_place = db.query(
        func.avg(func.julianday(Placement.created_at) - func.julianday(Student.created_at))
    ).join(Student, Student.id == Placement.student_id) \
     .filter(Student.school == school, Placement.status == "placed") \
     .scalar()

    avg_time_to_place = avg_time_to_place or 0
    return {
        "total_students": total_students,
        "total_placed": total_placed,
        "placement_rate": placement_rate,
        "interviews_by_employer": interviews_by_employer,
        "average_time_to_place_days": avg_time_to_place,
    }
