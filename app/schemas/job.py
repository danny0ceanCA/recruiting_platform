from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JobCreate(BaseModel):
    title: str
    license_type: str
    location: str
    schedule: Optional[str]
    pay: Optional[float]
    description: Optional[str]
    tags: Optional[str]
    urgency: Optional[str]

class JobOut(JobCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
