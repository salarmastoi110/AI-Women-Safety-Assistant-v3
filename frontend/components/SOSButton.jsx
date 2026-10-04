import { useApp } from "../services/AppContext.jsx";

export default function SOSButton({ onPress, disabled }) {
  const { t } = useApp();
  return (
    <div className="sos-wrap">
      <button className="sos" onClick={onPress} disabled={disabled} aria-label={t("sos") + " — " + t("sos_hint")}>
        <span className="sos-label">{t("sos")}</span>
      </button>
      <p className="sos-hint">{t("sos_hint")}</p>
    </div>
  );
}
