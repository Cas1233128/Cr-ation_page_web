# Suivi Multiprojets — Backend

API REST (Express + TypeScript + SQLite) pour l'application de suivi multiprojets.

## Démarrage

```bash
npm install
npm run dev      # développement (tsx watch), port 3001
npm run build    # compilation TypeScript
npm start        # exécution du build
```

Variables d'environnement : `PORT` (défaut 3001), `DB_PATH` (défaut `./data.sqlite`).

## Endpoints

### Projets
- `GET /api/projects` — liste des projets
- `POST /api/projects` — créer un projet
- `GET /api/projects/:id` / `PUT /api/projects/:id` / `DELETE /api/projects/:id`
- `GET /api/projects/export?format=json|csv` — export des projets
- `POST /api/projects/import` — import (JSON dans le corps ou fichier `file` en multipart) ; met à jour les projets existants par id

### Rôles (page de gestion des rôles)
- `GET /api/roles`, `POST /api/roles`, `PUT /api/roles/:id`, `DELETE /api/roles/:id`
- Un rôle : `{ name, description, permissions: string[] }`

### Utilisateurs
- `GET /api/users`, `POST /api/users`, `PUT /api/users/:id`, `DELETE /api/users/:id`
- Un utilisateur : `{ name, email, roleId }`

### Indicateurs (page de gestion des indicateurs)
- `GET /api/indicators`, `POST /api/indicators`, `PUT /api/indicators/:id`, `DELETE /api/indicators/:id`
- Valeurs (évolution) : `GET /api/indicators/:id/values?projectId=...`,
  `POST /api/indicators/:id/values` (`{ projectId?, date, value }`),
  `DELETE /api/indicators/:id/values/:valueId`

### Tableau de bord
- `GET /api/dashboard?projectId=...` — statistiques projets (par statut, avancement moyen, budget total)
  et séries temporelles d'évolution de chaque indicateur (`indicatorSeries`), prêtes à tracer côté frontend.

Des rôles par défaut (Administrateur, Chef de projet, Lecteur) et un utilisateur admin sont créés au premier lancement.
