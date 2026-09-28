def analyze_career_gap(user_skills, role_skills, skill_map):
    """
    Compare user's skills with the skills required for a role.
    """

    user_skill_map = {
        item.skill_id: item.proficiency
        for item in user_skills
    }

    matched_skills = []
    missing_skills = []

    total_importance = 0
    achieved_importance = 0

    for role_skill in role_skills:

        importance = role_skill.importance or 1.0
        total_importance += importance

        skill_name = skill_map.get(
            role_skill.skill_id,
            f"Skill {role_skill.skill_id}"
        )

        if role_skill.skill_id in user_skill_map:

            proficiency = user_skill_map[role_skill.skill_id]

            matched_skills.append({
                "skill_id": role_skill.skill_id,
                "skill": skill_name,
                "proficiency": proficiency
            })

            achieved_importance += (
                importance * min(proficiency, 100) / 100
            )

        else:

            missing_skills.append({
                "skill_id": role_skill.skill_id,
                "skill": skill_name,
                "importance": importance
            })

    if total_importance > 0:
        readiness_score = (
            achieved_importance / total_importance
        ) * 100
    else:
        readiness_score = 0

    recommendations = []

    for skill in missing_skills:
        recommendations.append(
            f"Develop {skill['skill']}"
        )

    return {
        "readiness_score": round(readiness_score, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommendations": recommendations
    }