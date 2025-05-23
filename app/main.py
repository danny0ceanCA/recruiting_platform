from app.api.routes import reporting
from app.api.routes import bulk_upload_csv
from app.api.routes import match
from fastapi import FastAPI
from app.api.routes import auth, students
from app.api.routes import jobs
import os

app = FastAPI()

# Debug print to confirm which main.py is loaded
print("📄 Loaded main.py from:", os.path.abspath(__file__))

# Include your routes here
app.include_router(auth.router, tags=["Authentication"])
app.include_router(students.router, tags=["Students"])
app.include_router(jobs.router, tags=["Jobs"])
app.include_router(match.router, tags=["Matching"])
app.include_router(reporting.router, tags=["Reporting"])
app.include_router(bulk_upload_csv.router, tags=["Students"])



# Debug print to show all registered routes
for route in app.routes:
    print(f"🛣️ {route.path} → {route.name}")
