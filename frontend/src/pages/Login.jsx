import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import api from '../services/api'
import { useAuth } from '../context/AuthContext'
import { validateEmail, validatePassword } from '../utils/validators'

export default function Login() {
  const [email,    setEmail]    = useState('')
  const [password, setPassword] = useState('')

  const [errors, setErrors] = useState({ email: '', password: '' })
  const [touched, setTouched] = useState({ email: false, password: false })

  const [error,    setError]    = useState('')
  const [submitting, setSubmitting] = useState(false)

  const navigate = useNavigate()
  const { login } = useAuth()

  const validateField = (field, value) => {
    let message = ''
    if (field === 'email') message = validateEmail(value)
    if (field === 'password') message = validatePassword(value)
    setErrors(prev => ({ ...prev, [field]: message }))
    return message
  }

  const handleChange = (field, value) => {
    if (field === 'email') setEmail(value)
    if (field === 'password') setPassword(value)
    if (touched[field]) validateField(field, value)
  }

  const handleBlur = (field, value) => {
    setTouched(prev => ({ ...prev, [field]: true }))
    validateField(field, value)
  }

  const validateAll = () => {
    const emailError    = validateField('email', email)
    const passwordError = validateField('password', password)
    setTouched({ email: true, password: true })
    return !emailError && !passwordError
  }

  const submit = async (e) => {
    e.preventDefault()
    setError('')

    if (!validateAll()) {
      return
    }

    setSubmitting(true)
    try {
      const { data } = await api.post('/auth/login', { email: email.trim(), password })
      login(data.token, data.user)
      navigate('/dashboard')
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="auth">
      <h2>Login</h2>
      {error && <div className="error">{error}</div>}
      <form onSubmit={submit} noValidate>
        <div className="form-field">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={e => handleChange('email', e.target.value)}
            onBlur={e => handleBlur('email', e.target.value)}
            className={errors.email && touched.email ? 'input-error' : ''}
          />
          {touched.email && errors.email && <small className="field-error">{errors.email}</small>}
        </div>

        <div className="form-field">
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={e => handleChange('password', e.target.value)}
            onBlur={e => handleBlur('password', e.target.value)}
            className={errors.password && touched.password ? 'input-error' : ''}
          />
          {touched.password && errors.password && <small className="field-error">{errors.password}</small>}
        </div>

        <button type="submit" className="btn btn-primary" disabled={submitting}>
          {submitting ? 'Logging in…' : 'Login'}
        </button>
      </form>
      <p>Don't have an account? <Link to="/register">Register</Link></p>
    </div>
  )
}
