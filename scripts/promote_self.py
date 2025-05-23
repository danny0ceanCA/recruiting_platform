import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from app.db.session import SessionLocal
from app.models.user import User
from app.models import Student, Job

# 👇 Set the email you want to promote
admin_email = "daniel@gmail.com"

db = SessionLocal()

print("📋 All users in the database:")
users = db.query(User).all()

for u in users:
    print(f"- ID: {u.id}, Email: {u.email}, Role: {u.role}, Status: {u.status}, School: {u.school}")

user = db.query(User).filter(User.email == admin_email).first()

if user:
    user.role = "admin"
    user.status = "active"
    db.commit()
    print(f"\n✅ {admin_email} promoted to admin and activated.")
else:
    print(f"\n❌ User with email {admin_email} not found.")
