import { useEffect, useState } from 'react'
import api from '../services/api'

export default function Dashboard() {
  const [household, setHousehold] = useState(null)
  const [chores,    setChores]    = useState([])
  const [balances,  setBalances]  = useState(null)
  const [name, setName]           = useState('')
  const [code, setCode]           = useState('')
  const [msg, setMsg]             = useState('')

  const refreshHousehold = async () => {
    const { data } = await api.get('/households/me')
    setHousehold(data)
    if (data) {
      const [c, b] = await Promise.all([
        api.get('/chores'),
        api.get('/expenses/balances')
      ])
      setChores(c.data)
      setBalances(b.data)
    }
  }

  useEffect(() => { refreshHousehold() }, [])

  const createHH = async () => {
    if (!name.trim()) return
    await api.post('/households/', { name })
    setMsg('Household created!')
    refreshHousehold()
  }

  const joinHH = async () => {
    if (!code.trim()) return
    try {
      await api.post('/households/join', { invite_code: code })
      setMsg('Joined household!')
      refreshHousehold()
    } catch (err) {
      setMsg(err.response?.data?.detail || 'Invalid code')
    }
  }

  if (!household) {
    return (
      <div className="page">
        <h2>Join or Create a Household</h2>
        <div className="card">
          <h3>Create new</h3>
          <input placeholder="Household name" value={name} onChange={e => setName(e.target.value)} />
          <button className="btn btn-primary" onClick={createHH}>Create</button>
        </div>
        <div className="card">
          <h3>Join existing</h3>
          <input placeholder="Invite code (e.g. A1B2C3)" value={code} onChange={e => setCode(e.target.value)} />
          <button className="btn" onClick={joinHH}>Join</button>
        </div>
        {msg && <div className="info">{msg}</div>}
      </div>
    )
  }

  const openChores = chores.filter(c => !c.completed)

  return (
    <div className="page">
      <h2>{household.name}</h2>
      <div className="info">Invite code: <b>{household.invite_code}</b> · {household.members.length} members</div>

      <div className="stats-grid">
        <div className="stat-card">
          <h4>Open Chores</h4>
          <div className="stat-num">{openChores.length}</div>
        </div>
        <div className="stat-card">
          <h4>Total Expenses</h4>
          <div className="stat-num">₹{balances?.total_expenses?.toFixed(2) || '0.00'}</div>
        </div>
        <div className="stat-card">
          <h4>Members</h4>
          <div className="stat-num">{household.members.length}</div>
        </div>
        <div className="stat-card">
          <h4>Settlements Needed</h4>
          <div className="stat-num">{balances?.settlements?.length || 0}</div>
        </div>
      </div>

      <div className="card">
        <h3>Members</h3>
        <ul className="member-list">
          {household.members.map(m => <li key={m.id}>{m.name} · {m.email}</li>)}
        </ul>
      </div>

      <div className="card">
        <h3>Open Chores</h3>
        {openChores.length === 0 ? <p>All done! 🎉</p> :
          <ul className="chore-list">
            {openChores.map(c => (
              <li key={c.id}>
                <b>{c.title}</b> — assigned to {c.assigned_to_name} · due {c.due_date?.slice(0,10)}
                {c.rotation_members?.length > 0 && <span className="badge">🔁 {c.frequency}</span>}
              </li>
            ))}
          </ul>
        }
      </div>

      {balances && (
        <div className="card">
          <h3>Current Balances</h3>
          <table className="table">
            <thead><tr><th>Member</th><th>Paid</th><th>Owed</th><th>Net</th></tr></thead>
            <tbody>
              {balances.members.map(m => (
                <tr key={m.id}>
                  <td>{m.name}</td>
                  <td>₹{m.paid.toFixed(2)}</td>
                  <td>₹{m.owed.toFixed(2)}</td>
                  <td className={m.net >= 0 ? 'pos' : 'neg'}>
                    {m.net >= 0 ? '+' : ''}₹{m.net.toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}