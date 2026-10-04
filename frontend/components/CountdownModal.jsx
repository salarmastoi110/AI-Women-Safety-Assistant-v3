import { useEffect, useRef, useState } from "react";
import { useApp } from "../services/AppContext.jsx";

export default function CountdownModal({ seconds, source, onCancel, onConfirm }) {
  const { t } = useApp();
  const [left, setLeft] = useState(seconds);
  const fired = useRef(false);

  useEffect(() => {
    const id = setInterval(() => setLeft((s) => s - 1), 1000);
    const esc = (e) => e.key === "Escape" && onCancel();
    window.addEventListener("keydown", esc);
    return () => { clearInterval(id); window.removeEventListener("keydown", esc); };
  }, []);

  useEffect(() => {
    try { navigator.vibrate?.(left > 0 ? 120 : [300, 100, 300]); } catch { /* ignore */ }
    if (left <= 0 && !fired.current) { fired.current = true; onConfirm(); }
  }, [left]);

  const R = 54, C = 2 * Math.PI * R;
  const frac = Math.max(0, left) / seconds;

  return (
    <div className="modal" role="alertdialog" aria-modal="true" aria-labelledby="cd-title">
      <div className="modal-card">
        <h2 id="cd-title">{source === "voice" ? t("countdown_voice") : t("countdown_manual")}</h2>
        <div className="ring" aria-live="assertive">
          <svg viewBox="0 0 120 120" width="160" height="160">
            <circle cx="60" cy="60" r={R} className="ring-bg" />
            <circle cx="60" cy="60" r={R} className="ring-fg" strokeDasharray={C} strokeDashoffset={C * (1 - frac)} />
          </svg>
          <span className="ring-num">{Math.max(0, left)}</span>
        </div>
        <p>{t("countdown_body")} <b>{Math.max(0, left)}</b> {t("seconds")}</p>
        <button className="btn big ghost" autoFocus onClick={onCancel}>{t("cancel")}</button>
        <button className="btn big danger" onClick={() => { if (!fired.current) { fired.current = true; onConfirm(); } }}>
          {t("send_now")}
        </button>
      </div>
    </div>
  );
}
