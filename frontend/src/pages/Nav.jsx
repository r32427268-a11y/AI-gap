import { Link } from "react-router-dom";
export default function Nav() {
  return (
    <nav>
      <Link to="/" className="logo">Career<b>Gap</b> AI</Link>
      <div>
        <Link to="/profile">Profile</Link>
        <Link to="/resume">Resume</Link>
        <Link to="/home">Dashboard</Link>
      </div>
    </nav>
  );
}
