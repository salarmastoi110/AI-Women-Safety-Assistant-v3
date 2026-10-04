import { useApp } from "../services/AppContext.jsx";

const COLORS = { low: "var(--safe)", medium: "var(--warn)", high: "var(--ajrak)", critical: "var(--ajrak-deep)" };

export default function AnalysisCard({ analysis }) {
  const { t } = useApp();
  if (!analysis) return null;
  const { level, threat_score, category, language_detected, matched, actions, summary } = analysis;
  return (
    <section className={"panel analysis lvl-" + level} aria-live="polite">
      <h3>{t("analysis_title")}</h3>
      <p className="summary">{t("cat_" + category)} — <b>{t("level_" + level)}</b></p>
      <div className="meter" role="img" aria-label={`${t("threat")}: ${threat_score}/100`}>
        <div style={{ width: `${threat_score}%`, background: COLORS[level] }} />
      </div>
      <p className="muted small">{t("threat")}: {threat_score}/100 · {t("detected_lang")}: {t("lang_" + language_detected)}</p>
      {matched?.length > 0 && (
        <p className="chips">{matched.slice(0, 6).map((m) => <bdi key={m} className="chip">{m}</bdi>)}</p>
      )}
      {actions?.length > 0 && (
        <>
          <h4>{t("what_to_do")}</h4>
          <ul className="actions">{actions.map((a) => <li key={a}>{a}</li>)}</ul>
        </>
      )}
    </section>
  );
}
