from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import Role, Skill, RoleSkill
from database.schemas import (
    RoleCreate,
    RoleResponse,
    RoleSkillCreate,
    RoleSkillResponse
)

router = APIRouter()


# -------------------------
# Create Role
# -------------------------

@router.post("/", response_model=RoleResponse)
def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Role).filter(Role.name == role.name).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Role already exists"
        )

    new_role = Role(
        name=role.name,
        description=role.description
    )

    db.add(new_role)
    db.commit()
    db.refresh(new_role)

    return new_role


# -------------------------
# Get All Roles
# -------------------------

@router.get("/", response_model=list[RoleResponse])
def get_roles(db: Session = Depends(get_db)):
    return db.query(Role).all()


# -------------------------
# Add Skill to Role
# -------------------------

@router.post("/{role_id}/skills", response_model=RoleSkillResponse)
def add_role_skill(
    role_id: int,
    skill_data: RoleSkillCreate,
    db: Session = Depends(get_db)
):
    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    skill = db.query(Skill).filter(
        Skill.id == skill_data.skill_id
    ).first()

    if not skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    existing = db.query(RoleSkill).filter(
        RoleSkill.role_id == role_id,
        RoleSkill.skill_id == skill_data.skill_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Skill already assigned to this role"
        )

    role_skill = RoleSkill(
        role_id=role_id,
        skill_id=skill_data.skill_id,
        importance=skill_data.importance
    )

    db.add(role_skill)
    db.commit()
    db.refresh(role_skill)

    return role_skill


# -------------------------
# Get Skills for Role
# -------------------------

@router.get("/{role_id}/skills", response_model=list[RoleSkillResponse])
def get_role_skills(
    role_id: int,
    db: Session = Depends(get_db)
):
    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    return db.query(RoleSkill).filter(
        RoleSkill.role_id == role_id
    ).all()