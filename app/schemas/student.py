from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    school: str
    email: Optional[str] = None
    license_type: str
    job_goals: Optional[str] = None
    availability: Optional[str] = None
    transportation: Optional[str] = None
    experience: Optional[str] = None
    soft_skills: Optional[str] = None

class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    school: Optional[str] = None
    email: Optional[str] = None
    license_type: Optional[str] = None
    job_goals: Optional[str] = None
    availability: Optional[str] = None
    transportation: Optional[str] = None
    experience: Optional[str] = None
    soft_skills: Optional[str] = None

class StudentOut(StudentCreate):
    id: int
    ai_summary: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class StudentMatchOut(BaseModel):
    student: StudentOut
    match_score: float

    class Config:
        from_attributes = True
