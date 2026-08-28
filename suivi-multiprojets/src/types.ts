export type ProjectStatus = 'en_cours' | 'termine' | 'en_pause' | 'planifie'

export interface Indicator {
  id: string
  name: string
  unit: string
  description: string
  target: number
}

export interface IndicatorMeasure {
  indicatorId: string
  date: string // ISO date (YYYY-MM-DD)
  value: number
}

export interface Project {
  id: string
  name: string
  description: string
  status: ProjectStatus
  startDate: string
  endDate: string
  progress: number // 0-100
  measures: IndicatorMeasure[]
}

export type Role = 'admin' | 'chef_de_projet' | 'contributeur' | 'lecteur'

export interface User {
  id: string
  name: string
  email: string
  role: Role
}

export interface AppData {
  projects: Project[]
  indicators: Indicator[]
  users: User[]
}

export const STATUS_LABELS: Record<ProjectStatus, string> = {
  en_cours: 'En cours',
  termine: 'Terminé',
  en_pause: 'En pause',
  planifie: 'Planifié',
}

export const ROLE_LABELS: Record<Role, string> = {
  admin: 'Administrateur',
  chef_de_projet: 'Chef de projet',
  contributeur: 'Contributeur',
  lecteur: 'Lecteur',
}

export const ROLE_DESCRIPTIONS: Record<Role, string> = {
  admin: 'Accès complet : gestion des projets, indicateurs et utilisateurs',
  chef_de_projet: 'Création et modification des projets et de leurs indicateurs',
  contributeur: 'Saisie des mesures d’indicateurs sur les projets assignés',
  lecteur: 'Consultation seule du tableau de bord et des projets',
}
