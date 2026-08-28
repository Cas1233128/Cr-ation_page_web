# Suivi Multi-Projets

Application frontend de suivi multi-projets (React + TypeScript + Vite).

## Fonctionnalités

- **Tableau de bord** : statistiques globales et graphique d'évolution des indicateurs par projet
- **Projets** : création, modification, suppression, avec **import/export JSON**
- **Indicateurs** : gestion des indicateurs (nom, unité, cible) et saisie de mesures datées par projet
- **Rôles** : gestion des utilisateurs et de leurs rôles (administrateur, chef de projet, contributeur, lecteur)

Les données sont persistées dans le `localStorage` du navigateur (aucun backend requis).

## Démarrage

```bash
npm install
npm run dev      # serveur de développement
npm run build    # build de production
npm run lint     # lint (oxlint)
```
