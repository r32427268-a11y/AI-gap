from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
import requests

from database.database import get_db
from database.models import (
    User,
    Role,
    Skill,
    UserSkill,
    Analysis
)
from database.schemas import AnalysisCreate, AnalysisResponse

router = APIRouter()

AI_SERVICE_URL = "http://127.0.0.1:5001"


@router.post("/")
def create_analysis(
    analysis_data: AnalysisCreate,
    db: Session = Depends(get_db)
):
    # ---------------------------------------------------------
    # 1. Check user
    # ---------------------------------------------------------
    user = db.query(User).filter(
        User.id == analysis_data.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # ---------------------------------------------------------
    # 2. Check role
    # ---------------------------------------------------------
    role = db.query(Role).filter(
        Role.id == analysis_data.role_id
    ).first()

    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    # ---------------------------------------------------------
    # 3. Get user's skills from database
    # ---------------------------------------------------------
    user_skills = (
        db.query(UserSkill)
        .filter(UserSkill.user_id == analysis_data.user_id)
        .all()
    )

    skill_ids = [
        user_skill.skill_id
        for user_skill in user_skills
    ]

    skills = (
        db.query(Skill)
        .filter(Skill.id.in_(skill_ids))
        .all()
        if skill_ids
        else []
    )

    skill_names = [
        skill.name
        for skill in skills
    ]

    # ---------------------------------------------------------
    # 4. Send user profile + role to Person 3 AI service
    # ---------------------------------------------------------
    ai_request = {
        "user_profile": {
            "skills": skill_names
        },
        "target_role": role.name
    }

    try:
        ai_response = requests.post(
            f"{AI_SERVICE_URL}/analyze",
            json=ai_request,
            timeout=30
        )

    except requests.RequestException as e:
        raise HTTPException(
            status_code=503,
            detail=f"AI service is unavailable: {str(e)}"
        )

    # ---------------------------------------------------------
    # 5. Handle AI service errors
    # ---------------------------------------------------------
    if ai_response.status_code != 200:
        try:
            error_data = ai_response.json()
        except Exception:
            error_data = {
                "error": ai_response.text
            }

        raise HTTPException(
            status_code=ai_response.status_code,
            detail=error_data
        )

    try:
        ai_result = ai_response.json()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Invalid response received from AI service"
        )

    # ---------------------------------------------------------
    # 6. Save analysis in database
    # ---------------------------------------------------------
    analysis = Analysis(
        user_id=analysis_data.user_id,
        role_id=analysis_data.role_id,
        readiness_score=ai_result.get(
            "readiness_score",
            0
        ),
        matched_skills=json.dumps(
            ai_result.get("matched_skills", [])
        ),
        missing_skills=json.dumps(
            ai_result.get("missing_skills", [])
        ),
        recommendations=json.dumps(
            ai_result.get("recommendations", [])
        )
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    # ---------------------------------------------------------
    # 7. Return combined backend + AI response
    # ---------------------------------------------------------
    return {
        "id": analysis.id,
        "user_id": analysis.user_id,
        "role_id": analysis.role_id,
        "target_role": ai_result.get(
            "target_role",
            role.name
        ),
        "readiness_score": ai_result.get(
            "readiness_score",
            0
        ),
        "matched_skills": ai_result.get(
            "matched_skills",
            []
        ),
        "missing_skills": ai_result.get(
            "missing_skills",
            []
        ),
        "priority_skills": ai_result.get(
            "priority_skills",
            []
        ),
        "recommendations": ai_result.get(
            "recommendations",
            []
        ),
        "roadmap": ai_result.get(
            "roadmap",
            []
        ),
        "ai_summary": ai_result.get(
            "ai_summary",
            ""
        )
    }


@router.get(
    "/user/{user_id}",
    response_model=list[AnalysisResponse]
)
def get_user_analyses(
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

    analyses = (
        db.query(Analysis)
        .filter(Analysis.user_id == user_id)
        .order_by(Analysis.created_at.desc())
        .all()
    )

    result = []

    for analysis in analyses:
        result.append({
            "id": analysis.id,
            "user_id": analysis.user_id,
            "role_id": analysis.role_id,
            "readiness_score": analysis.readiness_score,
            "matched_skills": json.loads(
                analysis.matched_skills or "[]"
            ),
            "missing_skills": json.loads(
                analysis.missing_skills or "[]"
            ),
            "recommendations": json.loads(
                analysis.recommendations or "[]"
            )
        })

    return result


@router.get(
    "/{analysis_id}",
    response_model=AnalysisResponse
)
def get_analysis(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id
    ).first()

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found"
        )

    return {
        "id": analysis.id,
        "user_id": analysis.user_id,
        "role_id": analysis.role_id,
        "readiness_score": analysis.readiness_score,
        "matched_skills": json.loads(
            analysis.matched_skills or "[]"
        ),
        "missing_skills": json.loads(
            analysis.missing_skills or "[]"
        ),
        "recommendations": json.loads(
            analysis.recommendations or "[]"
        )
    }