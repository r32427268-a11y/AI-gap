import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Shell from "../components/Shell";
import { API, CAREERS, ALL_SKILLS, detect, resumeChecks, loadProfile, saveProfile } from "../data";

export default function Resume() {
  const nav = useNavigate();
  const old = loadProfile();
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");
  const [file, setFile] = useState("");
  const [text, setText] = useState("");
  const [skills, setSkills] = useState(old?.skills || []);
  const [career, setCareer] = useState(old?.career || Object.keys(CAREERS)[0]);

  const upload = async (f) => {
    if (!f) return;
    setBusy(true); setErr(""); setFile(f.name);
    try {
      const fd = new FormData(); fd.append("file", f);
      const r = await fetch(`${API}/api/resume/upload`, { method: "POST", body: fd });
      const d = await r.json();
      if (!r.ok) throw new Error(d.detail || "Upload failed");
      setText(d.text); setSkills((p) => [...new Set([...p, ...detect(d.text)])]);
    } catch (e) { setErr(e.message === "Failed to fetch" ? "Backend offline. Run: uvicorn main:app --reload" : e.message); }
    setBusy(false);
  };
  const toggle = (s) => setSkills((p) => (p.includes(s) ? p.filter((x) => x !== s) : [...p, s]));
  const checks = text ? resumeChecks(text) : [];
  const go = () => { saveProfile({ name: old?.name || "Explorer", education: old?.education || "", career, skills }); nav("/home"); };

  return (
    <Shell title="Resume analyzer" sub="Upload a PDF or DOCX. Your backend parses it and we detect your skills.">
      <label className="drop glass">
        <input type="file" accept=".pdf,.docx" hidden onChange={(e) => upload(e.target.files[0])} />
        <div className="big">📄</div>{busy ? "Reading resume…" : file ? `${file} · click to replace` : "Click to upload your resume"}
      </label>
      {err && <p className="no">{err}</p>}
      <div className="two" style={{ marginTop: 20 }}>
        <div className="glass card">
          <h3>Detected skills</h3>
          <div className="chips">{ALL_SKILLS.map((s) => <button key={s} className={"chip" + (skills.includes(s) ? " on" : "")} onClick={() => toggle(s)}>{s}</button>)}</div>
          <label>Target career</label>
          <select value={career} onChange={(e) => setCareer(e.target.value)}>{Object.keys(CAREERS).map((c) => <option key={c}>{c}</option>)}</select>
          <br /><br /><button className="btn" onClick={go}>See gap analysis →</button>
        </div>
        <div className="glass card">
          <h3>Resume health {text && <span className="ok">{checks.filter((c) => c[1]).length}/{checks.length}</span>}</h3>
          {!text && <p className="sub">Upload a resume to see the checklist.</p>}
          {checks.map(([n, ok]) => <div className="row" key={n}><span>{n}</span><span className={ok ? "ok" : "no"}>{ok ? "✓" : "✗ Add"}</span></div>)}
        </div>
      </div>
    </Shell>
  );
}
