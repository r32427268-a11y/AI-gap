# AI Career Gap Navigator — Backend API Documentation

Base URL:

http://127.0.0.1:8000

Swagger Documentation:

http://127.0.0.1:8000/docs


# 1. PROFILE APIs

## Create Profile

POST /api/profile/

Request:

{
  "name": "Khushi Saxena",
  "email": "khushi@example.com",
  "education": "B.Tech CSE AI/ML",
  "experience_level": "Student"
}

Response:

{
  "id": 2,
  "name": "Khushi Saxena",
  "email": "khushi@example.com",
  "education": "B.Tech CSE AI/ML",
  "experience_level": "Student"
}


## Get Profile

GET /api/profile/{user_id}

Example:

GET /api/profile/2


## Update Profile

PUT /api/profile/{user_id}

Request:

{
  "name": "Khushi Saxena",
  "email": "khushi@example.com",
  "education": "B.Tech CSE AI/ML",
  "experience_level": "Student"
}


## Delete Profile

DELETE /api/profile/{user_id}


# 2. SKILLS APIs

## Create Skill

POST /api/skills/

Request:

{
  "name": "Python",
  "category": "Programming"
}


## Get All Skills

GET /api/skills/


## Get Single Skill

GET /api/skills/{skill_id}


## Add Skill to User

POST /api/skills/user/{user_id}

Request:

{
  "skill_id": 1,
  "proficiency": 85
}


## Get User Skills

GET /api/skills/user/{user_id}


# 3. PROJECT APIs

## Create Project

POST /api/projects/

Request:

{
  "user_id": 2,
  "name": "College InfoBot",
  "description": "College information chatbot",
  "technologies": "Python, Streamlit"
}


## Get User Projects

GET /api/projects/user/{user_id}


## Get Project

GET /api/projects/{project_id}


## Update Project

PUT /api/projects/{project_id}

Request:

{
  "user_id": 2,
  "name": "College InfoBot",
  "description": "Updated description",
  "technologies": "Python, Streamlit, FastAPI"
}


## Delete Project

DELETE /api/projects/{project_id}


# 4. ROLE APIs

## Create Career Role

POST /api/roles/

Request:

{
  "name": "AI Engineer",
  "description": "Develops and deploys AI and ML systems."
}


## Get All Roles

GET /api/roles/


## Add Required Skill to Role

POST /api/roles/{role_id}/skills

Request:

{
  "skill_id": 2,
  "importance": 1.0
}


## Get Role Skills

GET /api/roles/{role_id}/skills


# 5. RESUME APIs

## Upload and Parse Resume

POST /api/resume/upload

Content-Type:

multipart/form-data

Form field:

file

Supported formats:

PDF
DOCX

Response:

{
  "filename": "resume.pdf",
  "message": "Resume uploaded and parsed successfully.",
  "text": "Extracted resume text..."
}


## Analyze Resume

POST /api/resume/analyze/{user_id}

Content-Type:

multipart/form-data

Form field:

file

Example:

POST /api/resume/analyze/2

This endpoint:

1. Extracts resume text.
2. Detects known skills.
3. Checks the user's existing skills.
4. Adds newly detected skills to user_skills.
5. Returns detected and newly added skills.


# 6. GITHUB APIs

## Get GitHub Profile

GET /api/github/{username}

Example:

GET /api/github/octocat

Returns:

- GitHub username
- Repository count
- Repository information
- Primary programming languages


## Import GitHub Projects

POST /api/github/import/{user_id}/{username}

Example:

POST /api/github/import/2/octocat

This endpoint:

1. Fetches public GitHub repositories.
2. Filters out forked repositories.
3. Creates project records.
4. Associates projects with the user.
5. Avoids duplicate projects.


# 7. CAREER GAP ANALYSIS

## Create Analysis

POST /api/analysis/

Request:

{
  "user_id": 2,
  "role_id": 1
}

Response:

{
  "id": 1,
  "user_id": 2,
  "role_id": 1,
  "readiness_score": 50.0,
  "matched_skills": [
    {
      "skill_id": 1,
      "skill": "Python",
      "proficiency": 85
    }
  ],
  "missing_skills": [
    {
      "skill_id": 2,
      "skill": "Machine Learning",
      "importance": 1.0
    }
  ],
  "recommendations": [
    "Develop Machine Learning"
  ]
}


## Get User Analysis History

GET /api/analysis/user/{user_id}

Example:

GET /api/analysis/user/2


## Get Single Analysis

GET /api/analysis/{analysis_id}

Example:

GET /api/analysis/1


# 8. RECOMMENDED FRONTEND FLOW

The frontend should follow this sequence:

1. Create/Get User Profile

        ↓

2. Upload Resume

        ↓

3. Analyze Resume

        ↓

4. Detect User Skills

        ↓

5. Import GitHub Projects (optional)

        ↓

6. Select Career Role

        ↓

7. Run Career Gap Analysis

        ↓

8. Display Readiness Score

        ↓

9. Display Matched Skills

        ↓

10. Display Missing Skills

        ↓

11. Display Recommendations


# 9. ERROR RESPONSES

Typical errors use this format:

{
  "detail": "User not found"
}


Common HTTP status codes:

200 — Successful request

400 — Invalid request / duplicate data

404 — Resource not found

422 — Validation error

500 — Server-side error


# 10. SWAGGER

Interactive API documentation:

http://127.0.0.1:8000/docs