# app/models/__init__.py

from app.models.user import Base  # 👈 Base is defined in user.py, we expose it here
from app.models.user import User
from app.models.student import Student
