import { useEffect, useRef, useState } from "react";
import SOSButton from "../components/SOSButton.jsx";
import CountdownModal from "../components/CountdownModal.jsx";
import VoiceGuard from "../components/VoiceGuard.jsx";
import AnalysisCard from "../components/AnalysisCard.jsx";
import ActiveAlert from "../components/ActiveAlert.jsx";
import RiskMeter from "../components/RiskMeter.jsx";
import EmergencyNumbers from "../components/EmergencyNumbers.jsx";
import AlertsTable from "../components/AlertsTable.jsx";
import { api, getLocation } from "../services/api.js";
import { useApp } from "../services/AppContext.jsx";

export default function Home({ goTo }) {
  const { t, lang, settings } = useApp();
  const [analysis, setAnalysis] = useState(null);
  const [pending, setPending] = useState(null);   // {source, text, seconds}
  const [active, setActive] = useState(null);
  const [sending, setSending] = useState(false);
  const [note, setNote] = useState("");
  const [risk, setRisk] = useState(null);
  const [contactCount, setContactCount] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [msg, setMsg] = useState("");
  const gate = useRef({ pending: false, active: false });
  gate.current = { pending: !!pending, active: !!active && active.status !== "resolved" };

  const loadAlerts = () => api.alerts().then(setAlerts).catch(() => {});
  useEffect(() => {
    api.getContacts().then((c) => setContactCount(c.length)).catch(() => setMsg(t("api_error")));
    loadAlerts();
  }, []);

  // called by VoiceGuard for every analysed utterance
  const onAnalysis = (res, text) => {
    setAnalysis(res);
    if (res.auto_trigger && settings.autoTrigger && !gate.current.pending && !gate.current.active) {
      setPending({ source: "voice", text, seconds: settings.countdown });
    }
  };

  const sendSOS = async () => {
    const p = pending;
    setPending(null); setSending(true); setMsg("");
    try {
      const loc = await getLocation();
      if (!loc) setMsg(t("location_denied"));
      const res = await api.sos({
        message: p?.text || note, hour: new Date().getHours(), is_alone: true,
        lang, user_name: settings.userName, source: p?.source || "manual", ...(loc || {}),
      });
      setActive(res);
      loadAlerts();
    } catch { setMsg(t("api_error")); }
    finally { setSending(false); }
  };

  const checkRisk = async () => {
    try { setRisk(await api.assessRisk({ hour: new Date().getHours(), message: note, is_alone: true })); }
    catch { setMsg(t("api_error")); }
  };

  const activeCount = alerts.filter((a) => a.status === "active").length;

  return (
    <div className="dash">
      {(contactCount === 0 && !active || msg) && (
        <div className="cell s12">
          {contactCount === 0 && !active && (
            <div className="banner">
              {t("no_contacts_warn")} <button className="link" onClick={() => goTo("contacts")}>{t("add_contacts")}</button>
            </div>
          )}
          {msg && <div className="banner soft" role="status">{msg}</div>}
        </div>
      )}

      <div className="stats s12">
        <div className="panel stat"><b>{contactCount ?? "–"}</b><span>{t("contacts_title")}</span></div>
        <div className="panel stat"><b>{alerts.length}</b><span>{t("stat_alerts")}</span></div>
        <div className={"panel stat" + (activeCount > 0 ? " hot" : "")}><b>{activeCount}</b><span>{t("stat_active")}</span></div>
      </div>

      <div className="cell s5">
        {active
          ? <ActiveAlert alert={active} onGoContacts={() => goTo("contacts")} onDone={() => setActive(null)} />
          : (
            <section className="panel sos-panel">
              <SOSButton disabled={sending} onPress={() => setPending({ source: "manual", text: note, seconds: 5 })} />
              {sending && <p className="center muted">{t("sending")}</p>}
              <input className="note" value={note} onChange={(e) => setNote(e.target.value)} placeholder={t("note_placeholder")} />
            </section>
          )}
      </div>

      <div className="cell s7">
        <VoiceGuard onAnalysis={onAnalysis} />
        <AnalysisCard analysis={analysis} />
      </div>

      <section className="panel tablepanel s8">
        <div className="panel-head">
          <h3>{t("recent_alerts")}</h3>
          {alerts.length > 0 && <button className="link" onClick={() => goTo("history")}>{t("view_all")}</button>}
        </div>
        {alerts.length === 0 ? <p className="empty muted">{t("history_empty")}</p> : <AlertsTable alerts={alerts.slice(0, 5)} compact />}
      </section>

      <div className="cell s4">
        <section className="panel">
          <h3>{t("risk_score")}</h3>
          <button className="btn" onClick={checkRisk}>{t("risk_check")}</button>
        </section>
        <RiskMeter risk={risk} />
        <EmergencyNumbers />
      </div>

      {pending && (
        <CountdownModal seconds={pending.seconds} source={pending.source}
          onCancel={() => setPending(null)} onConfirm={sendSOS} />
      )}
    </div>
  );
}
