import { useEffect, useState } from "react";
import { api } from "../services/api.js";
import { useApp } from "../services/AppContext.jsx";
import AlertsTable from "../components/AlertsTable.jsx";

export default function History() {
  const { t } = useApp();
  const [alerts, setAlerts] = useState(null);
  const [filter, setFilter] = useState("all");
  useEffect(() => { api.alerts().then(setAlerts).catch(() => setAlerts([])); }, []);

  if (alerts === null) return null;
  const shown = filter === "all" ? alerts : alerts.filter((a) => (filter === "active" ? a.status === "active" : a.status !== "active"));
  const FILTERS = [["all", t("filter_all")], ["active", t("status_active")], ["resolved", t("status_resolved")]];

  return (
    <section className="panel tablepanel">
      <div className="panel-head end">
        <div className="seg" role="radiogroup" aria-label={t("col_status")}>
          {FILTERS.map(([k, label]) => (
            <button key={k} role="radio" aria-checked={filter === k} className={filter === k ? "on" : ""} onClick={() => setFilter(k)}>{label}</button>
          ))}
        </div>
      </div>
      {shown.length === 0 ? <p className="empty muted">{t("history_empty")}</p> : <AlertsTable alerts={shown} />}
    </section>
  );
}
