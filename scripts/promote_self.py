import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # ✅ Set path first

from app.db.session import SessionLocal
from app.models.user import User

db = SessionLocal()
your_email = "danielgojeda.1@gmail.com"

user = db.query(User).filter(User.email == your_email).first()
if user:
    user.role = "admin"
    user.status = "active"
    db.commit()
    print(f"✅ {your_email} promoted to admin and activated.")
else:
    print("❌ User not found.")
