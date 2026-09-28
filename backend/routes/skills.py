from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import Skill, User, UserSkill
from database.schemas import (
    SkillCreate,
    SkillResponse,
    UserSkillCreate,
    UserSkillResponse
)

router = APIRouter()


@router.post("/", response_model=SkillResponse)
def create_skill(
    skill: SkillCreate,
    db: Session = Depends(get_db)
):
    existing_skill = db.query(Skill).filter(
        Skill.name == skill.name
    ).first()

    if existing_skill:
        raise HTTPException(
            status_code=400,
            detail="Skill already exists"
        )

    new_skill = Skill(
        name=skill.name,
        category=skill.category
    )

    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)

    return new_skill


@router.get("/", response_model=list[SkillResponse])
def get_skills(
    db: Session = Depends(get_db)
):
    return db.query(Skill).all()


# IMPORTANT: user routes come BEFORE /{skill_id}

@router.post(
    "/user/{user_id}",
    response_model=UserSkillResponse
)
def add_user_skill(
    user_id: int,
    skill_data: UserSkillCreate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    skill = db.query(Skill).filter(
        Skill.id == skill_data.skill_id
    ).first()

    if not skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    existing = db.query(UserSkill).filter(
        UserSkill.user_id == user_id,
        UserSkill.skill_id == skill_data.skill_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="User already has this skill"
        )

    user_skill = UserSkill(
        user_id=user_id,
        skill_id=skill_data.skill_id,
        proficiency=skill_data.proficiency
    )

    db.add(user_skill)
    db.commit()
    db.refresh(user_skill)

    return user_skill


@router.get(
    "/user/{user_id}",
    response_model=list[UserSkillResponse]
)
def get_user_skills(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return db.query(UserSkill).filter(
        UserSkill.user_id == user_id
    ).all()


# Keep this LAST
@router.get("/{skill_id}", response_model=SkillResponse)
def get_skill(
    skill_id: int,
    db: Session = Depends(get_db)
):
    skill = db.query(Skill).filter(
        Skill.id == skill_id
    ).first()

    if not skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    return skill