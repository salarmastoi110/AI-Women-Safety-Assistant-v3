import { useApp } from "../services/AppContext.jsx";

const COLORS = { low: "var(--safe)", medium: "var(--warn)", high: "var(--ajrak)" };

export default function RiskMeter({ risk }) {
  const { t } = useApp();
  if (!risk) return null;
  return (
    <div className="panel">
      <b>{t("risk_score")}: {t("level_" + risk.level)} ({risk.score}/100)</b>
      <div className="meter"><div style={{ width: `${risk.score}%`, background: COLORS[risk.level] }} /></div>
      {risk.reasons.length > 0 && <p className="muted small">{risk.reasons.map((r) => t("reason_" + r)).join(" · ")}</p>}
    </div>
  );
}
