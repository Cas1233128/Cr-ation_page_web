import { HashRouter, NavLink, Route, Routes } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Projects from './pages/Projects'
import Roles from './pages/Roles'
import Indicators from './pages/Indicators'
import { StoreProvider } from './store'
import './App.css'

export default function App() {
  return (
    <StoreProvider>
      <HashRouter>
        <div className="layout">
          <aside className="sidebar">
            <div className="brand">Suivi Multi-Projets</div>
            <nav>
              <NavLink to="/" end>
                Tableau de bord
              </NavLink>
              <NavLink to="/projets">Projets</NavLink>
              <NavLink to="/indicateurs">Indicateurs</NavLink>
              <NavLink to="/roles">Rôles</NavLink>
            </nav>
          </aside>
          <main className="content">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/projets" element={<Projects />} />
              <Route path="/indicateurs" element={<Indicators />} />
              <Route path="/roles" element={<Roles />} />
            </Routes>
          </main>
        </div>
      </HashRouter>
    </StoreProvider>
  )
}
