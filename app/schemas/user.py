from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    status: str

    class Config:
        from_attributes = True  # replaces orm_mode in Pydantic v2

class UserRegister(BaseModel):
    email: EmailStr
    password: str
