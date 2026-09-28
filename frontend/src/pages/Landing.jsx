import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";

const TILES = [
  { n: "Python", i: "🐍", x: -560, y: -230, z: 60, r: -12 },
  { n: "SQL", i: "🗄️", x: -250, y: -310, z: -90, r: 8 },
  { n: "React", i: "⚛️", x: 420, y: -260, z: 40, r: 14 },
  { n: "Git", i: "🌿", x: 660, y: -40, z: -70, r: -9 },
  { n: "Docker", i: "🐳", x: -700, y: -70, z: -30, r: 10, gap: 1 },
  { n: "APIs", i: "🔌", x: 570, y: 220, z: 80, r: -14, gap: 1 },
  { n: "NLP", i: "🧠", x: 300, y: 310, z: -60, r: 9, gap: 1 },
  { n: "Figma", i: "🎨", x: 20, y: 330, z: -80, r: -8 },
];
const CAP = [
  ["Scene 01 · Where you are", "Your skills,", "mapped.", "Every skill you already own, floating in one place. Upload a resume and watch it appear."],
  ["Scene 02 · The gap", "See what's", "missing.", "The dashed tiles are skills your target role needs and you don't have yet."],
  ["Scene 03 · The path", "Close it,", "week by week.", "A roadmap with a course for every gap. Your readiness climbs as the tiles lock in."],
];
const features = [
  ["📄", "Live resume scan", "Upload a PDF or DOCX. Skills are extracted by your backend in seconds.", "wide"],
  ["🎯", "Skill gap analysis", "See exactly what you have and what is missing.", ""],
  ["🧭", "Best-fit careers", "Every role ranked by how ready you are today.", ""],
  ["🗺️", "Weekly roadmap", "A step-by-step plan with a course for each missing skill.", "wide"],
  ["🛠️", "Project ideas", "Portfolio projects that prove each skill.", ""],
  ["🎤", "Interview prep", "Role-specific questions to practice.", ""],
];
const faq = [
  ["Is my data private?", "Your profile lives only in your browser. Resumes are parsed by your own local backend."],
  ["Which resume formats work?", "PDF and DOCX."],
  ["Which careers are supported?", "Data Scientist, Web Developer, Backend Engineer and UI/UX Designer."],
];
const L = (a, b, t) => a + (b - a) * t;

export default function Landing() {
  const ref = useRef(null);
  const [p, setP] = useState(0);
  const [m, setM] = useState({ x: 0, y: 0 });
  useEffect(() => {
    const on = () => {
      const el = ref.current;
      const h = el.offsetHeight - window.innerHeight;
      setP(Math.min(1, Math.max(0, -el.getBoundingClientRect().top / h)));
    };
    on();
    window.addEventListener("scroll", on, { passive: true });
    return () => window.removeEventListener("scroll", on);
  }, []);
  const scene = p < 0.34 ? 0 : p < 0.67 ? 1 : 2;
  const t = Math.min(1, Math.max(0, (p - 0.6) / 0.3));
  const cap = CAP[scene];
  return (
    <div>
      <header className="top glass">
        <Link to="/" className="logo">◈ Career<b>Gap</b></Link>
        <div><a href="#features">Features</a><a href="#how">How it works</a><a href="#faq">FAQ</a><Link to="/resume" className="btn sm">Get started</Link></div>
      </header>

      <section className="film" ref={ref}>
        <div className="sticky" onMouseMove={(e) => setM({ x: (e.clientX / window.innerWidth - 0.5) * 14, y: (e.clientY / window.innerHeight - 0.5) * -10 })}>
          <div className="world" style={{ transform: `rotateX(${m.y + 6}deg) rotateY(${m.x + (p - 0.5) * 34}deg)` }}>
            {TILES.map((T, i) => {
              const a = (i / TILES.length) * Math.PI * 2;
              const x = L(T.x, Math.cos(a) * 470, t), y = L(T.y, Math.sin(a) * 180, t), z = L(T.z, Math.sin(a) * 260, t) + p * 90, r = L(T.r, 0, t);
              const ghost = T.gap && scene === 1;
              return (
                <div key={T.n} className={"tile" + (ghost ? " ghost" : "")} style={{ transform: `translate3d(${x}px,${y}px,${z}px) rotateZ(${r}deg)` }}>
                  <div className="ti" style={{ animationDelay: `${-i * 0.8}s` }}><b>{T.i}</b><span>{ghost ? "missing" : T.n}</span></div>
                </div>
              );
            })}
            <div className="orb" style={{ transform: `scale(${0.85 + 0.35 * t})` }}>
              <small>Backend Engineer</small><b>{Math.round(L(34, 92, t))}%</b><span>readiness</span>
            </div>
          </div>
          <div className="cap" key={scene}>
            <span className="pill">{cap[0]}</span>
            <h1 className="serif">{cap[1]}<br /><em>{cap[2]}</em></h1>
            <p className="sub">{cap[3]}</p>
            {scene !== 1 ? <><Link to="/resume" className="btn">Upload my resume →</Link>{" "}{scene === 0 && <span className="hint">Scroll ↓</span>}</> : <span className="hint">Keep scrolling ↓</span>}
          </div>
          <div className="tl">
            <span className="sc">0{scene + 1}/03</span>
            <div className="track"><i style={{ width: p * 100 + "%" }} /></div>
          </div>
        </div>
      </section>

      <section className="stats glass">{[["4", "Career tracks"], ["24+", "Skills tracked"], ["5", "Analysis views"], ["<5s", "Resume scan"]].map(([n, l]) => <div key={l}><b>{n}</b><span>{l}</span></div>)}</section>
      <section className="sec" id="features"><h2 className="serif2">Everything you need to close the gap</h2>
        <div className="bento">{features.map(([i, h, pp, w]) => <div className={"glass card " + w} key={h}><div className="ico">{i}</div><h3>{h}</h3><p className="sub">{pp}</p></div>)}</div></section>
      <section className="sec" id="how"><h2 className="serif2">How it works</h2>
        <div className="feat">{["Upload your resume", "Pick your target role", "Get your plan"].map((s, i) => <div className="glass card" key={s}><span className="num">0{i + 1}</span><h3>{s}</h3></div>)}</div></section>
      <section className="sec narrow" id="faq"><h2 className="serif2">FAQ</h2>
        {faq.map(([q, a]) => <details className="glass" key={q}><summary>{q}</summary><p className="sub">{a}</p></details>)}</section>
      <section className="sec cta glass"><h2 className="serif2">Ready to see your gap?</h2><Link to="/resume" className="btn">Start free →</Link></section>
      <footer>© CareerGap AI · Built for your next role</footer>
    </div>
  );
}
