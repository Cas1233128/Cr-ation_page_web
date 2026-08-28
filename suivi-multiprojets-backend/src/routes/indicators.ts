import { Router } from "express";
import { z } from "zod";
import { db, newId } from "../db.js";

const router = Router();

const indicatorSchema = z.object({
  name: z.string().min(1),
  description: z.string().default(""),
  unit: z.string().default(""),
  target: z.number().nullable().default(null),
});

const valueSchema = z.object({
  projectId: z.string().nullable().default(null),
  date: z.string().min(1),
  value: z.number(),
});

type IndicatorRow = {
  id: string;
  name: string;
  description: string;
  unit: string;
  target: number | null;
};

type ValueRow = {
  id: string;
  indicator_id: string;
  project_id: string | null;
  date: string;
  value: number;
};

function valueToApi(row: ValueRow) {
  return {
    id: row.id,
    indicatorId: row.indicator_id,
    projectId: row.project_id,
    date: row.date,
    value: row.value,
  };
}

router.get("/", (_req, res) => {
  const rows = db.prepare("SELECT * FROM indicators ORDER BY name").all() as IndicatorRow[];
  res.json(rows);
});

router.post("/", (req, res) => {
  const parsed = indicatorSchema.safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json({ error: "Données invalides", details: parsed.error.issues });
    return;
  }
  const id = newId();
  db.prepare("INSERT INTO indicators (id, name, description, unit, target) VALUES (?, ?, ?, ?, ?)").run(
    id,
    parsed.data.name,
    parsed.data.description,
    parsed.data.unit,
    parsed.data.target
  );
  const row = db.prepare("SELECT * FROM indicators WHERE id = ?").get(id) as IndicatorRow;
  res.status(201).json(row);
});

router.put("/:id", (req, res) => {
  const existing = db.prepare("SELECT * FROM indicators WHERE id = ?").get(req.params.id) as IndicatorRow | undefined;
  if (!existing) {
    res.status(404).json({ error: "Indicateur introuvable" });
    return;
  }
  const parsed = indicatorSchema.partial().safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json({ error: "Données invalides", details: parsed.error.issues });
    return;
  }
  const merged = { ...existing, ...parsed.data };
  db.prepare("UPDATE indicators SET name=?, description=?, unit=?, target=? WHERE id=?").run(
    merged.name,
    merged.description,
    merged.unit,
    merged.target,
    req.params.id
  );
  const row = db.prepare("SELECT * FROM indicators WHERE id = ?").get(req.params.id) as IndicatorRow;
  res.json(row);
});

router.delete("/:id", (req, res) => {
  const result = db.prepare("DELETE FROM indicators WHERE id = ?").run(req.params.id);
  if (result.changes === 0) {
    res.status(404).json({ error: "Indicateur introuvable" });
    return;
  }
  res.status(204).end();
});

router.get("/:id/values", (req, res) => {
  const indicator = db.prepare("SELECT id FROM indicators WHERE id = ?").get(req.params.id);
  if (!indicator) {
    res.status(404).json({ error: "Indicateur introuvable" });
    return;
  }
  const projectId = req.query.projectId ? String(req.query.projectId) : null;
  const rows = (
    projectId
      ? db
          .prepare("SELECT * FROM indicator_values WHERE indicator_id = ? AND project_id = ? ORDER BY date")
          .all(req.params.id, projectId)
      : db.prepare("SELECT * FROM indicator_values WHERE indicator_id = ? ORDER BY date").all(req.params.id)
  ) as ValueRow[];
  res.json(rows.map(valueToApi));
});

router.post("/:id/values", (req, res) => {
  const indicator = db.prepare("SELECT id FROM indicators WHERE id = ?").get(req.params.id);
  if (!indicator) {
    res.status(404).json({ error: "Indicateur introuvable" });
    return;
  }
  const parsed = valueSchema.safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json({ error: "Données invalides", details: parsed.error.issues });
    return;
  }
  if (parsed.data.projectId) {
    const project = db.prepare("SELECT id FROM projects WHERE id = ?").get(parsed.data.projectId);
    if (!project) {
      res.status(400).json({ error: "Projet introuvable" });
      return;
    }
  }
  const id = newId();
  db.prepare(
    "INSERT INTO indicator_values (id, indicator_id, project_id, date, value) VALUES (?, ?, ?, ?, ?)"
  ).run(id, req.params.id, parsed.data.projectId, parsed.data.date, parsed.data.value);
  const row = db.prepare("SELECT * FROM indicator_values WHERE id = ?").get(id) as ValueRow;
  res.status(201).json(valueToApi(row));
});

router.delete("/:id/values/:valueId", (req, res) => {
  const result = db
    .prepare("DELETE FROM indicator_values WHERE id = ? AND indicator_id = ?")
    .run(req.params.valueId, req.params.id);
  if (result.changes === 0) {
    res.status(404).json({ error: "Valeur introuvable" });
    return;
  }
  res.status(204).end();
});

export default router;
