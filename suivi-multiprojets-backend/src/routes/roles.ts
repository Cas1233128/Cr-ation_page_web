import { Router } from "express";
import { z } from "zod";
import { db, newId } from "../db.js";

const router = Router();

const roleSchema = z.object({
  name: z.string().min(1),
  description: z.string().default(""),
  permissions: z.array(z.string()).default([]),
});

type RoleRow = { id: string; name: string; description: string; permissions: string };

function toApi(row: RoleRow) {
  return {
    id: row.id,
    name: row.name,
    description: row.description,
    permissions: JSON.parse(row.permissions) as string[],
  };
}

router.get("/", (_req, res) => {
  const rows = db.prepare("SELECT * FROM roles ORDER BY name").all() as RoleRow[];
  res.json(rows.map(toApi));
});

router.post("/", (req, res) => {
  const parsed = roleSchema.safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json({ error: "Données invalides", details: parsed.error.issues });
    return;
  }
  const id = newId();
  try {
    db.prepare("INSERT INTO roles (id, name, description, permissions) VALUES (?, ?, ?, ?)").run(
      id,
      parsed.data.name,
      parsed.data.description,
      JSON.stringify(parsed.data.permissions)
    );
  } catch {
    res.status(409).json({ error: "Un rôle avec ce nom existe déjà" });
    return;
  }
  const row = db.prepare("SELECT * FROM roles WHERE id = ?").get(id) as RoleRow;
  res.status(201).json(toApi(row));
});

router.put("/:id", (req, res) => {
  const existing = db.prepare("SELECT * FROM roles WHERE id = ?").get(req.params.id) as RoleRow | undefined;
  if (!existing) {
    res.status(404).json({ error: "Rôle introuvable" });
    return;
  }
  const parsed = roleSchema.partial().safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json({ error: "Données invalides", details: parsed.error.issues });
    return;
  }
  const merged = { ...toApi(existing), ...parsed.data };
  try {
    db.prepare("UPDATE roles SET name=?, description=?, permissions=? WHERE id=?").run(
      merged.name,
      merged.description,
      JSON.stringify(merged.permissions),
      req.params.id
    );
  } catch {
    res.status(409).json({ error: "Un rôle avec ce nom existe déjà" });
    return;
  }
  const row = db.prepare("SELECT * FROM roles WHERE id = ?").get(req.params.id) as RoleRow;
  res.json(toApi(row));
});

router.delete("/:id", (req, res) => {
  const result = db.prepare("DELETE FROM roles WHERE id = ?").run(req.params.id);
  if (result.changes === 0) {
    res.status(404).json({ error: "Rôle introuvable" });
    return;
  }
  res.status(204).end();
});

export default router;
