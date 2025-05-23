from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, students, jobs, match, reporting, bulk_upload_csv, admin_users
import os

app = FastAPI(
    title="Recruitment Platform API",
    description="Match students to healthcare jobs via AI-assisted tools.",
    version="1.0.0"
)

# Enable CORS (optional but good for frontend integrations)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Debug print to confirm which main.py is loaded
print("📄 Loaded main.py from:", os.path.abspath(__file__))

# Include routes
app.include_router(auth.router, tags=["Authentication"])
app.include_router(students.router, tags=["Students"])
app.include_router(jobs.router, tags=["Jobs"])
app.include_router(match.router, tags=["Matching"])
app.include_router(reporting.router, tags=["Reporting"])
app.include_router(bulk_upload_csv.router, tags=["Students"])
app.include_router(admin_users.router)

# Debug print to show all registered routes
for route in app.routes:
    print(f"🛣️ {route.path} → {route.name}")
