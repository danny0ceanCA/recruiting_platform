from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PlacementCreate(BaseModel):
    student_id: int
    employer: str
    job_title: Optional[str] = None
    status: Optional[str] = "placed"

class PlacementOut(PlacementCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PlacementUpdate(BaseModel):
    employer: Optional[str] = None
    job_title: Optional[str] = None
    status: Optional[str] = None
