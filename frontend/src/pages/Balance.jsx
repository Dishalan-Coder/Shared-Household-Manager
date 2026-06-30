import { useEffect, useState } from 'react'
import api from '../services/api'

export default function Balances() {
  const [data, setData] = useState(null)

  const load = async () => setData((await api.get('/expenses/balances')).data)
  useEffect(() => { load() }, [])

  if (!data) return <div className="page"><p>Loading…</p></div>

  return (
    <div className="page">
      <h2>Balances — Who Owes Whom</h2>

      <div className="card">
        <h3>Member Summary</h3>
        <table className="table">
          <thead><tr><th>Member</th><th>Paid</th><th>Owes</th><th>Net</th></tr></thead>
          <tbody>
            {data.members.map(m => (
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
        <p className="small">Total household spend: <b>₹{data.total_expenses.toFixed(2)}</b></p>
      </div>

      <div className="card">
        <h3>Suggested Settlements</h3>
        {data.settlements.length === 0 ? (
          <p>All settled up! </p>
        ) : (
          <ul className="settlement-list">
            {data.settlements.map((s, i) => (
              <li key={i}>
                <b>{s.from}</b> should pay <b>{s.to}</b> → <span className="amt">₹{s.amount.toFixed(2)}</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}