import { useEffect, useState, useRef } from 'react'
import api from '../services/api'

export default function Expenses() {
  const [expenses, setExpenses]   = useState([])
  const [household, setHousehold] = useState(null)
  const [form, setForm] = useState({
    description: '', amount: '', payer_id: '', split_between: [], date: ''
  })
  const [uploadMsg, setUploadMsg] = useState('')
  const fileRef = useRef(null)

  const load = async () => {
    const hh = await api.get('/households/me')
    setHousehold(hh.data)
    setExpenses((await api.get('/expenses')).data)
  }
  useEffect(() => { load() }, [])

  const submit = async (e) => {
    e.preventDefault()
    const split = form.split_between.length ? form.split_between : household.members.map(m => m.id)
    await api.post('/expenses/', {
      description: form.description,
      amount: parseFloat(form.amount),
      payer_id: form.payer_id,
      split_between: split,
      date: form.date || undefined
    })
    setForm({ description: '', amount: '', payer_id: '', split_between: [], date: '' })
    load()
  }

  const remove = async (id) => {
    await api.delete(`/expenses/${id}`)
    load()
  }

  const toggleSplit = (mid) => {
    setForm(f => ({
      ...f,
      split_between: f.split_between.includes(mid)
        ? f.split_between.filter(x => x !== mid)
        : [...f.split_between, mid]
    }))
  }

  
  const uploadCSV = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    const fd = new FormData()
    fd.append('file', file)
    try {
      const { data } = await api.post('/expenses/upload-csv', fd, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      setUploadMsg(`✅ Imported ${data.added} of ${data.total_in_file} rows.`)
      load()
    } catch (err) {
      setUploadMsg('❌ ' + (err.response?.data?.detail || 'Upload failed'))
    }
    if (fileRef.current) fileRef.current.value = ''
  }

  
  const downloadCSV = async () => {
    const res = await api.get('/expenses/download-csv', { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([res.data]))
    const a = document.createElement('a')
    a.href = url
    a.download = 'bills.csv'
    a.click()
    window.URL.revokeObjectURL(url)
  }

  if (!household) return <div className="page"><p>Loading…</p></div>

  return (
    <div className="page">
      <h2>Shared Expenses</h2>

      <form className="card" onSubmit={submit}>
        <h3>Add Expense</h3>
        <input placeholder="Description (e.g. Electricity bill)" value={form.description}
               onChange={e => setForm({...form, description: e.target.value})} required />
        <input type="number" step="0.01" placeholder="Amount" value={form.amount}
               onChange={e => setForm({...form, amount: e.target.value})} required />
        <input type="date" value={form.date} onChange={e => setForm({...form, date: e.target.value})} />

        <label>Paid by:</label>
        <select value={form.payer_id} onChange={e => setForm({...form, payer_id: e.target.value})} required>
          <option value="">— select —</option>
          {household.members.map(m => <option key={m.id} value={m.id}>{m.name}</option>)}
        </select>

        <label>Split between (default = all):</label>
        <div className="checkbox-row">
          {household.members.map(m => (
            <label key={m.id} className="checkbox">
              <input
                type="checkbox"
                checked={form.split_between.includes(m.id)}
                onChange={() => toggleSplit(m.id)}
              /> {m.name}
            </label>
          ))}
        </div>

        <button className="btn btn-primary">Add Expense</button>
      </form>

      
      <div className="card">
        <h3>Upload Bills (CSV only)</h3>
        <p className="small">
          Expected columns: <code>description, amount, payer, date, split_between</code>.
          <br/>split_between is a comma-separated list of member names (empty = split all).
        </p>
        <input type="file" accept=".csv" ref={fileRef} onChange={uploadCSV} />
        <button className="btn" onClick={downloadCSV} style={{marginLeft:10}}>⬇ Download bills.csv</button>
        {uploadMsg && <div className="info">{uploadMsg}</div>}
      </div>

      <div className="card">
        <h3>History</h3>
        <table className="table">
          <thead><tr><th>Date</th><th>Description</th><th>Amount</th><th>Paid by</th><th>Split</th><th></th></tr></thead>
          <tbody>
            {expenses.map(e => (
              <tr key={e.id}>
                <td>{e.date?.slice(0,10)}</td>
                <td>{e.description}</td>
                <td>₹{e.amount.toFixed(2)}</td>
                <td>{e.payer_name}</td>
                <td>{e.split_between_names.join(', ')}</td>
                <td><button className="btn-sm danger" onClick={() => remove(e.id)}>×</button></td>
              </tr>
            ))}
            {expenses.length === 0 && <tr><td colSpan="6">No expenses yet.</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  )
}