from sqlalchemy import Column, Integer, String
from app.db.base_class import Base  # ✅ shared Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="staff")
    status = Column(String, default="pending")
    school = Column(String, nullable=False)
