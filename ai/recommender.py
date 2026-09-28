"""
recommender.py
----------------
Turns prioritized skill gaps into:
  1. Concrete learning resources per skill (rule-based, always works)
  2. A phased learning roadmap (rule-based, always works)
  3. An optional AI-generated narrative summary (LLM, nice-to-have)

IMPORTANT for demo day: steps 1 and 2 never depend on network/API access.
Step 3 is wrapped in a try/except and silently falls back to a rule-based
summary if the LLM call fails or no API key is configured. Never let the
AI layer be a single point of failure during a live demo.
"""

import os

# --- 1. Curated learning resources -----------------------------------------
# Beginner-friendly, free-first resources. Extend this as time allows.
LEARNING_RESOURCES = {
    "python": [{"title": "Python for Everybody", "url": "https://www.py4e.com/", "platform": "Free course"}],
    "sql": [{"title": "SQL Tutorial", "url": "https://www.w3schools.com/sql/", "platform": "W3Schools"}],
    "machine learning": [{"title": "Machine Learning Specialization", "url": "https://www.coursera.org/specializations/machine-learning-introduction", "platform": "Coursera (Andrew Ng)"}],
    "deep learning": [{"title": "Deep Learning Specialization", "url": "https://www.coursera.org/specializations/deep-learning", "platform": "Coursera"}],
    "tensorflow": [{"title": "TensorFlow Core Tutorials", "url": "https://www.tensorflow.org/tutorials", "platform": "TensorFlow.org"}],
    "pytorch": [{"title": "PyTorch Basics", "url": "https://pytorch.org/tutorials/beginner/basics/intro.html", "platform": "PyTorch.org"}],
    "react": [{"title": "React Official Docs (Learn)", "url": "https://react.dev/learn", "platform": "react.dev"}],
    "javascript": [{"title": "JavaScript.info", "url": "https://javascript.info/", "platform": "Free"}],
    "docker": [{"title": "Docker Get Started", "url": "https://docs.docker.com/get-started/", "platform": "Docker Docs"}],
    "aws": [{"title": "AWS Cloud Practitioner Essentials", "url": "https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/", "platform": "AWS Training"}],
    "flask": [{"title": "Flask Quickstart", "url": "https://flask.palletsprojects.com/en/latest/quickstart/", "platform": "Flask Docs"}],
    "fastapi": [{"title": "FastAPI Tutorial", "url": "https://fastapi.tiangolo.com/tutorial/", "platform": "FastAPI Docs"}],
    "git": [{"title": "Git Handbook", "url": "https://guides.github.com/introduction/git-handbook/", "platform": "GitHub Guides"}],
    "llm": [{"title": "Prompt Engineering Guide", "url": "https://www.promptingguide.ai/", "platform": "Free"}],
    "rag": [{"title": "RAG from Scratch", "url": "https://python.langchain.com/docs/tutorials/rag/", "platform": "LangChain Docs"}],
    "vector database": [{"title": "Vector Databases Explained", "url": "https://www.pinecone.io/learn/vector-database/", "platform": "Pinecone Learn"}],
}


def _resource_for(skill: str) -> list:
    if skill in LEARNING_RESOURCES:
        return LEARNING_RESOURCES[skill]
    # Fallback so every skill still returns something actionable.
    query = skill.replace(" ", "+")
    return [{"title": f"Search: learn {skill}", "url": f"https://www.google.com/search?q=learn+{query}", "platform": "Web search"}]


def get_recommendations(prioritized_gaps: list) -> list:
    """
    Input: output of skill_matcher.prioritize_gaps()
    Output: [{"skill", "priority", "resources": [...]}, ...]
    """
    return [
        {
            "skill": gap["skill"],
            "priority": gap["priority"],
            "resources": _resource_for(gap["skill"]),
        }
        for gap in prioritized_gaps
    ]


# --- 2. Phased roadmap -------------------------------------------------------
def generate_roadmap(prioritized_gaps: list) -> list:
    """
    Groups gaps into phases by priority. Returns a simple, presentable roadmap:
    [{"phase": "Weeks 1-3", "focus": "High priority", "skills": [...]}, ...]
    """
    high = [g["skill"] for g in prioritized_gaps if g["priority"] == "High"]
    medium = [g["skill"] for g in prioritized_gaps if g["priority"] == "Medium"]
    low = [g["skill"] for g in prioritized_gaps if g["priority"] == "Low"]

    roadmap = []
    if high:
        roadmap.append({"phase": "Weeks 1-3", "focus": "Core gaps (High priority)", "skills": high})
    if medium:
        roadmap.append({"phase": "Weeks 4-6", "focus": "Important gaps (Medium priority)", "skills": medium})
    if low:
        roadmap.append({"phase": "Weeks 7-8", "focus": "Nice-to-have polish (Low priority)", "skills": low})
    if not roadmap:
        roadmap.append({"phase": "Ongoing", "focus": "Maintain & deepen current skills", "skills": []})
    return roadmap


# --- 3. Optional AI narrative layer ------------------------------------------
def generate_ai_narrative(user_profile: dict, target_role: str, analysis: dict) -> str:
    """
    Uses an LLM to turn the structured analysis into a short, personalized
    paragraph of advice. Returns a rule-based fallback string if no API key
    is set or the call fails for any reason (network, quota, etc.) so the
    rest of the app is completely unaffected.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return _fallback_narrative(target_role, analysis)

    try:
        import anthropic  # pip install anthropic

        client = anthropic.Anthropic(api_key=api_key)
        missing_list = ", ".join(analysis["missing"].keys()) or "none"
        matched_list = ", ".join(analysis["matched"].keys()) or "none"

        prompt = (
            f"A student is targeting the role '{target_role}'. "
            f"They already have these skills: {matched_list}. "
            f"They are missing: {missing_list}. "
            f"Their current readiness score is {analysis['readiness_score']}%. "
            "In under 80 words, write an encouraging, specific, and practical "
            "paragraph of career advice for them. No markdown, plain text only."
        )

        response = client.messages.create(
            model=os.environ.get("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001"),
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text.strip()

    except Exception:
        # Never let an LLM/network hiccup break the API response during a demo.
        return _fallback_narrative(target_role, analysis)


def _fallback_narrative(target_role: str, analysis: dict) -> str:
    score = analysis["readiness_score"]
    missing_count = len(analysis["missing"])
    if score >= 80:
        tone = "You're in strong shape"
    elif score >= 50:
        tone = "You're making solid progress"
    else:
        tone = "You're at the early stages, and that's fine"
    return (
        f"{tone} for the {target_role} role, with a readiness score of {score}%. "
        f"Focus on the {missing_count} skill gap(s) below, starting with the "
        "highest-priority ones, to steadily close the gap."
    )


