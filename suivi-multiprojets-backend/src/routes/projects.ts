import { Router } from "express";
import multer from "multer";
import { z } from "zod";
import { db, newId } from "../db.js";

const router = Router();
const upload = multer({ storage: multer.memoryStorage(), limits: { fileSize: 5 * 1024 * 1024 } });

const projectSchema = z.object({
  name: z.string().min(1),
  description: z.string().default(""),
  status: z.enum(["en_cours", "termine", "en_pause", "annule"]).default("en_cours"),
  startDate: z.string().nullable().default(null),
  endDate: z.string().nullable().default(null),
  budget: z.number().nullable().default(null),
  progress: z.number().min(0).max(100).default(0),
  manager: z.string().default(""),
});

type ProjectRow = {
  id: string;
  name: string;
  description: string;
  status: string;
  start_date: string | null;
  end_date: string | null;
  budget: number | null;
  progress: number;
  manager: string;
};

function toApi(row: ProjectRow) {
  return {
    id: row.id,
    name: row.name,
    description: row.description,
    status: row.status,
    startDate: row.start_date,
    endDate: row.end_date,
    budget: row.budget,
    progress: row.progress,
    manager: row.manager,
  };
}

router.get("/", (_req, res) => {
  const rows = db.prepare("SELECT * FROM projects ORDER BY name").all() as ProjectRow[];
  res.json(rows.map(toApi));
});

router.get("/export", (req, res) => {
  const rows = db.prepare("SELECT * FROM projects ORDER BY name").all() as ProjectRow[];
  const projects = rows.map(toApi);
  const format = String(req.query.format ?? "json");
  if (format === "csv") {
    const header = "id;name;description;status;startDate;endDate;budget;progress;manager";
    const escape = (v: unknown) => {
      const s = v === null || v === undefined ? "" : String(v);
      return /[;"\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
    };
    const lines = projects.map((p) =>
      [p.id, p.name, p.description, p.status, p.startDate, p.endDate, p.budget, p.progress, p.manager]
        .map(escape)
        .join(";")
    );
    res.setHeader("Content-Type", "text/csv; charset=utf-8");
    res.setHeader("Content-Disposition", "attachment; filename=projets.csv");
    res.send([header, ...lines].join("\n"));
    return;
  }
  res.setHeader("Content-Disposition", "attachment; filename=projets.json");
  res.json(projects);
});

router.post("/import", upload.single("file"), (req, res) => {
  let payload: unknown;
  if (req.file) {
    try {
      payload = JSON.parse(req.file.buffer.toString("utf-8"));
    } catch {
      res.status(400).json({ error: "Fichier JSON invalide" });
      return;
    }
  } else {
    payload = req.body;
  }
  const parsed = z.array(projectSchema.extend({ id: z.string().optional() })).safeParse(payload);
  if (!parsed.success) {
    res.status(400).json({ error: "Format de projets invalide", details: parsed.error.issues });
    return;
  }

  const upsert = db.prepare(`
    INSERT INTO projects (id, name, description, status, start_date, end_date, budget, progress, manager)
    VALUES (@id, @name, @description, @status, @startDate, @endDate, @budget, @progress, @manager)
    ON CONFLICT(id) DO UPDATE SET
      name=excluded.name, description=excluded.description, status=excluded.status,
      start_date=excluded.start_date, end_date=excluded.end_date, budget=excluded.budget,
      progress=excluded.progress, manager=excluded.manager
  `);
  const importAll = db.transaction((projects: (z.infer<typeof projectSchema> & { id?: string })[]) => {
    let created = 0;
    let updated = 0;
    for (const p of projects) {
      const id = p.id ?? newId();
      const existing = p.id
        ? db.prepare("SELECT id FROM projects WHERE id = ?").get(p.id)
        : undefined;
      upsert.run({ ...p, id });
      if (existing) updated += 1;
      else created += 1;
    }
    return { created, updated };
  });
  const result = importAll(parsed.data);
  res.status(201).json({ imported: parsed.data.length, ...result });
});

router.get("/:id", (req, res) => {
  const row = db.prepare("SELECT * FROM projects WHERE id = ?").get(req.params.id) as ProjectRow | undefined;
  if (!row) {
    res.status(404).json({ error: "Projet introuvable" });
    return;
  }
  res.json(toApi(row));
});

router.post("/", (req, res) => {
  const parsed = projectSchema.safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json({ error: "Données invalides", details: parsed.error.issues });
    return;
  }
  const id = newId();
  db.prepare(`
    INSERT INTO projects (id, name, description, status, start_date, end_date, budget, progress, manager)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
  `).run(
    id,
    parsed.data.name,
    parsed.data.description,
    parsed.data.status,
    parsed.data.startDate,
    parsed.data.endDate,
    parsed.data.budget,
    parsed.data.progress,
    parsed.data.manager
  );
  const row = db.prepare("SELECT * FROM projects WHERE id = ?").get(id) as ProjectRow;
  res.status(201).json(toApi(row));
});

router.put("/:id", (req, res) => {
  const existing = db.prepare("SELECT * FROM projects WHERE id = ?").get(req.params.id) as ProjectRow | undefined;
  if (!existing) {
    res.status(404).json({ error: "Projet introuvable" });
    return;
  }
  const parsed = projectSchema.partial().safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json({ error: "Données invalides", details: parsed.error.issues });
    return;
  }
  const merged = { ...toApi(existing), ...parsed.data };
  db.prepare(`
    UPDATE projects SET name=?, description=?, status=?, start_date=?, end_date=?, budget=?, progress=?, manager=?
    WHERE id=?
  `).run(
    merged.name,
    merged.description,
    merged.status,
    merged.startDate,
    merged.endDate,
    merged.budget,
    merged.progress,
    merged.manager,
    req.params.id
  );
  const row = db.prepare("SELECT * FROM projects WHERE id = ?").get(req.params.id) as ProjectRow;
  res.json(toApi(row));
});

router.delete("/:id", (req, res) => {
  const result = db.prepare("DELETE FROM projects WHERE id = ?").run(req.params.id);
  if (result.changes === 0) {
    res.status(404).json({ error: "Projet introuvable" });
    return;
  }
  res.status(204).end();
});

export default router;
