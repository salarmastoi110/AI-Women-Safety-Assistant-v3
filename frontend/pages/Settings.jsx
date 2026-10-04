import { LANGS, VOICE_LANGS } from "../services/i18n.js";
import { useApp } from "../services/AppContext.jsx";

export default function Settings() {
  const { t, settings, setSettings } = useApp();
  return (
    <div className="dash">
      <div className="cell s6">
        <section className="panel form">
          <h3>{t("set_profile")}</h3>
          <label>{t("your_name")}
            <input value={settings.userName} onChange={(e) => setSettings({ userName: e.target.value })} />
          </label>
        </section>

        <section className="panel form">
          <h3>{t("set_alerts")}</h3>
          <label className="check">
            <input type="checkbox" checked={settings.autoTrigger} onChange={(e) => setSettings({ autoTrigger: e.target.checked })} />
            {t("auto_trigger")}
          </label>
          <label>{t("countdown_secs")}: <b>{settings.countdown}</b>
            <input type="range" min="5" max="30" step="1" value={settings.countdown}
              onChange={(e) => setSettings({ countdown: +e.target.value })} />
          </label>
        </section>
      </div>

      <section className="panel form s6">
        <h3>{t("set_language")}</h3>
        <label>{t("ui_language")}
          <div className="seg" role="radiogroup">
            {LANGS.map((l) => (
              <button key={l.code} type="button" role="radio" aria-checked={settings.uiLang === l.code}
                className={settings.uiLang === l.code ? "on" : ""} onClick={() => setSettings({ uiLang: l.code })}>
                {l.label}
              </button>
            ))}
          </div>
        </label>
        <label>{t("voice_language")}
          <select value={settings.voiceLang} onChange={(e) => setSettings({ voiceLang: e.target.value })}>
            {VOICE_LANGS.map((l) => <option key={l.code} value={l.code}>{l.label}</option>)}
          </select>
        </label>
        <p className="muted small">{t("sindhi_note")}</p>
      </section>
    </div>
  );
}
