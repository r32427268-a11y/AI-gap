"""
skill_extractor.py
-------------------
Turns whatever the user gives us (a list of skills, and/or raw resume/profile
text) into a clean, normalized set of skill strings we can match against a
target role.

Kept deliberately simple (keyword + synonym matching, no heavy NLP) because:
- it's explainable, debuggable, and fast to build for a hackathon
- it doesn't need a trained model or GPU
- it's easy to extend later with spaCy/NER if there's time left
"""

import json
import re
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "roles_skills.json"


def _load_knowledge_base():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


_KB = _load_knowledge_base()
SYNONYMS = _KB.get("synonyms", {})

# Build the master list of every skill mentioned across every role.
# This is what we scan resume text against.
MASTER_SKILLS = set()
for role_data in _KB["roles"].values():
    MASTER_SKILLS.update(role_data.get("core_skills", {}).keys())
    MASTER_SKILLS.update(role_data.get("nice_to_have_skills", {}).keys())


def normalize_skill(raw_skill: str) -> str:
    """Lowercase, strip whitespace, and map known synonyms to a canonical name."""
    if not raw_skill:
        return ""
    cleaned = raw_skill.strip().lower()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return SYNONYMS.get(cleaned, cleaned)


def extract_skills_from_text(text: str) -> set:
    """
    Scan free-text (e.g. a pasted resume or 'about me' blurb) for any skill
    that appears in MASTER_SKILLS or SYNONYMS. Uses word-boundary matching so
    'r' doesn't match inside 'react', etc.
    """
    if not text:
        return set()

    normalized_text = " " + re.sub(r"\s+", " ", text.lower()) + " "
    found = set()

    # Check multi-word skills first (e.g. "machine learning"), then single words.
    all_known_terms = set(MASTER_SKILLS) | set(SYNONYMS.keys())
    for term in all_known_terms:
        pattern = r"(?<![a-z0-9+#])" + re.escape(term) + r"(?![a-z0-9+#])"
        if re.search(pattern, normalized_text):
            found.add(normalize_skill(term))

    return found


def get_user_skills(user_profile: dict) -> set:
    """
    Accepts a user_profile dict shaped like:
    {
        "skills": ["Python", "React", ...],   # optional, structured input
        "resume_text": "Third year CS student with experience in..."  # optional
    }
    Returns a normalized set of skills combining both sources.
    """
    skills = set()

    for raw_skill in user_profile.get("skills", []) or []:
        normalized = normalize_skill(raw_skill)
        if normalized:
            skills.add(normalized)

    resume_text = user_profile.get("resume_text", "")
    skills |= extract_skills_from_text(resume_text)

    return skills


def list_available_roles() -> list:
    return list(_KB["roles"].keys())
