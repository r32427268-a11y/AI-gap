from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import Project, User
from database.schemas import ProjectCreate, ProjectResponse

router = APIRouter()


# -------------------------
# Create Project
# -------------------------

@router.post("/", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == project.user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    new_project = Project(
        user_id=project.user_id,
        name=project.name,
        description=project.description,
        technologies=project.technologies
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


# -------------------------
# Get User Projects
# IMPORTANT:
# This route comes before /{project_id}
# -------------------------

@router.get("/user/{user_id}", response_model=list[ProjectResponse])
def get_user_projects(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return db.query(Project).filter(
        Project.user_id == user_id
    ).all()


# -------------------------
# Get Single Project
# -------------------------

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project


# -------------------------
# Update Project
# -------------------------

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_data: ProjectCreate,
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    user = db.query(User).filter(
        User.id == project_data.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    project.user_id = project_data.user_id
    project.name = project_data.name
    project.description = project_data.description
    project.technologies = project_data.technologies

    db.commit()
    db.refresh(project)

    return project


# -------------------------
# Delete Project
# -------------------------

@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    db.delete(project)
    db.commit()

    return {
        "message": "Project deleted successfully"
    }