import { useEffect, useState } from 'react'
import api from '../services/api'

export default function Chores() {
  const [chores, setChores]       = useState([])
  const [household, setHousehold] = useState(null)
  const [form, setForm] = useState({
    title: '', description: '', due_date: '', assigned_to: '',
    frequency: 'none', rotation_members: []
  })

  const load = async () => {
    const hh = await api.get('/households/me')
    setHousehold(hh.data)
    const { data } = await api.get('/chores')
    setChores(data)
  }
  useEffect(() => { load() }, [])

  const submit = async (e) => {
    e.preventDefault()
    const payload = {
      ...form,
      rotation_members: form.rotation_members.length ? form.rotation_members : (form.frequency !== 'none' ? [form.assigned_to] : [])
    }
    await api.post('/chores/', payload)
    setForm({ title: '', description: '', due_date: '', assigned_to: '', frequency: 'none', rotation_members: [] })
    load()
  }

  const complete = async (id) => {
    await api.post(`/chores/${id}/complete`)
    load()
  }

  const remove = async (id) => {
    await api.delete(`/chores/${id}`)
    load()
  }

  const toggleRotation = (mid) => {
    setForm(f => ({
      ...f,
      rotation_members: f.rotation_members.includes(mid)
        ? f.rotation_members.filter(x => x !== mid)
        : [...f.rotation_members, mid]
    }))
  }

  if (!household) return <div className="page"><p>Loading…</p></div>

  return (
    <div className="page">
      <h2>Chores</h2>

      <form className="card" onSubmit={submit}>
        <h3>Add Chore</h3>
        <input placeholder="Title" value={form.title} onChange={e => setForm({...form, title: e.target.value})} required />
        <input placeholder="Description" value={form.description} onChange={e => setForm({...form, description: e.target.value})} />
        <input type="date" value={form.due_date} onChange={e => setForm({...form, due_date: e.target.value})} required />

        <label>Assign to:</label>
        <select value={form.assigned_to} onChange={e => setForm({...form, assigned_to: e.target.value})} required>
          <option value="">— select —</option>
          {household.members.map(m => <option key={m.id} value={m.id}>{m.name}</option>)}
        </select>

        <label>Frequency:</label>
        <select value={form.frequency} onChange={e => setForm({...form, frequency: e.target.value})}>
          <option value="none">One-time</option>
          <option value="daily">Daily (rotating)</option>
          <option value="weekly">Weekly (rotating)</option>
          <option value="monthly">Monthly (rotating)</option>
        </select>

        {form.frequency !== 'none' && (
          <div>
            <label>Rotation order (tick members):</label>
            <div className="checkbox-row">
              {household.members.map(m => (
                <label key={m.id} className="checkbox">
                  <input
                    type="checkbox"
                    checked={form.rotation_members.includes(m.id)}
                    onChange={() => toggleRotation(m.id)}
                  /> {m.name}
                </label>
              ))}
            </div>
            <small>If none selected, only the assignee is used.</small>
          </div>
        )}

        <button className="btn btn-primary" type="submit">Add Chore</button>
      </form>

      <div className="card">
        <h3>All Chores</h3>
        <ul className="chore-list">
          {chores.map(c => (
            <li key={c.id} className={c.completed ? 'done' : ''}>
              <div>
                <b>{c.title}</b> — {c.assigned_to_name} · due {c.due_date?.slice(0,10)}
                {c.rotation_members?.length > 0 && <span className="badge">🔁 {c.frequency} · idx {c.rotation_index}</span>}
                {c.completed && <span className="badge done-badge">✓ done</span>}
                {c.last_completed_by && <small> (last by {c.last_completed_by?.slice(-4)})</small>}
              </div>
              <div className="actions">
                {!c.completed && <button className="btn-sm" onClick={() => complete(c.id)}>Complete</button>}
                <button className="btn-sm danger" onClick={() => remove(c.id)}>Delete</button>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}