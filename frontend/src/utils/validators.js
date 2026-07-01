// Centralized, strict client-side validation rules.
// Used by Login.jsx and Register.jsx (and reusable anywhere else a form needs it).

// Strict email check:
//  - must contain exactly one "@"
//  - must have a non-empty local part before "@"
//  - must have a domain with at least one "." after "@" (e.g. user@example.com)
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/

export function validateName(name) {
  const value = (name || '').trim()
  if (!value) return 'Name is required'
  if (value.length < 2) return 'Name must be at least 2 characters'
  if (value.length > 60) return 'Name must be under 60 characters'
  return ''
}

export function validateEmail(email) {
  const value = (email || '').trim()
  if (!value) return 'Email is required'
  if (!value.includes('@')) return 'Email must contain "@"'
  if (!EMAIL_REGEX.test(value)) return 'Enter a valid email address (e.g. name@example.com)'
  return ''
}

// Password policy: min 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special character.
export const PASSWORD_RULES = [
  { test: (v) => v.length >= 8, label: 'At least 8 characters' },
  { test: (v) => /[A-Z]/.test(v), label: 'At least 1 uppercase letter' },
  { test: (v) => /[a-z]/.test(v), label: 'At least 1 lowercase letter' },
  { test: (v) => /[0-9]/.test(v), label: 'At least 1 number' },
  { test: (v) => /[^A-Za-z0-9]/.test(v), label: 'At least 1 special character' },
]

export function validatePassword(password) {
  const value = password || ''
  if (!value) return 'Password is required'
  const failed = PASSWORD_RULES.filter(rule => !rule.test(value))
  if (failed.length) {
    return 'Password needs: ' + failed.map(r => r.label).join(', ')
  }
  return ''
}

// Generic "required" check for simple text fields (used by other forms).
export function validateRequired(value, fieldLabel = 'This field') {
  if (value === undefined || value === null || String(value).trim() === '') {
    return `${fieldLabel} is required`
  }
  return ''
}
