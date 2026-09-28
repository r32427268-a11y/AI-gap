# AI / Career Intelligence Module

This is Person 3's part of **AI Career Gap Navigator**: skill extraction,
skill matching, gap prioritization, recommendations, and roadmap generation.

## Files

| File                     | Responsibility                                                                            |
| ------------------------ | ----------------------------------------------------------------------------------------- |
| `data/roles_skills.json` | Knowledge base: target roles, required skills, importance weights, synonym map            |
| `skill_extractor.py`     | Turns a user's structured skills and/or resume text into a normalized skill set           |
| `skill_matcher.py`       | Compares user skills vs. a target role; computes matched/missing skills + readiness score |
| `recommender.py`         | Builds learning resource suggestions, a phased roadmap, and an optional AI narrative      |
| `app.py`                 | Flask API exposing `/analyze`, `/roles`, `/health`                                        |
| `requirements.txt`       | Python dependencies                                                                       |

## Setup

```bash
cd ai
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py                  # runs on http://localhost:5001
```

The AI narrative feature is optional. To enable it, set an environment
variable before running:

```bash
export ANTHROPIC_API_KEY=your_key_here     # Windows: set ANTHROPIC_API_KEY=...
```

If it's not set (or the call fails for any reason — no internet, rate limit,
etc.), the module automatically falls back to a rule-based summary. **The
rest of the analysis never depends on the LLM**, so the demo is safe even
offline.

## API Contract (for the backend team)

### `POST /analyze`

**Request:**

```json
{
  "user_profile": {
    "skills": ["Python", "React", "SQL"],
    "resume_text": "Optional pasted resume or bio text..."
  },
  "target_role": "Machine Learning Engineer"
}
```

`skills` and `resume_text` are both optional individually, but at least one
should be present. Skills from both sources are merged.

**Response:**

```json
{
  "target_role": "Machine Learning Engineer",
  "readiness_score": 45.7,
  "matched_skills": [
    "git",
    "machine learning",
    "python",
    "scikit-learn",
    "sql"
  ],
  "missing_skills": ["aws", "deep learning", "docker", "..."],
  "priority_skills": [
    { "skill": "deep learning", "weight": 4, "priority": "High" }
  ],
  "recommendations": [
    {
      "skill": "deep learning",
      "priority": "High",
      "resources": [{ "title": "...", "url": "...", "platform": "..." }]
    }
  ],
  "roadmap": [
    {
      "phase": "Weeks 1-3",
      "focus": "Core gaps (High priority)",
      "skills": ["deep learning"]
    }
  ],
  "ai_summary": "You're at the early stages... (one paragraph)"
}
```

### `GET /roles`

Returns the list of supported target roles, for the frontend's role-selector
dropdown:

```json
{
  "roles": ["Data Scientist", "Machine Learning Engineer", "AI Engineer", "..."]
}
```

### `GET /health`

Liveness check — returns `{"status": "ok"}`.

## Integration options

Backend team, pick whichever is easier for your setup:

1. **Run this as its own microservice** (recommended for a hackathon —
   keeps Person 3 unblocked from Person 2's work): keep `app.py` running on
   port 5001, and have the main backend make an HTTP call to
   `POST http://localhost:5001/analyze`, then pass the result straight
   through to the frontend.
2. **Import directly**: if you end up with one combined Flask backend,
   `from ai.app import analyze_profile` and call
   `analyze_profile(user_profile, target_role)` as a plain Python function —
   no HTTP hop needed.

## Extending this after the MVP works

- **More roles**: add entries to `data/roles_skills.json` — no code changes needed.
- **Better extraction**: swap the keyword matching in `skill_extractor.py`
  for spaCy NER or an LLM-based extractor once the rule-based MVP is proven.
- **RAG upgrade**: if you want role requirements pulled from a larger,
  unstructured dataset (real job postings, syllabi) instead of the curated
  JSON, embed that dataset with `sentence-transformers` and store it in
  Chroma or FAISS, then retrieve the top-k relevant skill mentions for a
  given role before matching. Skip this for the MVP — the curated JSON is
  faster to build, easier to debug live, and good enough for a demo.
- **Resource freshness**: `LEARNING_RESOURCES` is static; could later be
  swapped for an LLM call that generates resource suggestions dynamically.

## Branch

```bash
git checkout -b ai
```

Work inside `ai/`, commit, push, and open a PR into the shared branch once
`/analyze` returns clean output for at least 2-3 test profiles.
