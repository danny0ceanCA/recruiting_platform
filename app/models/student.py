from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.session import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    school = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    license_type = Column(String, nullable=False)
    job_goals = Column(String)
    availability = Column(String)
    transportation = Column(String)
    experience = Column(String)
    soft_skills = Column(String)
    ai_summary = Column(String)
    embedding = Column(String)  # JSON string
    resume_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
