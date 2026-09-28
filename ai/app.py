"""
app.py
-------
The API Person 3 hands to the backend team. Run standalone during
development (python app.py), or the backend team can call this service
directly, or import analyze_profile() as a function if you end up merging
this into a single Flask backend instead of running it separately.

Endpoints:
  POST /analyze   -> full skill-gap analysis for a user_profile + target_role
  GET  /roles     -> list of supported target roles (for the frontend dropdown)
  GET  /health    -> simple liveness check
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

from skill_extractor import get_user_skills, list_available_roles
from skill_matcher import match_skills, prioritize_gaps, RoleNotFoundError
from recommender import get_recommendations, generate_roadmap, generate_ai_narrative

app = Flask(__name__)
CORS(app)  # allow the React frontend (different port) to call this API


def analyze_profile(user_profile: dict, target_role: str) -> dict:
    """
    Core function — kept separate from the Flask route so it can also be
    imported and called directly by the backend team without going over HTTP.
    """
    user_skills = get_user_skills(user_profile)
    analysis = match_skills(user_skills, target_role)
    prioritized = prioritize_gaps(analysis["missing"])
    recommendations = get_recommendations(prioritized)
    roadmap = generate_roadmap(prioritized)
    narrative = generate_ai_narrative(user_profile, target_role, analysis)

    return {
        "target_role": target_role,
        "readiness_score": analysis["readiness_score"],
        "matched_skills": sorted(analysis["matched"].keys()),
        "missing_skills": sorted(analysis["missing"].keys()),
        "priority_skills": prioritized,
        "recommendations": recommendations,
        "roadmap": roadmap,
        "ai_summary": narrative,
    }


@app.route("/analyze", methods=["POST"])
def analyze():
    body = request.get_json(silent=True) or {}
    user_profile = body.get("user_profile")
    target_role = body.get("target_role")

    if not user_profile or not target_role:
        return jsonify({"error": "Both 'user_profile' and 'target_role' are required."}), 400

    try:
        result = analyze_profile(user_profile, target_role)
        return jsonify(result), 200
    except RoleNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@app.route("/roles", methods=["GET"])
def roles():
    return jsonify({"roles": list_available_roles()}), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    # Runs on http://localhost:5001 by default so it doesn't clash with a
    # main backend that's likely already using port 5000.
    app.run(debug=True, port=5001)

