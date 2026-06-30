import { Routes, Route, Navigate } from 'react-router-dom'
import Login      from './pages/Login'
import Register   from './pages/Register'
import Home       from './pages/Home'
import Dashboard  from './pages/Dashboard'
import Chores     from './pages/Chores'
import Groceries  from './pages/Groceries'
import Expenses   from './pages/Expenses'
import Balances   from './pages/Balances'
import ProtectedRoute from './components/ProtectedRoute'
import Navbar     from './components/Navbar'
import { useAuth } from './context/AuthContext'

export default function App() {
  const { user } = useAuth()
  return (
    <div className="app">
      {user && <Navbar />}
      <Routes>
        <Route path="/"          element={user ? <Navigate to="/dashboard"/> : <Home/>} />
        <Route path="/login"     element={<Login/>} />
        <Route path="/register"  element={<Register/>} />
        <Route path="/dashboard" element={<ProtectedRoute><Dashboard/></ProtectedRoute>} />
        <Route path="/chores"    element={<ProtectedRoute><Chores/></ProtectedRoute>} />
        <Route path="/groceries" element={<ProtectedRoute><Groceries/></ProtectedRoute>} />
        <Route path="/expenses"  element={<ProtectedRoute><Expenses/></ProtectedRoute>} />
        <Route path="/balances"  element={<ProtectedRoute><Balances/></ProtectedRoute>} />
      </Routes>
    </div>
  )
}