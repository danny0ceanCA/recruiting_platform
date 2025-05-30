from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

# Create a test user
def create_user():
    db = SessionLocal()
    test_email = "test@example.com"
    test_password = "password123"

    # Check if user already exists
    existing_user = db.query(User).filter(User.email == test_email).first()
    if existing_user:
        print("Test user already exists.")
        return

    # Create user
    new_user = User(
        first_name="Test",
        last_name="User",
        email=test_email,
        hashed_password=get_password_hash(test_password),
        role="staff",
        school="Test School"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(f"Test user created: {new_user.email}")

if __name__ == "__main__":
    create_user()
