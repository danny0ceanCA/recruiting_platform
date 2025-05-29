from app.core.security import create_access_token
from app.models.user import User
from app.api.routes import auth
from app.core.security import get_password_hash
from app.models.user import User
from app.models.job import Job
from sqlalchemy.orm import Session
from tests.conftest import create_user


def test_registration_and_login(client_and_db):
    client, SessionLocal = client_and_db
    data = {"email": "new@example.com", "password": "secret", "school": "Test"}
    resp = client.post("/register", json=data)
    assert resp.status_code == 200
    assert "Account request" in resp.json()["message"]

    # Login should fail while pending
    resp = client.post("/login", json={"email": data["email"], "password": data["password"]})
    assert resp.status_code == 403

    # Activate user and login
    db = SessionLocal()
    user = db.query(User).filter(User.email == data["email"]).first()
    user.status = "active"
    db.commit()
    db.close()

    resp = client.post("/login", json={"email": data["email"], "password": data["password"]})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_create_student(client_and_db):
    client, SessionLocal = client_and_db
    create_user(SessionLocal, "staff@example.com", "password", role="staff", status="active")

    login = client.post("/login", json={"email": "staff@example.com", "password": "password"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    data = {
        "first_name": "John",
        "last_name": "Doe",
        "license_type": "RN",
        "school": "Test",
    }
    resp = client.post("/students/start", headers=headers, data=data)
    assert resp.status_code == 200
    assert resp.json()["first_name"] == "John"


def test_create_job_admin(client_and_db):
    client, SessionLocal = client_and_db
    create_user(SessionLocal, "admin@example.com", "password", role="admin", status="active")

    login = client.post("/login", json={"email": "admin@example.com", "password": "password"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    job = {
        "title": "Nurse",
        "license_type": "RN",
        "location": "NY",
        "schedule": "FT",
        "pay": 30.0,
        "description": "Desc",
        "tags": "",
        "urgency": "low",
    }
    resp = client.post("/jobs/", json=job, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["title"] == job["title"]


def test_matching_flow(client_and_db):
    client, SessionLocal = client_and_db
    # create users
    create_user(SessionLocal, "admin@example.com", "password", role="admin", status="active")
    create_user(SessionLocal, "staff@example.com", "password", role="staff", status="active")

    # login staff and create student
    token_staff = client.post("/login", json={"email": "staff@example.com", "password": "password"}).json()["access_token"]
    headers_staff = {"Authorization": f"Bearer {token_staff}"}
    student = {
        "first_name": "John",
        "last_name": "Doe",
        "license_type": "RN",
        "school": "Test",
    }
    client.post("/students/start", headers=headers_staff, data=student)

    # login admin and create job
    token_admin = client.post("/login", json={"email": "admin@example.com", "password": "password"}).json()["access_token"]
    headers_admin = {"Authorization": f"Bearer {token_admin}"}
    job = {
        "title": "Nurse",
        "license_type": "RN",
        "location": "NY",
        "schedule": "FT",
        "pay": 30.0,
        "description": "Desc",
        "tags": "",
        "urgency": "low",
    }
    job_resp = client.post("/jobs/", json=job, headers=headers_admin)
    job_id = job_resp.json()["id"]

    match_resp = client.post("/match-now/", json={"job_id": job_id}, headers=headers_admin)
    assert match_resp.status_code == 200
    matches = match_resp.json()
    assert len(matches) >= 1
    assert matches[0]["student"]["first_name"] == "John"
