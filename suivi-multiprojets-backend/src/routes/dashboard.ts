import { Router } from "express";
import { db } from "../db.js";

const router = Router();

type CountRow = { status: string; c: number };
type SeriesRow = {
  indicator_id: string;
  indicator_name: string;
  unit: string;
  target: number | null;
  date: string;
  avg_value: number;
};

router.get("/", (req, res) => {
  const projectId = req.query.projectId ? String(req.query.projectId) : null;

  const statusCounts = db
    .prepare("SELECT status, COUNT(*) AS c FROM projects GROUP BY status")
    .all() as CountRow[];
  const totals = db
    .prepare("SELECT COUNT(*) AS projects, COALESCE(AVG(progress), 0) AS avgProgress, COALESCE(SUM(budget), 0) AS totalBudget FROM projects")
    .get() as { projects: number; avgProgress: number; totalBudget: number };
  const counts = {
    users: (db.prepare("SELECT COUNT(*) AS c FROM users").get() as { c: number }).c,
    roles: (db.prepare("SELECT COUNT(*) AS c FROM roles").get() as { c: number }).c,
    indicators: (db.prepare("SELECT COUNT(*) AS c FROM indicators").get() as { c: number }).c,
  };

  const seriesRows = (
    projectId
      ? db
          .prepare(`
            SELECT i.id AS indicator_id, i.name AS indicator_name, i.unit, i.target,
                   v.date, AVG(v.value) AS avg_value
            FROM indicator_values v JOIN indicators i ON i.id = v.indicator_id
            WHERE v.project_id = ?
            GROUP BY i.id, v.date ORDER BY i.name, v.date
          `)
          .all(projectId)
      : db
          .prepare(`
            SELECT i.id AS indicator_id, i.name AS indicator_name, i.unit, i.target,
                   v.date, AVG(v.value) AS avg_value
            FROM indicator_values v JOIN indicators i ON i.id = v.indicator_id
            GROUP BY i.id, v.date ORDER BY i.name, v.date
          `)
          .all()
  ) as SeriesRow[];

  const seriesMap = new Map<
    string,
    { indicatorId: string; name: string; unit: string; target: number | null; points: { date: string; value: number }[] }
  >();
  for (const row of seriesRows) {
    let entry = seriesMap.get(row.indicator_id);
    if (!entry) {
      entry = {
        indicatorId: row.indicator_id,
        name: row.indicator_name,
        unit: row.unit,
        target: row.target,
        points: [],
      };
      seriesMap.set(row.indicator_id, entry);
    }
    entry.points.push({ date: row.date, value: row.avg_value });
  }

  res.json({
    projects: {
      total: totals.projects,
      averageProgress: totals.avgProgress,
      totalBudget: totals.totalBudget,
      byStatus: Object.fromEntries(statusCounts.map((r) => [r.status, r.c])),
    },
    counts,
    indicatorSeries: [...seriesMap.values()],
  });
});

export default router;
