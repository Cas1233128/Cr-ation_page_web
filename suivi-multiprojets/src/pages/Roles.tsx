import { useState } from 'react'
import type { FormEvent } from 'react'
import { newId, useStore } from '../store'
import type { Role, User } from '../types'
import { ROLE_DESCRIPTIONS, ROLE_LABELS } from '../types'

const emptyForm = { name: '', email: '', role: 'lecteur' as Role }

export default function Roles() {
  const { data, setUsers } = useStore()
  const [form, setForm] = useState(emptyForm)

  function addUser(e: FormEvent) {
    e.preventDefault()
    if (!form.name.trim() || !form.email.trim()) return
    const user: User = { id: newId('usr'), ...form }
    setUsers([...data.users, user])
    setForm(emptyForm)
  }

  function updateRole(id: string, role: Role) {
    setUsers(data.users.map((u) => (u.id === id ? { ...u, role } : u)))
  }

  function remove(id: string) {
    if (confirm('Supprimer cet utilisateur ?')) {
      setUsers(data.users.filter((u) => u.id !== id))
    }
  }

  return (
    <div>
      <h1>Gestion des rôles</h1>

      <div className="card">
        <h2>Rôles disponibles</h2>
        <table>
          <thead>
            <tr>
              <th>Rôle</th>
              <th>Permissions</th>
            </tr>
          </thead>
          <tbody>
            {(Object.keys(ROLE_LABELS) as Role[]).map((role) => (
              <tr key={role}>
                <td>
                  <span className={`badge badge-role-${role}`}>{ROLE_LABELS[role]}</span>
                </td>
                <td>{ROLE_DESCRIPTIONS[role]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="card">
        <h2>Ajouter un utilisateur</h2>
        <form onSubmit={addUser} className="form-grid">
          <label>
            Nom
            <input
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              required
            />
          </label>
          <label>
            Email
            <input
              type="email"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              required
            />
          </label>
          <label>
            Rôle
            <select
              value={form.role}
              onChange={(e) => setForm({ ...form, role: e.target.value as Role })}
            >
              {(Object.keys(ROLE_LABELS) as Role[]).map((role) => (
                <option key={role} value={role}>
                  {ROLE_LABELS[role]}
                </option>
              ))}
            </select>
          </label>
          <div className="form-actions">
            <button type="submit">Ajouter</button>
          </div>
        </form>
      </div>

      <div className="card">
        <h2>Utilisateurs</h2>
        <table>
          <thead>
            <tr>
              <th>Nom</th>
              <th>Email</th>
              <th>Rôle</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {data.users.map((u) => (
              <tr key={u.id}>
                <td>{u.name}</td>
                <td>{u.email}</td>
                <td>
                  <select value={u.role} onChange={(e) => updateRole(u.id, e.target.value as Role)}>
                    {(Object.keys(ROLE_LABELS) as Role[]).map((role) => (
                      <option key={role} value={role}>
                        {ROLE_LABELS[role]}
                      </option>
                    ))}
                  </select>
                </td>
                <td className="row-actions">
                  <button className="danger" onClick={() => remove(u.id)}>
                    Supprimer
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
