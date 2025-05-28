# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

# Import all routers
from app.api.routes import (
    auth,
    students,
    jobs,
    match,
    reporting,
    bulk_upload_csv,
    admin_users,
    users,
    placements,
)

# Instantiate FastAPI without automatic docs URLs
app = FastAPI(
    openapi_url="/openapi.json",  # serve the OpenAPI schema
    docs_url=None,                  # disable automatic Swagger UI
    redoc_url=None,                # disable automatic ReDoc
)

# DEV: Allow your React dev server (and any other) to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # for dev; in prod, lock this down
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Swagger UI endpoint
@app.get("/docs", include_in_schema=False)
def swagger_ui():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="Recruitment Platform API Docs",
    )

# Custom ReDoc endpoint
@app.get("/redoc", include_in_schema=False)
def redoc_ui():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title="Recruitment Platform ReDoc",
    )

# Mount all your routers
app.include_router(auth.router, prefix="", tags=["Authentication"])
app.include_router(students.router, prefix="", tags=["Students"])
app.include_router(jobs.router, prefix="", tags=["Jobs"])
app.include_router(match.router, prefix="", tags=["Matching"])
app.include_router(reporting.router, prefix="", tags=["Reporting"])
app.include_router(bulk_upload_csv.router, prefix="", tags=["Bulk Upload"])
app.include_router(admin_users.router, prefix="", tags=["Admin"])
app.include_router(users.router, prefix="", tags=["Users"])
app.include_router(placements.router, prefix="", tags=["Placements"])
