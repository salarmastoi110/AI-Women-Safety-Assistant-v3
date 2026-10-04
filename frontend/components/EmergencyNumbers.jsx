import { EMERGENCY_NUMBERS } from "../services/i18n.js";
import { useApp } from "../services/AppContext.jsx";

export default function EmergencyNumbers() {
  const { t } = useApp();
  return (
    <section className="panel">
      <h3>{t("emergency_numbers")}</h3>
      <div className="numbers">
        {EMERGENCY_NUMBERS.map((n) => (
          <a key={n.number} className="num" href={`tel:${n.number}`}>
            <b dir="ltr">{n.number}</b><span>{t(n.key)}</span>
          </a>
        ))}
      </div>
    </section>
  );
}
