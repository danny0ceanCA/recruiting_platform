from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader  # Use this instead
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.core.security import SECRET_KEY, ALGORITHM
from app.models.user import User
from app.db.session import SessionLocal

# Use APIKeyHeader instead of OAuth2PasswordBearer
api_key_header = APIKeyHeader(name="Authorization")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(api_key_header), db: Session = Depends(get_db)) -> User:
    if not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = token.split("Bearer ")[-1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Token missing email")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
