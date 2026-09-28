export const API = import.meta.env.VITE_API_URL ?? (import.meta.env.PROD ? "" : "http://127.0.0.1:8000");
export const CAREERS = {
  "Data Scientist": ["Python", "Statistics", "Machine Learning", "Deep Learning", "SQL", "NLP"],
  "Web Developer": ["HTML", "CSS", "JavaScript", "React", "Node.js", "Git"],
  "Backend Engineer": ["Python", "SQL", "APIs", "Docker", "Git", "System Design"],
  "UI/UX Designer": ["Figma", "Wireframing", "Prototyping", "User Research", "CSS", "Design Systems"],
};
export const ALL_SKILLS = [...new Set(Object.values(CAREERS).flat())];
export const INFO = {
  "Data Scientist": { projects: ["Customer churn predictor with a deployed model", "Sentiment analysis on reviews (NLP)", "Kaggle competition write-up"], questions: ["Explain bias vs variance.", "How do you handle imbalanced data?", "L1 vs L2 regularization?"] },
  "Web Developer": { projects: ["Portfolio site with animations", "Full-stack task manager (React + Node)", "Weather dashboard using a public API"], questions: ["Explain the virtual DOM.", "What is a closure?", "How does CORS work?"] },
  "Backend Engineer": { projects: ["REST API with auth and a database", "URL shortener with caching", "Dockerized microservice"], questions: ["SQL index: how does it help?", "Design a rate limiter.", "REST vs GraphQL?"] },
  "UI/UX Designer": { projects: ["Redesign a real app's onboarding", "Design system in Figma", "Usability test report"], questions: ["Walk me through your design process.", "How do you validate a design?", "What makes a UI accessible?"] },
};
const ALIAS = { JavaScript: ["js"], "Machine Learning": ["ml"], "Node.js": ["node", "nodejs"], APIs: ["api", "rest"], "Deep Learning": ["neural network", "cnn"], NLP: ["natural language"], Statistics: ["statistical"], Figma: ["figma"] };
export const detect = (text) => {
  const t = text.toLowerCase();
  return ALL_SKILLS.filter((s) =>
    [s, ...(ALIAS[s] || [])].some((a) => new RegExp(`(^|[^a-z])${a.toLowerCase().replace(/[.+]/g, "\\$&")}([^a-z]|$)`).test(t))
  );
};
export const resumeChecks = (text) => {
  const t = text.toLowerCase();
  return [
    ["Email address", /[\w.-]+@[\w.-]+\.\w+/.test(t)], ["Phone number", /\+?\d[\d\s-]{8,}/.test(t)],
    ["LinkedIn / GitHub link", /linkedin|github/.test(t)], ["Education section", /education|b\.?tech|degree|university/.test(t)],
    ["Projects section", /project/.test(t)], ["Experience / internship", /experience|intern/.test(t)],
    ["Skills section", /skills/.test(t)], ["Enough detail (250+ words)", t.split(/\s+/).length > 250],
  ];
};
export const learnUrl = (s) => `https://www.youtube.com/results?search_query=${encodeURIComponent(s + " full course")}`;
const KEY = "careergap_profile";
export const saveProfile = (p) => localStorage.setItem(KEY, JSON.stringify(p));
export const clearProfile = () => localStorage.removeItem(KEY);
export const loadProfile = () => { try { return JSON.parse(localStorage.getItem(KEY)); } catch { return null; } };
export const analyze = (p) => {
  const req = CAREERS[p.career] || [];
  const have = p.skills.map((s) => s.toLowerCase());
  const matched = req.filter((r) => have.includes(r.toLowerCase()));
  const missing = req.filter((r) => !have.includes(r.toLowerCase()));
  return { matched, missing, score: Math.round((matched.length / req.length) * 100) };
};
export const rank = (skills) =>
  Object.keys(CAREERS).map((career) => ({ career, ...analyze({ career, skills }) })).sort((a, b) => b.score - a.score);
export const ping = () => fetch(`${API}/`).then((r) => r.ok).catch(() => false);
