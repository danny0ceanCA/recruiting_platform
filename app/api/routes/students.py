# app/api/routes/students.py

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os, json

from app.models.student import Student
from app.schemas.student import StudentOut, StudentCreate, StudentUpdate
from app.services.ai_assistant import generate_summary
from app.services.embedding import get_embedding
from app.db.session import SessionLocal
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/students", tags=["students"])

# Where to save uploaded resumes
UPLOAD_DIR = "uploads/resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1) Create a new student via form+file upload
@router.post("/start", response_model=StudentOut)
def create_student_profile(
    first_name: str = Form(...),
    last_name: str = Form(...),
    license_type: str = Form(...),
    school: str = Form(...),
    job_goals: str = Form(None),
    availability: str = Form(None),
    transportation: str = Form(None),
    experience: str = Form(None),
    soft_skills: str = Form(None),
    resume: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Save resume file if provided
    resume_path = None
    if resume:
        filename = f"{first_name}_{last_name}_{resume.filename}"
        resume_path = os.path.join(UPLOAD_DIR, filename)
        with open(resume_path, "wb") as f:
            f.write(resume.file.read())

    # Build a Pydantic model to pass into OpenAI
    student_dict = {
        "first_name": first_name,
        "last_name": last_name,
        "license_type": license_type,
        "school": school,
        "job_goals": job_goals,
        "availability": availability,
        "transportation": transportation,
        "experience": experience,
        "soft_skills": soft_skills,
        "email": None,
    }
    student_obj = StudentCreate(**student_dict)

    # AI summary + embedding
    summary = generate_summary(student_obj)
    embedding = get_embedding(summary)

    # Persist to DB
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

# 2) List all submitted students
@router.get("/", response_model=List[StudentOut])
def list_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Student).order_by(Student.created_at.desc())
    if current_user.role != "admin":
        query = query.filter(Student.school == current_user.school)
    return query.all()

# 3) Fetch one student by ID
@router.get("/{student_id}", response_model=StudentOut)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Student).filter(Student.id == student_id)
    if current_user.role != "admin":
        query = query.filter(Student.school == current_user.school)
    student = query.first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# 4) Update an existing student
@router.patch("/{student_id}", response_model=StudentOut)
def update_student(
    student_id: int,
    first_name: str = Form(None),
    last_name: str = Form(None),
    license_type: str = Form(None),
    school: str = Form(None),
    job_goals: str = Form(None),
    availability: str = Form(None),
    transportation: str = Form(None),
    experience: str = Form(None),
    soft_skills: str = Form(None),
    email: str = Form(None),
    resume: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Student).filter(Student.id == student_id)
    if current_user.role != "admin":
        query = query.filter(Student.school == current_user.school)
    student = query.first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Save new resume if provided
    if resume:
        filename = f"{student.first_name}_{student.last_name}_{resume.filename}"
        resume_path = os.path.join(UPLOAD_DIR, filename)
        with open(resume_path, "wb") as f:
            f.write(resume.file.read())
        student.resume_path = resume_path

    update_data = StudentUpdate(
        first_name=first_name,
        last_name=last_name,
        license_type=license_type,
        school=school,
        job_goals=job_goals,
        availability=availability,
        transportation=transportation,
        experience=experience,
        soft_skills=soft_skills,
        email=email,
    ).dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(student, field, value)

    # Regenerate summary and embedding if any field updated
    if update_data or resume:
        student_dict = {
            "first_name": student.first_name,
            "last_name": student.last_name,
            "license_type": student.license_type,
            "school": student.school,
            "job_goals": student.job_goals,
            "availability": student.availability,
            "transportation": student.transportation,
            "experience": student.experience,
            "soft_skills": student.soft_skills,
            "email": student.email,
        }
        summary = generate_summary(StudentCreate(**student_dict))
        embedding = get_embedding(summary)
        student.ai_summary = summary
        student.embedding = json.dumps(embedding)

    db.commit()
    db.refresh(student)
    return student
