from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserRegister
from app.models.user import User
from app.db.session import SessionLocal
from app.core.security import verify_password, create_access_token, get_password_hash

router = APIRouter()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(user_data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if user.status != "active":
        raise HTTPException(status_code=403, detail="Account not yet approved")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        role="staff",
        status="pending",
        school = user_data.school
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Account request submitted. Awaiting approval."}
