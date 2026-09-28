from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import (
    analysis,
    github,
    interview,
    resume,
    profile,
    skills,
    projects,
    roles
)


# ============================================================
# CREATE FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="AI Career Gap Navigator API",
    description="Backend API for AI-powered career gap analysis",
    version="1.0.0"
)


# ============================================================
# CORS CONFIGURATION
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "AI Career Gap Navigator API is running",
        "docs": "/docs"
    }


# ============================================================
# API ROUTES
# ============================================================

app.include_router(
    analysis.router,
    prefix="/api/analysis",
    tags=["analysis"]
)

app.include_router(
    github.router,
    prefix="/api/github",
    tags=["github"]
)

app.include_router(
    interview.router,
    prefix="/api/interview",
    tags=["interview"]
)

app.include_router(
    resume.router,
    prefix="/api/resume",
    tags=["resume"]
)

app.include_router(
    profile.router,
    prefix="/api/profile",
    tags=["profile"]
)

app.include_router(
    skills.router,
    prefix="/api/skills",
    tags=["skills"]
)

app.include_router(
    projects.router,
    prefix="/api/projects",
    tags=["projects"]
)

app.include_router(
    roles.router,
    prefix="/api/roles",
    tags=["roles"]
)
