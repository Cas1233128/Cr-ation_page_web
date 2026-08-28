import express from "express";
import cors from "cors";
import projectsRouter from "./routes/projects.js";
import rolesRouter from "./routes/roles.js";
import usersRouter from "./routes/users.js";
import indicatorsRouter from "./routes/indicators.js";
import dashboardRouter from "./routes/dashboard.js";

const app = express();
app.use(cors());
app.use(express.json({ limit: "5mb" }));

app.get("/api/health", (_req, res) => {
  res.json({ status: "ok" });
});

app.use("/api/projects", projectsRouter);
app.use("/api/roles", rolesRouter);
app.use("/api/users", usersRouter);
app.use("/api/indicators", indicatorsRouter);
app.use("/api/dashboard", dashboardRouter);

const port = Number(process.env.PORT ?? 3001);
app.listen(port, () => {
  console.log(`Suivi multiprojets API démarrée sur le port ${port}`);
});
