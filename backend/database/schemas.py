from pydantic import BaseModel
from typing import Optional


# ============================================================
# PROFILE SCHEMAS
# ============================================================

class ProfileCreate(BaseModel):
    name: str
    email: str
    education: Optional[str] = None
    experience_level: Optional[str] = None


class ProfileResponse(BaseModel):
    id: int
    name: str
    email: str
    education: Optional[str] = None
    experience_level: Optional[str] = None

    class Config:
        from_attributes = True


# ============================================================
# SKILL SCHEMAS
# ============================================================

class SkillCreate(BaseModel):
    name: str
    category: Optional[str] = None


class SkillResponse(BaseModel):
    id: int
    name: str
    category: Optional[str] = None

    class Config:
        from_attributes = True


# ============================================================
# USER SKILL SCHEMAS
# ============================================================

class UserSkillCreate(BaseModel):
    skill_id: int
    proficiency: float = 0.0


class UserSkillResponse(BaseModel):
    id: int
    user_id: int
    skill_id: int
    proficiency: float

    class Config:
        from_attributes = True


# ============================================================
# PROJECT SCHEMAS
# ============================================================

class ProjectCreate(BaseModel):
    user_id: int
    name: str
    description: Optional[str] = None
    technologies: Optional[str] = None


class ProjectResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: Optional[str] = None
    technologies: Optional[str] = None

    class Config:
        from_attributes = True


# ============================================================
# ROLE SCHEMAS
# ============================================================

class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None


class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


# ============================================================
# ROLE SKILL SCHEMAS
# ============================================================

class RoleSkillCreate(BaseModel):
    skill_id: int
    importance: float = 1.0


class RoleSkillResponse(BaseModel):
    id: int
    role_id: int
    skill_id: int
    importance: float

    class Config:
        from_attributes = True


# ============================================================
# ANALYSIS SCHEMAS
# ============================================================

class AnalysisCreate(BaseModel):
    user_id: int
    role_id: int


class AnalysisResponse(BaseModel):
    id: int
    user_id: int
    role_id: int
    readiness_score: float
    matched_skills: list
    missing_skills: list
    recommendations: list

    class Config:
        from_attributes = True