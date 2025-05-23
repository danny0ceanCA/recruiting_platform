from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.user import UserOut
from app.api.dependencies import admin_required

router = APIRouter(prefix="/admin", tags=["admin-users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/pending-users", response_model=List[UserOut], dependencies=[Depends(admin_required)])
def get_pending_users(db: Session = Depends(get_db)):
    return db.query(User).filter(User.status == "pending").all()

@router.post("/approve-user/{user_id}", dependencies=[Depends(admin_required)])
def approve_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.status = "active"
    db.commit()
    return {"message": f"User {user.email} approved."}

@router.post("/reject-user/{user_id}", dependencies=[Depends(admin_required)])
def reject_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.status = "rejected"
    db.commit()
    return {"message": f"User {user.email} rejected."}
