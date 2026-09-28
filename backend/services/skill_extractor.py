import re


# ============================================================
# SKILL ALIASES
# ============================================================

SKILL_ALIASES = {
    "python": ["python", "python programming"],
    "machine learning": [
        "machine learning",
        "machine-learning",
        "ml"
    ],
    "deep learning": [
        "deep learning",
        "deep-learning",
        "dl"
    ],
    "javascript": [
        "javascript",
        "java script",
        "js"
    ],
    "typescript": [
        "typescript",
        "ts"
    ],
    "react": [
        "react",
        "reactjs",
        "react.js"
    ],
    "fastapi": [
        "fastapi",
        "fast api"
    ],
    "sql": [
        "sql",
        "structured query language"
    ],
    "mongodb": [
        "mongodb",
        "mongo db"
    ],
    "mysql": [
        "mysql",
        "my sql"
    ],
    "git": [
        "git",
        "git version control"
    ],
    "github": [
        "github",
        "git hub"
    ],
    "html": [
        "html",
        "html5"
    ],
    "css": [
        "css",
        "css3"
    ],
    "pandas": [
        "pandas"
    ],
    "numpy": [
        "numpy"
    ],
    "scikit-learn": [
        "scikit-learn",
        "scikit learn",
        "sklearn"
    ],
    "tensorflow": [
        "tensorflow",
        "tensor flow"
    ],
    "pytorch": [
        "pytorch",
        "py torch"
    ],
    "computer vision": [
        "computer vision",
        "computer-vision",
        "cv"
    ],
    "generative ai": [
        "generative ai",
        "generative artificial intelligence",
        "gen ai"
    ]
}


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text: str) -> str:
    """
    Normalize resume text before skill matching.
    """

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# EXTRACT SKILL NAMES
# ============================================================

def extract_skill_names(
    resume_text: str,
    database_skill_names: list[str]
) -> list[str]:
    """
    Match database skills against resume text
    using common aliases.
    """

    normalized_text = normalize_text(
        resume_text
    )

    detected_skills = []

    for skill_name in database_skill_names:

        canonical_name = skill_name.strip()

        if not canonical_name:
            continue

        aliases = SKILL_ALIASES.get(
            canonical_name.lower(),
            [canonical_name.lower()]
        )

        found = False

        for alias in aliases:

            pattern = r"(?<!\w)" + re.escape(alias) + r"(?!\w)"

            if re.search(
                pattern,
                normalized_text
            ):
                found = True
                break

        if found:

            detected_skills.append(
                canonical_name
            )

    return detected_skills