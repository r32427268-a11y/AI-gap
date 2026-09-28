from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

import os
import shutil
import tempfile

from database.database import get_db
from database.models import User, Skill, UserSkill

from services.resume_parser import parse_resume
from services.skill_extractor import extract_skill_names


router = APIRouter()


# ============================================================
# UPLOAD AND PARSE RESUME
# ============================================================

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...)
):

    allowed_extensions = [".pdf", ".docx"]

    file_extension = os.path.splitext(
        file.filename
    )[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX resume files are supported."
        )

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=file_extension
    )

    temp_file_path = temp_file.name
    temp_file.close()

    try:

        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        resume_text = parse_resume(
            temp_file_path
        )

        if not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the resume."
            )

        return {
            "filename": file.filename,
            "message": "Resume uploaded and parsed successfully.",
            "text": resume_text
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Resume parsing failed: {str(e)}"
        )

    finally:

        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


# ============================================================
# RESUME → SKILL EXTRACTION
# ============================================================

@router.post("/analyze/{user_id}")
async def analyze_resume(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # Check user
    # --------------------------------------------------------

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # --------------------------------------------------------
    # Check file type
    # --------------------------------------------------------

    allowed_extensions = [".pdf", ".docx"]

    file_extension = os.path.splitext(
        file.filename
    )[1].lower()

    if file_extension not in allowed_extensions:

        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX resume files are supported."
        )

    # --------------------------------------------------------
    # Temporary file
    # --------------------------------------------------------

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=file_extension
    )

    temp_file_path = temp_file.name
    temp_file.close()

    try:

        # ----------------------------------------------------
        # Save uploaded resume
        # ----------------------------------------------------

        with open(temp_file_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        # ----------------------------------------------------
        # Extract resume text
        # ----------------------------------------------------

        resume_text = parse_resume(
            temp_file_path
        )

        if not resume_text.strip():

            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the resume."
            )

        # ----------------------------------------------------
        # Get skills from database
        # ----------------------------------------------------

        database_skills = db.query(
            Skill
        ).all()

        skill_names = [
            skill.name
            for skill in database_skills
        ]

        # ----------------------------------------------------
        # Extract matching skills
        # ----------------------------------------------------

        detected_skill_names = extract_skill_names(
            resume_text,
            skill_names
        )

        detected_skills = []

        added_skills = []

        already_existing_skills = []

        # ----------------------------------------------------
        # Process detected skills
        # ----------------------------------------------------

        for skill_name in detected_skill_names:

            skill = db.query(
                Skill
            ).filter(
                Skill.name == skill_name
            ).first()

            if not skill:
                continue

            detected_skills.append({
                "skill_id": skill.id,
                "skill": skill.name,
                "category": skill.category
            })

            # ------------------------------------------------
            # Check existing user skill
            # ------------------------------------------------

            existing_user_skill = db.query(
                UserSkill
            ).filter(
                UserSkill.user_id == user_id,
                UserSkill.skill_id == skill.id
            ).first()

            if existing_user_skill:

                already_existing_skills.append(
                    skill.name
                )

            else:

                new_user_skill = UserSkill(
                    user_id=user_id,
                    skill_id=skill.id,
                    proficiency=0.0
                )

                db.add(
                    new_user_skill
                )

                added_skills.append(
                    skill.name
                )

        # ----------------------------------------------------
        # Save database changes
        # ----------------------------------------------------

        db.commit()

        # ----------------------------------------------------
        # Return result
        # ----------------------------------------------------

        return {

            "filename": file.filename,

            "message": "Resume analyzed successfully.",

            "user_id": user_id,

            "detected_skills": detected_skills,

            "added_to_profile": added_skills,

            "already_existing": already_existing_skills,

            "total_detected": len(
                detected_skills
            ),

            "resume_text": resume_text
        }

    except HTTPException:

        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Resume analysis failed: {str(e)}"
        )

    finally:

        if os.path.exists(temp_file_path):

            os.remove(temp_file_path)