from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.db.base_class import Base

class Placement(Base):
    __tablename__ = "placements"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    employer = Column(String, nullable=False)
    job_title = Column(String, nullable=True)
    status = Column(String, default="placed")
    created_at = Column(DateTime, default=datetime.utcnow)
