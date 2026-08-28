import { useState } from 'react'
import type { FormEvent } from 'react'
import { newId, useStore } from '../store'
import type { Indicator, IndicatorMeasure } from '../types'

const emptyForm = { name: '', unit: '', description: '', target: 0 }
const emptyMeasure = { projectId: '', indicatorId: '', date: '', value: 0 }

export default function Indicators() {
  const { data, setIndicators, setProjects } = useStore()
  const [form, setForm] = useState(emptyForm)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [measure, setMeasure] = useState(emptyMeasure)

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    if (!form.name.trim()) return
    if (editingId) {
      setIndicators(data.indicators.map((i) => (i.id === editingId ? { ...i, ...form } : i)))
      setEditingId(null)
    } else {
      const indicator: Indicator = { id: newId('ind'), ...form }
      setIndicators([...data.indicators, indicator])
    }
    setForm(emptyForm)
  }

  function startEdit(indicator: Indicator) {
    setEditingId(indicator.id)
    setForm({
      name: indicator.name,
      unit: indicator.unit,
      description: indicator.description,
      target: indicator.target,
    })
  }

  function remove(id: string) {
    if (!confirm('Supprimer cet indicateur et toutes ses mesures ?')) return
    setIndicators(data.indicators.filter((i) => i.id !== id))
    setProjects(
      data.projects.map((p) => ({
        ...p,
        measures: p.measures.filter((m) => m.indicatorId !== id),
      })),
    )
  }

  function addMeasure(e: FormEvent) {
    e.preventDefault()
    if (!measure.projectId || !measure.indicatorId || !measure.date) return
    const newMeasure: IndicatorMeasure = {
      indicatorId: measure.indicatorId,
      date: measure.date,
      value: measure.value,
    }
    setProjects(
      data.projects.map((p) =>
        p.id === measure.projectId ? { ...p, measures: [...p.measures, newMeasure] } : p,
      ),
    )
    setMeasure(emptyMeasure)
  }

  return (
    <div>
      <h1>Gestion des indicateurs</h1>

      <div className="card">
        <h2>{editingId ? 'Modifier l’indicateur' : 'Nouvel indicateur'}</h2>
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
            Unité
            <input
              value={form.unit}
              onChange={(e) => setForm({ ...form, unit: e.target.value })}
              placeholder="%, k€, nb…"
            />
          </label>
          <label>
            Cible
            <input
              type="number"
              value={form.target}
              onChange={(e) => setForm({ ...form, target: Number(e.target.value) })}
            />
          </label>
          <label className="span-2">
            Description
            <input
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
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
        <h2>Indicateurs</h2>
        <table>
          <thead>
            <tr>
              <th>Nom</th>
              <th>Unité</th>
              <th>Cible</th>
              <th>Description</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {data.indicators.map((i) => (
              <tr key={i.id}>
                <td>
                  <strong>{i.name}</strong>
                </td>
                <td>{i.unit}</td>
                <td>{i.target}</td>
                <td>{i.description}</td>
                <td className="row-actions">
                  <button className="secondary" onClick={() => startEdit(i)}>
                    Modifier
                  </button>
                  <button className="danger" onClick={() => remove(i.id)}>
                    Supprimer
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="card">
        <h2>Saisir une mesure</h2>
        <form onSubmit={addMeasure} className="form-grid">
          <label>
            Projet
            <select
              value={measure.projectId}
              onChange={(e) => setMeasure({ ...measure, projectId: e.target.value })}
              required
            >
              <option value="">— Choisir —</option>
              {data.projects.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name}
                </option>
              ))}
            </select>
          </label>
          <label>
            Indicateur
            <select
              value={measure.indicatorId}
              onChange={(e) => setMeasure({ ...measure, indicatorId: e.target.value })}
              required
            >
              <option value="">— Choisir —</option>
              {data.indicators.map((i) => (
                <option key={i.id} value={i.id}>
                  {i.name}
                </option>
              ))}
            </select>
          </label>
          <label>
            Date
            <input
              type="date"
              value={measure.date}
              onChange={(e) => setMeasure({ ...measure, date: e.target.value })}
              required
            />
          </label>
          <label>
            Valeur
            <input
              type="number"
              step="any"
              value={measure.value}
              onChange={(e) => setMeasure({ ...measure, value: Number(e.target.value) })}
            />
          </label>
          <div className="form-actions">
            <button type="submit">Enregistrer la mesure</button>
          </div>
        </form>
      </div>
    </div>
  )
}
