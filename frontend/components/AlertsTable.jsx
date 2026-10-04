import { useApp } from "../services/AppContext.jsx";

const LEVEL_CHIP = { low: "chip-green", medium: "chip-amber", high: "chip-red", critical: "chip-red" };
const LOCALES = { en: "en-GB", ur: "ur-PK", sd: "sd-PK" };

export default function AlertsTable({ alerts, compact = false }) {
  const { t, lang } = useApp();
  const when = (a) => new Date(a.created_at + "Z").toLocaleString(LOCALES[lang] || "en-GB", { dateStyle: "medium", timeStyle: "short" });

  return (
    <div className="tablewrap">
      <table className="tbl">
        <thead>
          <tr>
            <th>{t("col_when")}</th>
            <th>{t("col_type")}</th>
            <th>{t("col_level")}</th>
            <th>{t("col_status")}</th>
            {!compact && <th>{t("col_notified")}</th>}
            {!compact && <th>{t("col_message")}</th>}
            {!compact && <th><span className="sr-only">{t("open_track")}</span></th>}
          </tr>
        </thead>
        <tbody>
          {alerts.map((a) => (
            <tr key={a.id}>
              <td data-label={t("col_when")}>{when(a)}</td>
              <td data-label={t("col_type")}><b>{t("cat_" + a.category)}</b></td>
              <td data-label={t("col_level")}><span className={"chip nm " + (LEVEL_CHIP[a.level] || "")}>{t("level_" + a.level)}</span></td>
              <td data-label={t("col_status")}>
                <span className={"chip nm " + (a.status === "active" ? "chip-red" : "chip-green")}>
                  {a.status === "active" ? t("status_active") : t("status_resolved")}
                </span>
              </td>
              {!compact && <td data-label={t("col_notified")}>{a.notified}</td>}
              {!compact && <td data-label={t("col_message")} className="msg">{a.message ? <bdi>{a.message}</bdi> : <span className="muted">—</span>}</td>}
              {!compact && (
                <td>
                  <a className="link" href={a.track_url} target="_blank" rel="noreferrer">{t("open_track")}</a>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
