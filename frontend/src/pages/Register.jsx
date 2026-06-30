import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import api from '../services/api'
import { useAuth } from '../context/AuthContext'

export default function Register() {
  const [name, setName]         = useState('')
  const [email, setEmail]       = useState('')
  const [password, setPassword] = useState('')
  const [error, setError]       = useState('')
  const navigate = useNavigate()
  const { login } = useAuth()

  const submit = async (e) => {
    e.preventDefault()
    try {
      const { data } = await api.post('/auth/register', { name, email, password })
      login(data.token, data.user)
      navigate('/dashboard')
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed')
    }
  }

  return (
    <div className="auth">
      <h2>Register</h2>
      {error && <div className="error">{error}</div>}
      <form onSubmit={submit}>
        <input placeholder="Name"     value={name}     onChange={e => setName(e.target.value)}     required />
        <input type="email" placeholder="Email"    value={email}    onChange={e => setEmail(e.target.value)}    required />
        <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
        <button type="submit" className="btn btn-primary">Register</button>
      </form>
      <p>Already have an account? <Link to="/login">Login</Link></p>
    </div>
  )
}