import { Router } from "express";
import { z } from "zod";
import { db, newId } from "../db.js";

const router = Router();

const userSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  roleId: z.string().nullable().default(null),
});

type UserRow = { id: string; name: string; email: string; role_id: string | null; role_name?: string | null };

function toApi(row: UserRow) {
  return {
    id: row.id,
    name: row.name,
    email: row.email,
    roleId: row.role_id,
    roleName: row.role_name ?? null,
  };
}

const selectUser = `
  SELECT u.*, r.name AS role_name
  FROM users u LEFT JOIN roles r ON r.id = u.role_id
`;

function roleExists(roleId: string | null): boolean {
  if (roleId === null) return true;
  return Boolean(db.prepare("SELECT id FROM roles WHERE id = ?").get(roleId));
}

router.get("/", (_req, res) => {
  const rows = db.prepare(`${selectUser} ORDER BY u.name`).all() as UserRow[];
  res.json(rows.map(toApi));
});

router.post("/", (req, res) => {
  const parsed = userSchema.safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json({ error: "Données invalides", details: parsed.error.issues });
    return;
  }
  if (!roleExists(parsed.data.roleId)) {
    res.status(400).json({ error: "Rôle introuvable" });
    return;
  }
  const id = newId();
  try {
    db.prepare("INSERT INTO users (id, name, email, role_id) VALUES (?, ?, ?, ?)").run(
      id,
      parsed.data.name,
      parsed.data.email,
      parsed.data.roleId
    );
  } catch {
    res.status(409).json({ error: "Un utilisateur avec cet email existe déjà" });
    return;
  }
  const row = db.prepare(`${selectUser} WHERE u.id = ?`).get(id) as UserRow;
  res.status(201).json(toApi(row));
});

router.put("/:id", (req, res) => {
  const existing = db.prepare(`${selectUser} WHERE u.id = ?`).get(req.params.id) as UserRow | undefined;
  if (!existing) {
    res.status(404).json({ error: "Utilisateur introuvable" });
    return;
  }
  const parsed = userSchema.partial().safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json({ error: "Données invalides", details: parsed.error.issues });
    return;
  }
  const merged = { ...toApi(existing), ...parsed.data };
  if (!roleExists(merged.roleId)) {
    res.status(400).json({ error: "Rôle introuvable" });
    return;
  }
  try {
    db.prepare("UPDATE users SET name=?, email=?, role_id=? WHERE id=?").run(
      merged.name,
      merged.email,
      merged.roleId,
      req.params.id
    );
  } catch {
    res.status(409).json({ error: "Un utilisateur avec cet email existe déjà" });
    return;
  }
  const row = db.prepare(`${selectUser} WHERE u.id = ?`).get(req.params.id) as UserRow;
  res.json(toApi(row));
});

router.delete("/:id", (req, res) => {
  const result = db.prepare("DELETE FROM users WHERE id = ?").run(req.params.id);
  if (result.changes === 0) {
    res.status(404).json({ error: "Utilisateur introuvable" });
    return;
  }
  res.status(204).end();
});

export default router;
