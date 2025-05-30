from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    status: str
    school: str

    class Config:
        from_attributes = True  # replaces orm_mode in Pydantic v2

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    school: str

from typing import Optional

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    school: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class PasswordChange(BaseModel):
    old_password: str
    new_password: str

class RoleUpdate(BaseModel):
    role: str
