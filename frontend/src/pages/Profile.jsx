import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Shell from "../components/Shell";
import { CAREERS, ALL_SKILLS, saveProfile, loadProfile } from "../data";

export default function Profile() {
  const nav = useNavigate();
  const old = loadProfile();
  const [name, setName] = useState(old?.name || "");
  const [education, setEducation] = useState(old?.education || "");
  const [career, setCareer] = useState(old?.career || Object.keys(CAREERS)[0]);
  const [skills, setSkills] = useState(old?.skills || []);
  const toggle = (s) => setSkills((p) => (p.includes(s) ? p.filter((x) => x !== s) : [...p, s]));
  const submit = () => { saveProfile({ name: name || "Explorer", education, career, skills }); nav("/home"); };
  return (
    <Shell title="Your profile" sub="Tell us who you are and where you want to go.">
      <div className="glass card">
        <div className="two">
          <div><label>Name</label><input value={name} onChange={(e) => setName(e.target.value)} placeholder="e.g. Vyom" /></div>
          <div><label>Education</label><input value={education} onChange={(e) => setEducation(e.target.value)} placeholder="e.g. B.Tech CSE" /></div>
        </div>
        <label>Target career</label>
        <select value={career} onChange={(e) => setCareer(e.target.value)}>{Object.keys(CAREERS).map((c) => <option key={c}>{c}</option>)}</select>
        <label>Skills you already have</label>
        <div className="chips">{ALL_SKILLS.map((s) => <button key={s} className={"chip" + (skills.includes(s) ? " on" : "")} onClick={() => toggle(s)}>{s}</button>)}</div>
        <br /><button className="btn" onClick={submit}>Save & analyze →</button>
      </div>
    </Shell>
  );
}
