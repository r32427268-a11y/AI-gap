from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import User, Project

from services.github_analyzer import (
    analyze_github_profile
)


router = APIRouter()


# ============================================================
# GET GITHUB PROFILE
# ============================================================

@router.get("/{username}")
def github_profile(username: str):

    if not username.strip():
        raise HTTPException(
            status_code=400,
            detail="GitHub username is required"
        )

    try:

        result = analyze_github_profile(
            username
        )

        return result

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"GitHub analysis failed: {str(e)}"
        )


# ============================================================
# IMPORT GITHUB PROJECTS INTO USER PROFILE
# ============================================================

@router.post("/import/{user_id}/{username}")
def import_github_projects(
    user_id: int,
    username: str,
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
    # Get GitHub repositories
    # --------------------------------------------------------

    try:

        github_data = analyze_github_profile(
            username
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"GitHub analysis failed: {str(e)}"
        )

    # --------------------------------------------------------
    # Import repositories
    # --------------------------------------------------------

    imported_projects = []
    existing_projects = []

    for repo in github_data["projects"]:

        project_name = repo.get("name")

        if not project_name:
            continue

        # Check whether project already exists
        existing_project = db.query(Project).filter(
            Project.user_id == user_id,
            Project.name == project_name
        ).first()

        if existing_project:

            existing_projects.append(
                project_name
            )

            continue

        # Create project description
        description = repo.get(
            "description"
        )

        # Add GitHub URL to description
        github_url = repo.get(
            "url"
        )

        if github_url:

            if description:

                description = (
                    f"{description}\n"
                    f"GitHub: {github_url}"
                )

            else:

                description = (
                    f"GitHub: {github_url}"
                )

        # Create project
        new_project = Project(
            user_id=user_id,
            name=project_name,
            description=description,
            technologies=repo.get(
                "language"
            )
        )

        db.add(new_project)

        imported_projects.append(
            project_name
        )

    # --------------------------------------------------------
    # Save database changes
    # --------------------------------------------------------

    db.commit()

    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------

    return {

        "message": "GitHub projects imported successfully.",

        "user_id": user_id,

        "github_username": username,

        "total_github_projects": github_data[
            "total_repositories"
        ],

        "imported_projects": imported_projects,

        "already_existing": existing_projects,

        "total_imported": len(
            imported_projects
        )
    }