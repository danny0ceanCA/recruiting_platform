from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.student import Student
from app.services.ai_assistant import generate_summary
from app.services.embedding import get_embedding
from app.schemas.student import StudentCreate  # ✅ Import schema for summary generation
from app.api.dependencies import get_current_user
from app.models.user import User
import csv, json, io

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/students/upload-csv")
def upload_students_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a .csv")

    content = file.file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))

    created_students = []

    for row in reader:
        try:
            student_obj = StudentCreate(**row)  # ✅ Convert row to schema
            summary = generate_summary(student_obj)
            embedding = get_embedding(summary)

            new_student = Student(
                first_name=student_obj.first_name,
                last_name=student_obj.last_name,
                school=student_obj.school,
                email=student_obj.email,
                license_type=student_obj.license_type,
                job_goals=student_obj.job_goals,
                availability=student_obj.availability,
                transportation=student_obj.transportation,
                experience=student_obj.experience,
                soft_skills=student_obj.soft_skills,
                ai_summary=summary,
                embedding=json.dumps(embedding)
            )
            db.add(new_student)
            created_students.append(f"{student_obj.first_name} {student_obj.last_name}")
        except Exception as e:
            print(f"⚠️ Failed to process row: {row} — {e}")
            continue

    db.commit()
    return {"created": created_students, "total": len(created_students)}
