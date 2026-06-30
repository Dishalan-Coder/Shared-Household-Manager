import { Link } from 'react-router-dom'

export default function Home() {
  return (
    <div className="home">
<<<<<<< HEAD
      <h1>🏠 Shared-Household Manager</h1>
=======
      <h1> Shared-Household Manager</h1>
>>>>>>> 336a4142295721689e63031816a7c5e7a1677629
      <p>Split chores, groceries and bills with your housemates — fairly.</p>
      <div className="home-actions">
        <Link to="/login"    className="btn">Login</Link>
        <Link to="/register" className="btn btn-primary">Get Started</Link>
      </div>
    </div>
  )
}