"""
skill_matcher.py
-----------------
Compares a user's skill set against a target role's requirements.
Produces matched skills, missing skills, a weighted readiness score,
and a prioritized list of gaps (High / Medium / Low).
"""

import json
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "roles_skills.json"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    _KB = json.load(f)


class RoleNotFoundError(Exception):
    pass


def _get_role_data(role_name: str) -> dict:
    """Case-insensitive role lookup."""
    for name, data in _KB["roles"].items():
        if name.lower() == role_name.strip().lower():
            return data
    available = ", ".join(_KB["roles"].keys())
    raise RoleNotFoundError(
        f"Role '{role_name}' not found. Available roles: {available}"
    )


def match_skills(user_skills: set, target_role: str) -> dict:
    """
    Returns:
    {
        "matched": {skill: weight, ...},
        "missing": {skill: weight, ...},
        "readiness_score": float (0-100, weighted by skill importance)
    }
    """
    role_data = _get_role_data(target_role)
    all_role_skills = {**role_data.get("core_skills", {}), **role_data.get("nice_to_have_skills", {})}

    matched = {}
    missing = {}

    for skill, weight in all_role_skills.items():
        if skill in user_skills:
            matched[skill] = weight
        else:
            missing[skill] = weight

    total_weight = sum(all_role_skills.values()) or 1
    matched_weight = sum(matched.values())
    readiness_score = round((matched_weight / total_weight) * 100, 1)

    return {
        "matched": matched,
        "missing": missing,
        "readiness_score": readiness_score,
    }


def prioritize_gaps(missing_skills: dict) -> list:
    """
    Turns {skill: weight} into a sorted, labeled priority list:
    [{"skill": "sql", "weight": 4, "priority": "High"}, ...]
    Weight scale: 5 = critical/core, 3-4 = important, 1-2 = nice to have.
    """
    def label(weight):
        if weight >= 4:
            return "High"
        elif weight >= 2:
            return "Medium"
        return "Low"

    prioritized = [
        {"skill": skill, "weight": weight, "priority": label(weight)}
        for skill, weight in missing_skills.items()
    ]
    prioritized.sort(key=lambda x: x["weight"], reverse=True)
    return prioritized

