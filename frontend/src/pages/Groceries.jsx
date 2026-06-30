import { useEffect, useState } from 'react'
import api from '../services/api'

export default function Groceries() {
  const [items, setItems] = useState([])
  const [name, setName]   = useState('')
  const [qty, setQty]     = useState(1)

  const load = async () => setItems((await api.get('/groceries')).data)
  useEffect(() => { load() }, [])

  const add = async (e) => {
    e.preventDefault()
    if (!name.trim()) return
    await api.post('/groceries/', { name, quantity: parseInt(qty) || 1 })
    setName(''); setQty(1); load()
  }

  const toggle = async (it) => {
    await api.patch(`/groceries/${it.id}`, { checked: !it.checked })
    load()
  }

  const remove = async (id) => {
    await api.delete(`/groceries/${id}`)
    load()
  }

  return (
    <div className="page">
      <h2>Shared Grocery List</h2>
      <form className="card row" onSubmit={add}>
        <input placeholder="Item name" value={name} onChange={e => setName(e.target.value)} />
        <input type="number" min="1" value={qty} onChange={e => setQty(e.target.value)} style={{width:80}} />
        <button className="btn btn-primary">Add</button>
      </form>

      <div className="card">
        <ul className="grocery-list">
          {items.map(it => (
            <li key={it.id} className={it.checked ? 'done' : ''}>
              <label>
                <input type="checkbox" checked={it.checked} onChange={() => toggle(it)} />
                <span className="qty">{it.quantity}×</span> {it.name}
              </label>
              <button className="btn-sm danger" onClick={() => remove(it.id)}>×</button>
            </li>
          ))}
          {items.length === 0 && <p>List is empty.</p>}
        </ul>
      </div>
    </div>
  )
}