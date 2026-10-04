import { useState } from "react";
import { AppProvider, useApp } from "./services/AppContext.jsx";
import { LANGS } from "./services/i18n.js";
import Home from "./pages/Home.jsx";
import Contacts from "./pages/Contacts.jsx";
import History from "./pages/History.jsx";
import Settings from "./pages/Settings.jsx";

const ICONS = {
  home: "M3 11l9-8 9 8v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z",
  contacts: "M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zm8 1a3 3 0 1 0 0-6M2 21a7 7 0 0 1 14 0M17 14a5 5 0 0 1 5 5v2",
  history: "M12 7v5l3 2M3 12a9 9 0 1 0 3-6.7M3 4v4h4",
  settings: "M4 6h10M18 6h2M4 12h2M10 12h10M4 18h12M20 18h0M14 4v4M8 10v4M18 16v4",
};
const PAGES = { home: Home, contacts: Contacts, history: History, settings: Settings };
const TITLES = { home: "tab_home", contacts: "contacts_title", history: "history_title", settings: "settings_title" };

function LangSwitch({ className = "" }) {
  const { settings, setSettings } = useApp();
  return (
    <div className={"seg compact " + className} role="radiogroup" aria-label="Language">
      {LANGS.map((l) => (
        <button key={l.code} role="radio" aria-checked={settings.uiLang === l.code}
          className={settings.uiLang === l.code ? "on" : ""} onClick={() => setSettings({ uiLang: l.code })}>
          {l.label}
        </button>
      ))}
    </div>
  );
}

function Shell() {
  const { t } = useApp();
  const [tab, setTab] = useState("home");
  const Page = PAGES[tab];
  return (
    <div className="shell">
      <aside className="side">
        <div className="brand">
          <h1>{t("app_title")}</h1>
          <p>{t("app_sub")}</p>
        </div>

        <nav className="nav" aria-label="Main">
          {Object.keys(PAGES).map((k) => (
            <button key={k} className={tab === k ? "on" : ""} aria-current={tab === k ? "page" : undefined} onClick={() => setTab(k)}>
              <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" strokeWidth="1.8"
                   strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d={ICONS[k]} /></svg>
              <span>{t("tab_" + k)}</span>
            </button>
          ))}
        </nav>

        <div className="side-foot"><LangSwitch /></div>
      </aside>

      <div className="content">
        <header className="topbar">
          <div className="tb-title">
            <span className="tb-brand">{t("app_title")}</span>
            <h2>{t(TITLES[tab])}</h2>
          </div>
          <div className="tb-right">
            {tab !== "home" && <button className="btn danger sm tb-sos" onClick={() => setTab("home")}>{t("sos")}</button>}
            <LangSwitch className="tb-lang" />
          </div>
        </header>

        <main className="page"><Page goTo={setTab} /></main>
      </div>
    </div>
  );
}

export default function App() {
  return <AppProvider><Shell /></AppProvider>;
}
