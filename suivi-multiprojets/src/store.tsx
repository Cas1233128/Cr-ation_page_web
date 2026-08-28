import { createContext, useContext, useEffect, useState } from 'react'
import type { ReactNode } from 'react'
import type { AppData, Indicator, Project, User } from './types'

const STORAGE_KEY = 'suivi-multiprojets-data'

const seedData: AppData = {
  indicators: [
    { id: 'ind-1', name: 'Taux d’avancement', unit: '%', description: 'Avancement global du projet', target: 100 },
    { id: 'ind-2', name: 'Budget consommé', unit: 'k€', description: 'Budget cumulé consommé', target: 250 },
    { id: 'ind-3', name: 'Jalons atteints', unit: 'nb', description: 'Nombre de jalons validés', target: 12 },
  ],
  projects: [
    {
      id: 'prj-1',
      name: 'Refonte du portail client',
      description: 'Modernisation du portail web client',
      status: 'en_cours',
      startDate: '2026-01-15',
      endDate: '2026-09-30',
      progress: 55,
      measures: [
        { indicatorId: 'ind-1', date: '2026-03-01', value: 15 },
        { indicatorId: 'ind-1', date: '2026-05-01', value: 35 },
        { indicatorId: 'ind-1', date: '2026-07-01', value: 55 },
        { indicatorId: 'ind-2', date: '2026-03-01', value: 40 },
        { indicatorId: 'ind-2', date: '2026-05-01', value: 95 },
        { indicatorId: 'ind-2', date: '2026-07-01', value: 150 },
        { indicatorId: 'ind-3', date: '2026-03-01', value: 2 },
        { indicatorId: 'ind-3', date: '2026-05-01', value: 5 },
        { indicatorId: 'ind-3', date: '2026-07-01', value: 8 },
      ],
    },
    {
      id: 'prj-2',
      name: 'Migration ERP',
      description: 'Migration vers le nouvel ERP',
      status: 'en_cours',
      startDate: '2026-02-01',
      endDate: '2026-12-15',
      progress: 30,
      measures: [
        { indicatorId: 'ind-1', date: '2026-03-01', value: 5 },
        { indicatorId: 'ind-1', date: '2026-05-01', value: 18 },
        { indicatorId: 'ind-1', date: '2026-07-01', value: 30 },
        { indicatorId: 'ind-2', date: '2026-03-01', value: 20 },
        { indicatorId: 'ind-2', date: '2026-05-01', value: 60 },
        { indicatorId: 'ind-2', date: '2026-07-01', value: 110 },
        { indicatorId: 'ind-3', date: '2026-05-01', value: 1 },
        { indicatorId: 'ind-3', date: '2026-07-01', value: 3 },
      ],
    },
    {
      id: 'prj-3',
      name: 'Application mobile terrain',
      description: 'Application de saisie terrain pour les équipes',
      status: 'planifie',
      startDate: '2026-09-01',
      endDate: '2027-03-31',
      progress: 0,
      measures: [],
    },
  ],
  users: [
    { id: 'usr-1', name: 'Alice Martin', email: 'alice.martin@example.com', role: 'admin' },
    { id: 'usr-2', name: 'Benoît Dupont', email: 'benoit.dupont@example.com', role: 'chef_de_projet' },
    { id: 'usr-3', name: 'Chloé Bernard', email: 'chloe.bernard@example.com', role: 'contributeur' },
    { id: 'usr-4', name: 'David Leroy', email: 'david.leroy@example.com', role: 'lecteur' },
  ],
}

interface StoreValue {
  data: AppData
  setProjects: (projects: Project[]) => void
  setIndicators: (indicators: Indicator[]) => void
  setUsers: (users: User[]) => void
  importData: (data: AppData) => void
}

const StoreContext = createContext<StoreValue | null>(null)

function loadData(): AppData {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) return JSON.parse(raw) as AppData
  } catch {
    // ignore corrupted storage and fall back to seed data
  }
  return seedData
}

export function StoreProvider({ children }: { children: ReactNode }) {
  const [data, setData] = useState<AppData>(loadData)

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
  }, [data])

  const value: StoreValue = {
    data,
    setProjects: (projects) => setData((d) => ({ ...d, projects })),
    setIndicators: (indicators) => setData((d) => ({ ...d, indicators })),
    setUsers: (users) => setData((d) => ({ ...d, users })),
    importData: (imported) => setData(imported),
  }

  return <StoreContext.Provider value={value}>{children}</StoreContext.Provider>
}

export function useStore(): StoreValue {
  const ctx = useContext(StoreContext)
  if (!ctx) throw new Error('useStore must be used within StoreProvider')
  return ctx
}

export function newId(prefix: string): string {
  return `${prefix}-${Date.now()}-${Math.floor(Math.random() * 10000)}`
}
