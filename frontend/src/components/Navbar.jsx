import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="navbar">
      <div className="nav-brand">🏠 Household Manager</div>
      {user && (
        <div className="nav-links">
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/chores">Chores</Link>
          <Link to="/groceries">Groceries</Link>
          <Link to="/expenses">Expenses</Link>
          <Link to="/balances">Balances</Link>
          <span className="nav-user">Hi, {user.name}</span>
          <button onClick={handleLogout} className="btn-link">Logout</button>
        </div>
      )}
    </nav>
  )
}