import { useEffect, useState } from "react";
import { NavLink, Link } from "react-router-dom";
import { ping } from "../data";

const links = [["/", "🏠", "Home"], ["/home", "▦", "Dashboard"], ["/resume", "📄", "Resume"], ["/profile", "👤", "Profile"]];

export default function Shell({ title, sub, children }) {
  const [online, setOnline] = useState(null);
  useEffect(() => { ping().then(setOnline); }, []);
  return (
    <div className="shell">
      <aside className="side glass">
        <Link to="/" className="logo">◈ Career<b>Gap</b></Link>
        {links.map(([to, i, l]) => <NavLink key={to} to={to} end className="sl"><span>{i}</span>{l}</NavLink>)}
        <div className="api"><i className={online ? "dot on" : "dot"} />{online === null ? "Checking API…" : online ? "API connected" : "API offline"}</div>
      </aside>
      <main className="main">
        <h1 className="ptitle">{title}</h1>
        {sub && <p className="sub">{sub}</p>}
        {children}
      </main>
    </div>
  );
}
