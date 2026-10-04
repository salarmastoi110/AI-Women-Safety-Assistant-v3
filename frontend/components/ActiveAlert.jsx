import { useEffect, useRef, useState } from "react";
import { api } from "../services/api.js";
import { useApp } from "../services/AppContext.jsx";

export default function ActiveAlert({ alert, onGoContacts, onDone }) {
  const { t } = useApp();
  const [copied, setCopied] = useState(false);
  const [safe, setSafe] = useState(alert.status === "resolved");
  const lastPush = useRef(0);

  // keep pushing live location to the tracking page while the alert is active
  useEffect(() => {
    if (safe || !navigator.geolocation) return;
    const id = navigator.geolocation.watchPosition((p) => {
      const now = Date.now();
      if (now - lastPush.current < 15000) return;
      lastPush.current = now;
      api.pushLocation(alert.token, p.coords.latitude, p.coords.longitude).catch(() => {});
    }, () => {}, { enableHighAccuracy: true, maximumAge: 5000 });
    return () => navigator.geolocation.clearWatch(id);
  }, [alert.token, safe]);

  const copy = async () => {
    try { await navigator.clipboard.writeText(alert.track_url); setCopied(true); setTimeout(() => setCopied(false), 1500); } catch { /* ignore */ }
  };
  const markSafe = async () => { await api.resolve(alert.token); setSafe(true); };

  return (
    <section className={"panel active-alert " + (safe ? "safe" : "")} role="status">
      <h3>{safe ? t("safe_done") : t("alert_active")}</h3>
      <p>{t("notified_n", { n: alert.notified })}</p>
      {alert.notified === 0 && (
        <p className="warn">{t("no_contacts_warn")} <button className="link" onClick={onGoContacts}>{t("add_contacts")}</button></p>
      )}
      {!safe && <p className="live"><span className="dot live" /> {t("sharing_location")}</p>}
      <p className="small muted">{t("tracking_link")}:</p>
      <div className="row gap">
        <input readOnly value={alert.track_url} dir="ltr" onFocus={(e) => e.target.select()} />
        <button className="btn" onClick={copy}>{copied ? t("copied") : t("copy")}</button>
      </div>
      <div className="row gap wrap mt">
        {!safe && <button className="btn big safe-btn" onClick={markSafe}>{t("im_safe")}</button>}
        {safe && <button className="btn" onClick={onDone}>OK</button>}
      </div>
    </section>
  );
}
