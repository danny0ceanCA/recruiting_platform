from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_current_user, admin_required
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.user import UserOut, UserUpdate, PasswordChange, RoleUpdate
from app.core.security import verify_password, get_password_hash

router = APIRouter(prefix="/users", tags=["users"])

# Local DB dependency for this router
# (reuse SessionLocal as other route modules do)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.school is not None:
        user.school = user_update.school
    db.commit()
    db.refresh(user)
    return user

@router.post("/change-password")
def change_password(
    passwords: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not verify_password(passwords.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect current password")
    user.hashed_password = get_password_hash(passwords.new_password)
    db.commit()
    return {"message": "Password updated"}

@router.get("/", response_model=List[UserOut], dependencies=[Depends(admin_required)])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.post("/{user_id}/role", dependencies=[Depends(admin_required)])
def change_role(
    user_id: int,
    role_update: RoleUpdate,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = role_update.role
    db.commit()
    return {"message": f"Role updated to {user.role}"}
