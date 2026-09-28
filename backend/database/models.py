from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    education = Column(String(200))
    experience_level = Column(String(50))

    skills = relationship("UserSkill", back_populates="user")
    projects = relationship("Project", back_populates="user")
    analyses = relationship("Analysis", back_populates="user")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)

    analyses = relationship("Analysis", back_populates="role")
    skills = relationship("RoleSkill", back_populates="role")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(100))

    users = relationship("UserSkill", back_populates="skill")
    roles = relationship("RoleSkill", back_populates="skill")


class UserSkill(Base):
    __tablename__ = "user_skills"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))

    proficiency = Column(Float, default=0.0)

    user = relationship("User", back_populates="skills")
    skill = relationship("Skill", back_populates="users")


class RoleSkill(Base):
    __tablename__ = "role_skills"

    id = Column(Integer, primary_key=True, index=True)

    role_id = Column(Integer, ForeignKey("roles.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))

    importance = Column(Float, default=1.0)

    role = relationship("Role", back_populates="skills")
    skill = relationship("Skill", back_populates="roles")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(150), nullable=False)
    description = Column(Text)
    technologies = Column(Text)

    user = relationship("User", back_populates="projects")


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))

    readiness_score = Column(Float)

    matched_skills = Column(Text)
    missing_skills = Column(Text)
    recommendations = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="analyses")
    role = relationship("Role", back_populates="analyses")