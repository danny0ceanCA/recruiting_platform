# app/models/__init__.py

from app.models.user import Base, User
from app.models.student import Student
from app.models.job import Job  # ✅ This was missing
from app.models.placement import Placement
