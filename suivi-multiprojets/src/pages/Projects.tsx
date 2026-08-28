import { useRef, useState } from 'react'
import type { ChangeEvent, FormEvent } from 'react'
import { newId, useStore } from '../store'
import type { AppData, Project, ProjectStatus } from '../types'
import { STATUS_LABELS } from '../types'

const emptyForm = {
  name: '',
  description: '',
  status: 'planifie' as ProjectStatus,
  startDate: '',
  endDate: '',
  progress: 0,
}

export default function Projects() {
  const { data, setProjects, importData } = useStore()
  const [form, setForm] = useState(emptyForm)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [message, setMessage] = useState('')
  const fileInputRef = useRef<HTMLInputElement>(null)

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    if (!form.name.trim()) return
    if (editingId) {
      setProjects(
        data.projects.map((p) => (p.id === editingId ? { ...p, ...form } : p)),
      )
      setEditingId(null)
    } else {
      const project: Project = { id: newId('prj'), measures: [], ...form }
      setProjects([...data.projects, project])
    }
    setForm(emptyForm)
  }

  function startEdit(project: Project) {
    setEditingId(project.id)
    setForm({
      name: project.name,
      description: project.description,
      status: project.status,
      startDate: project.startDate,
      endDate: project.endDate,
      progress: project.progress,
    })
  }

  function remove(id: string) {
    if (confirm('Supprimer ce projet ?')) {
      setProjects(data.projects.filter((p) => p.id !== id))
    }
  }

  function exportProjects() {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `suivi-multiprojets-${new Date().toISOString().slice(0, 10)}.json`
    a.click()
    URL.revokeObjectURL(url)
    setMessage('Export réalisé avec succès.')
  }

  function handleImport(e: ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = () => {
      try {
        const parsed = JSON.parse(String(reader.result)) as Partial<AppData>
        if (!Array.isArray(parsed.projects)) {
          setMessage('Fichier invalide : la clé "projects" est manquante.')
          return
        }
        importData({
          projects: parsed.projects,
          indicators: Array.isArray(parsed.indicators) ? parsed.indicators : data.indicators,
          users: Array.isArray(parsed.users) ? parsed.users : data.users,
        })
        setMessage(`Import réussi : ${parsed.projects.length} projet(s) chargé(s).`)
      } catch {
        setMessage('Fichier invalide : JSON illisible.')
      }
    }
    reader.readAsText(file)
    e.target.value = ''
  }

  return (
    <div>
      <div className="page-header">
        <h1>Projets</h1>
        <div className="actions">
          <button onClick={exportProjects}>Exporter (JSON)</button>
          <button onClick={() => fileInputRef.current?.click()}>Importer (JSON)</button>
          <input
            ref={fileInputRef}
            type="file"
            accept="application/json"
            style={{ display: 'none' }}
            onChange={handleImport}
          />
        </div>
      </div>
      {message && <p className="notice">{message}</p>}

      <div className="card">
        <h2>{editingId ? 'Modifier le projet' : 'Nouveau projet'}</h2>
        <form onSubmit={handleSubmit} className="form-grid">
          <label>
            Nom
            <input
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              required
            />
          </label>
          <label>
            Statut
            <select
              value={form.status}
              onChange={(e) => setForm({ ...form, status: e.target.value as ProjectStatus })}
            >
              {Object.entries(STATUS_LABELS).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </label>
          <label>
            Date de début
            <input
              type="date"
              value={form.startDate}
              onChange={(e) => setForm({ ...form, startDate: e.target.value })}
            />
          </label>
          <label>
            Date de fin
            <input
              type="date"
              value={form.endDate}
              onChange={(e) => setForm({ ...form, endDate: e.target.value })}
            />
          </label>
          <label className="span-2">
            Description
            <input
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
            />
          </label>
          <label>
            Avancement (%)
            <input
              type="number"
              min={0}
              max={100}
              value={form.progress}
              onChange={(e) => setForm({ ...form, progress: Number(e.target.value) })}
            />
          </label>
          <div className="form-actions">
            <button type="submit">{editingId ? 'Enregistrer' : 'Ajouter'}</button>
            {editingId && (
              <button
                type="button"
                className="secondary"
                onClick={() => {
                  setEditingId(null)
                  setForm(emptyForm)
                }}
              >
                Annuler
              </button>
            )}
          </div>
        </form>
      </div>

      <div className="card">
        <table>
          <thead>
            <tr>
              <th>Nom</th>
              <th>Statut</th>
              <th>Début</th>
              <th>Fin</th>
              <th>Avancement</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {data.projects.map((p) => (
              <tr key={p.id}>
                <td>
                  <strong>{p.name}</strong>
                  <div className="muted">{p.description}</div>
                </td>
                <td>
                  <span className={`badge badge-${p.status}`}>{STATUS_LABELS[p.status]}</span>
                </td>
                <td>{p.startDate}</td>
                <td>{p.endDate}</td>
                <td>{p.progress}%</td>
                <td className="row-actions">
                  <button className="secondary" onClick={() => startEdit(p)}>
                    Modifier
                  </button>
                  <button className="danger" onClick={() => remove(p.id)}>
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
