import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import Shell from "../components/Shell";
import { loadProfile, clearProfile, analyze, rank, INFO, learnUrl } from "../data";

const TABS = ["Overview", "Skill gap", "Roadmap", "Projects", "Interview"];

export default function Home() {
  const nav = useNavigate();
  const [tab, setTab] = useState(0);
  const [open, setOpen] = useState(null);
  const p = loadProfile();
  if (!p) return <Navigate to="/profile" />;
  const { matched, missing, score } = analyze(p);
  const info = INFO[p.career];
  return (
    <Shell title={`Hi ${p.name} 👋`} sub={`Target: ${p.career}${p.education ? " · " + p.education : ""}`}>
      <div className="tabs">{TABS.map((t, i) => <button key={t} className={i === tab ? "on" : ""} onClick={() => setTab(i)}>{t}</button>)}</div>
      {tab === 0 && (
        <div className="two side-l">
          <div className="glass card center">
            <div className="score" style={{ background: `conic-gradient(var(--c1) ${score}%, rgba(255,255,255,.1) 0)` }}><span>{score}%</span></div>
            <p className="sub">Career readiness</p>
            <Link to="/resume" className="btn ghost">Upload resume</Link>{" "}
            <button className="btn ghost" onClick={() => { clearProfile(); nav("/"); }}>Reset</button>
          </div>
          <div className="glass card">
            <h3>Best-fit careers</h3>
            {rank(p.skills).map((r) => (
              <div key={r.career} style={{ margin: "16px 0" }}>
                <div className="row" style={{ border: 0, padding: 0 }}><span>{r.career}</span><span className="ok">{r.score}%</span></div>
                <div className="bar"><i style={{ width: r.score + "%" }} /></div>
              </div>
            ))}
            <p className="sub">You have {matched.length} of {matched.length + missing.length} core skills for {p.career}.</p>
          </div>
        </div>
      )}
      {tab === 1 && <div className="glass card">{[...matched.map((s) => [s, 1]), ...missing.map((s) => [s, 0])].map(([s, ok]) => <div className="row" key={s}><span>{s}</span><span className={ok ? "ok" : "no"}>{ok ? "✓ You have this" : "Missing · high priority"}</span></div>)}</div>}
      {tab === 2 && (
        <div className="glass card">
          {missing.length === 0 && <p className="ok">You cover every core skill. Time to apply! 🎉</p>}
          {missing.map((s, i) => <div className="step" key={s}><b>Week {i * 2 + 1}–{i * 2 + 2}</b><div><h3>Learn {s}</h3><a className="ok" href={learnUrl(s)} target="_blank" rel="noreferrer">Watch a full course →</a></div></div>)}
        </div>
      )}
      {tab === 3 && <div className="feat">{info.projects.map((x, i) => <div className="glass card" key={x}><span className="ok">Project {i + 1}</span><h3>{x}</h3><p className="sub">Add this to your resume and GitHub.</p></div>)}</div>}
      {tab === 4 && (
        <div className="glass card">
          {info.questions.map((q, i) => (
            <div className="row" key={q} style={{ cursor: "pointer", flexDirection: "column" }} onClick={() => setOpen(open === i ? null : i)}>
              <b>{q}</b>{open === i && <p className="sub" style={{ margin: "8px 0 0" }}>Structure: definition → example → trade-off.</p>}
            </div>
          ))}
        </div>
      )}
    </Shell>
  );
}
