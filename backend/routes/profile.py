from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import User
from database.schemas import ProfileCreate, ProfileResponse


router = APIRouter()


@router.post("/", response_model=ProfileResponse)
def create_profile(
    profile: ProfileCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.email == profile.email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="A profile with this email already exists"
        )

    new_user = User(
        name=profile.name,
        email=profile.email,
        education=profile.education,
        experience_level=profile.experience_level
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{user_id}", response_model=ProfileResponse)
def get_profile(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    return user


@router.put("/{user_id}", response_model=ProfileResponse)
def update_profile(
    user_id: int,
    profile: ProfileCreate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    user.name = profile.name
    user.email = profile.email
    user.education = profile.education
    user.experience_level = profile.experience_level

    db.commit()
    db.refresh(user)

    return user


@router.delete("/{user_id}")
def delete_profile(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "Profile deleted successfully"
    }