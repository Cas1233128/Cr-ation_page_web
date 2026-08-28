import { useMemo, useState } from 'react'
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { useStore } from '../store'
import { STATUS_LABELS } from '../types'

const COLORS = ['#2563eb', '#16a34a', '#ea580c', '#9333ea', '#0891b2', '#be123c']

export default function Dashboard() {
  const { data } = useStore()
  const [indicatorId, setIndicatorId] = useState(data.indicators[0]?.id ?? '')

  const indicator = data.indicators.find((i) => i.id === indicatorId)

  const chartData = useMemo(() => {
    const dates = new Set<string>()
    for (const p of data.projects) {
      for (const m of p.measures) {
        if (m.indicatorId === indicatorId) dates.add(m.date)
      }
    }
    return [...dates].sort().map((date) => {
      const row: Record<string, string | number> = { date }
      for (const p of data.projects) {
        const m = p.measures.find((x) => x.indicatorId === indicatorId && x.date === date)
        if (m) row[p.name] = m.value
      }
      return row
    })
  }, [data.projects, indicatorId])

  const stats = useMemo(() => {
    const total = data.projects.length
    const enCours = data.projects.filter((p) => p.status === 'en_cours').length
    const termines = data.projects.filter((p) => p.status === 'termine').length
    const avgProgress = total
      ? Math.round(data.projects.reduce((s, p) => s + p.progress, 0) / total)
      : 0
    return { total, enCours, termines, avgProgress }
  }, [data.projects])

  return (
    <div>
      <h1>Tableau de bord</h1>
      <div className="stat-grid">
        <div className="stat-card">
          <span className="stat-value">{stats.total}</span>
          <span className="stat-label">Projets</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{stats.enCours}</span>
          <span className="stat-label">En cours</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{stats.termines}</span>
          <span className="stat-label">Terminés</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{stats.avgProgress}%</span>
          <span className="stat-label">Avancement moyen</span>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <h2>Évolution des indicateurs</h2>
          <select value={indicatorId} onChange={(e) => setIndicatorId(e.target.value)}>
            {data.indicators.map((i) => (
              <option key={i.id} value={i.id}>
                {i.name} ({i.unit})
              </option>
            ))}
          </select>
        </div>
        {chartData.length === 0 ? (
          <p className="empty">Aucune mesure enregistrée pour cet indicateur.</p>
        ) : (
          <ResponsiveContainer width="100%" height={360}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis label={{ value: indicator?.unit ?? '', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Legend />
              {data.projects.map((p, idx) => (
                <Line
                  key={p.id}
                  type="monotone"
                  dataKey={p.name}
                  stroke={COLORS[idx % COLORS.length]}
                  strokeWidth={2}
                  connectNulls
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>

      <div className="card">
        <h2>Avancement des projets</h2>
        <table>
          <thead>
            <tr>
              <th>Projet</th>
              <th>Statut</th>
              <th>Avancement</th>
            </tr>
          </thead>
          <tbody>
            {data.projects.map((p) => (
              <tr key={p.id}>
                <td>{p.name}</td>
                <td>
                  <span className={`badge badge-${p.status}`}>{STATUS_LABELS[p.status]}</span>
                </td>
                <td>
                  <div className="progress-bar">
                    <div className="progress-fill" style={{ width: `${p.progress}%` }} />
                    <span>{p.progress}%</span>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
