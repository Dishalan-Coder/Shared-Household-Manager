import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import api from '../services/api'
import { useAuth } from '../context/AuthContext'
import { validateName, validateEmail, validatePassword, PASSWORD_RULES } from '../utils/validators'

export default function Register() {
  const [name, setName]         = useState('')
  const [email, setEmail]       = useState('')
  const [password, setPassword] = useState('')

  // Field-level validation errors (shown under each input)
  const [errors, setErrors] = useState({ name: '', email: '', password: '' })
  // Tracks which fields the user has already interacted with, so we don't
  // show "required" errors before they've even typed anything.
  const [touched, setTouched] = useState({ name: false, email: false, password: false })

  // Server / general error (e.g. "Email already registered")
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const navigate = useNavigate()
  const { login } = useAuth()

  const validateField = (field, value) => {
    let message = ''
    if (field === 'name') message = validateName(value)
    if (field === 'email') message = validateEmail(value)
    if (field === 'password') message = validatePassword(value)
    setErrors(prev => ({ ...prev, [field]: message }))
    return message
  }

  const handleChange = (field, value) => {
    if (field === 'name') setName(value)
    if (field === 'email') setEmail(value)
    if (field === 'password') setPassword(value)
    // Re-validate as the user types, but only once the field has been touched
    if (touched[field]) validateField(field, value)
  }

  const handleBlur = (field, value) => {
    setTouched(prev => ({ ...prev, [field]: true }))
    validateField(field, value)
  }

  const validateAll = () => {
    const nameError     = validateField('name', name)
    const emailError    = validateField('email', email)
    const passwordError = validateField('password', password)
    setTouched({ name: true, email: true, password: true })
    return !nameError && !emailError && !passwordError
  }

  const submit = async (e) => {
    e.preventDefault()
    setError('')

    if (!validateAll()) {
      return
    }

    setSubmitting(true)
    try {
      const { data } = await api.post('/auth/register', { name: name.trim(), email: email.trim(), password })
      login(data.token, data.user)
      navigate('/dashboard')
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="auth">
      <h2>Register</h2>
      {error && <div className="error">{error}</div>}
      <form onSubmit={submit} noValidate>
        <div className="form-field">
          <input
            placeholder="Name"
            value={name}
            onChange={e => handleChange('name', e.target.value)}
            onBlur={e => handleBlur('name', e.target.value)}
            className={errors.name && touched.name ? 'input-error' : ''}
          />
          {touched.name && errors.name && <small className="field-error">{errors.name}</small>}
        </div>

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
          <small className="field-hint">
            Password must have {PASSWORD_RULES.map(r => r.label.replace('At least ', '')).join(', ')}.
          </small>
        </div>

        <button type="submit" className="btn btn-primary" disabled={submitting}>
          {submitting ? 'Registering…' : 'Register'}
        </button>
      </form>
      <p>Already have an account? <Link to="/login">Login</Link></p>
    </div>
  )
}
