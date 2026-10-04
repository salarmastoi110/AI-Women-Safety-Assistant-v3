import { useEffect, useRef, useState } from "react";
import { api } from "../services/api.js";
import { useApp } from "../services/AppContext.jsx";

const SR = typeof window !== "undefined" ? window.SpeechRecognition || window.webkitSpeechRecognition : null;

export default function VoiceGuard({ onAnalysis }) {
  const { t, lang, settings } = useApp();
  const [on, setOn] = useState(false);
  const [heard, setHeard] = useState("");
  const [note, setNote] = useState("");
  const [typed, setTyped] = useState("");

  const recRef = useRef(null);
  const activeRef = useRef(false);
  const langRef = useRef(settings.voiceLang);
  const cbRef = useRef(onAnalysis);
  const lastRun = useRef({ text: "", at: 0 });
  cbRef.current = onAnalysis;

  const run = async (text) => {
    text = (text || "").trim();
    if (text.length < 2) return;
    const now = Date.now();
    if (text === lastRun.current.text && now - lastRun.current.at < 3000) return;
    lastRun.current = { text, at: now };
    try {
      const res = await api.analyze({ text, hour: new Date().getHours(), is_alone: true, lang });
      cbRef.current?.(res, text);
    } catch { setNote(t("api_error")); }
  };

  const begin = (code) => {
    if (!SR) return;
    langRef.current = code;
    const r = new SR();
    r.lang = code; r.continuous = true; r.interimResults = true;
    let lastInterim = 0;
    r.onresult = (e) => {
      for (let i = e.resultIndex; i < e.results.length; i++) {
        const res = e.results[i];
        const text = res[0].transcript;
        setHeard(text);
        const now = Date.now();
        if (res.isFinal || now - lastInterim > 1500) { lastInterim = now; run(text); }
      }
    };
    r.onerror = (e) => {
      if (e.error === "not-allowed" || e.error === "service-not-allowed") { setNote(t("mic_denied")); stop(); }
      else if (e.error === "language-not-supported" && code !== "ur-PK") { setNote(t("lang_fallback")); r.onend = null; begin("ur-PK"); }
      else if (e.error === "network") setNote(t("net_error"));
    };
    r.onend = () => { if (activeRef.current) setTimeout(() => activeRef.current && begin(langRef.current), 300); };
    recRef.current = r;
    try { r.start(); } catch { /* already started */ }
  };

  const start = () => { setNote(""); activeRef.current = true; setOn(true); begin(settings.voiceLang); };
  function stop() { activeRef.current = false; setOn(false); try { recRef.current?.stop(); } catch { /* ignore */ } }
  useEffect(() => () => { activeRef.current = false; try { recRef.current?.abort(); } catch { /* ignore */ } }, []);

  return (
    <section className="panel voice">
      <div className="row between">
        <h3>{t("voice_guard")}</h3>
        <span className={"dot " + (on ? "live" : "")} aria-hidden="true" />
      </div>
      <p className="muted" aria-live="polite">{SR ? (on ? t("voice_listening") : t("voice_idle")) : t("voice_unsupported")}</p>
      {SR && (
        <button className={"btn " + (on ? "ghost" : "primary")} onClick={on ? stop : start}>
          {on ? t("voice_stop") : t("voice_start")}
        </button>
      )}
      {heard && <p className="heard"><span className="muted">{t("heard")}:</span> <bdi>{heard}</bdi></p>}
      {note && <p className="warn" role="status">{note}</p>}

      <details className="test">
        <summary>{t("test_title")}</summary>
        <div className="row gap">
          <input value={typed} onChange={(e) => setTyped(e.target.value)} placeholder={t("test_placeholder")}
                 onKeyDown={(e) => e.key === "Enter" && (run(typed), setHeard(typed))} />
          <button className="btn" onClick={() => { setHeard(typed); run(typed); }}>{t("test_button")}</button>
        </div>
      </details>
    </section>
  );
}
