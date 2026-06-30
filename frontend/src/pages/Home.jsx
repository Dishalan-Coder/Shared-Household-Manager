import { Link } from 'react-router-dom'

export default function Home() {
  return (
    <div className="home">
      <h1>Shared-Household Manager</h1>
      <p>Split chores, groceries and bills with your housemates — fairly.</p>
      <div className="home-actions">
        <Link to="/login"    className="btn">Login</Link>
        <Link to="/register" className="btn btn-primary">Get Started</Link>
      </div>
    </div>
  )
}