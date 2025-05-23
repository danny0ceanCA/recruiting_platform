from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.models.student import Student
from app.schemas.student import StudentOut, StudentCreate
from app.services.ai_assistant import generate_summary
from app.services.embedding import get_embedding
from app.db.session import SessionLocal
import os, json

router = APIRouter()

UPLOAD_DIR = "uploads/resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/students/start", response_model=StudentOut)
def create_student_profile(
    first_name: str = Form(...),
    last_name: str = Form(...),
    license_type: str = Form(...),
    school: str = Form(...),  # ✅ NEW field
    job_goals: str = Form(None),
    availability: str = Form(None),
    transportation: str = Form(None),
    experience: str = Form(None),
    soft_skills: str = Form(None),
    resume: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    # Save resume if uploaded
    resume_path = None
    if resume:
        filename = f"{first_name}_{last_name}_{resume.filename}"
        resume_path = os.path.join(UPLOAD_DIR, filename)
        with open(resume_path, "wb") as f:
            f.write(resume.file.read())

    # AI summary & embedding
    student_dict = {
        "first_name": first_name,
        "last_name": last_name,
        "license_type": license_type,
        "school": school,  # ✅ Include in dict
        "job_goals": job_goals,
        "availability": availability,
        "transportation": transportation,
        "experience": experience,
        "soft_skills": soft_skills,
        "email": None,
    }

    student_obj = StudentCreate(**student_dict)
    summary = generate_summary(student_obj)
    embedding = get_embedding(summary)

    new_student = Student(
        **student_dict,
        ai_summary=summary,
        embedding=json.dumps(embedding),
        resume_path=resume_path
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student
