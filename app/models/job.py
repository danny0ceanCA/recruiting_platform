from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.db.session import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    license_type = Column(String, nullable=False)
    location = Column(String, nullable=False)
    schedule = Column(String)
    pay = Column(Float)
    description = Column(String)
    tags = Column(String)
    urgency = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
