import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base_class import Base
from app.models.user import User
from app.core.security import get_password_hash
from app.services import ai_assistant, embedding
from app.api.routes import auth, students, jobs, match

@pytest.fixture()
def client_and_db(monkeypatch):
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    # Override DB dependencies
    for module in (auth, students, jobs, match):
        app.dependency_overrides[module.get_db] = override_get_db

    # Patch AI-related functions
    monkeypatch.setattr(ai_assistant, "generate_summary", lambda *a, **k: "AI Summary")
    monkeypatch.setattr(embedding, "get_embedding", lambda *a, **k: [1.0, 0.0])

    client = TestClient(app)
    yield client, TestingSessionLocal

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)

def create_user(SessionLocal, email, password, role="staff", status="active", school="Test"):
    db = SessionLocal()
    user = User(
        email=email,
        hashed_password=get_password_hash(password),
        role=role,
        status=status,
        school=school,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user
