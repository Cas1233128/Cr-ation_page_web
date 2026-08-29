import Database from "better-sqlite3";
import path from "path";
import { randomUUID } from "crypto";

const dbPath = process.env.DB_PATH ?? path.join(process.cwd(), "data.sqlite");
export const db = new Database(dbPath);
db.pragma("journal_mode = WAL");
db.pragma("foreign_keys = ON");

db.exec(`
CREATE TABLE IF NOT EXISTS roles (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  description TEXT NOT NULL DEFAULT '',
  permissions TEXT NOT NULL DEFAULT '[]'
);

CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  role_id TEXT REFERENCES roles(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS projects (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL DEFAULT 'en_cours',
  start_date TEXT,
  end_date TEXT,
  budget REAL,
  progress REAL NOT NULL DEFAULT 0,
  manager TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS indicators (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT NOT NULL DEFAULT '',
  unit TEXT NOT NULL DEFAULT '',
  target REAL
);

CREATE TABLE IF NOT EXISTS indicator_values (
  id TEXT PRIMARY KEY,
  indicator_id TEXT NOT NULL REFERENCES indicators(id) ON DELETE CASCADE,
  project_id TEXT REFERENCES projects(id) ON DELETE CASCADE,
  date TEXT NOT NULL,
  value REAL NOT NULL
);
`);

export function newId(): string {
  return randomUUID();
}

function seed() {
  const roleCount = db.prepare("SELECT COUNT(*) AS c FROM roles").get() as { c: number };
  if (roleCount.c > 0) return;

  const insertRole = db.prepare(
    "INSERT INTO roles (id, name, description, permissions) VALUES (?, ?, ?, ?)"
  );
  const adminId = newId();
  insertRole.run(
    adminId,
    "Administrateur",
    "Accès complet à l'application",
    JSON.stringify(["projects:read", "projects:write", "indicators:read", "indicators:write", "users:manage", "roles:manage"])
  );
  const managerId = newId();
  insertRole.run(
    managerId,
    "Chef de projet",
    "Gestion des projets et des indicateurs",
    JSON.stringify(["projects:read", "projects:write", "indicators:read", "indicators:write"])
  );
  insertRole.run(
    newId(),
    "Lecteur",
    "Consultation uniquement",
    JSON.stringify(["projects:read", "indicators:read"])
  );

  db.prepare("INSERT INTO users (id, name, email, role_id) VALUES (?, ?, ?, ?)").run(
    newId(),
    "Admin",
    "admin@example.com",
    adminId
  );
}

seed();
