import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { LANGS, translate } from "./i18n.js";

const DEFAULTS = { userName: "", uiLang: "en", voiceLang: "ur-PK", autoTrigger: true, countdown: 10 };
const Ctx = createContext(null);

function load() {
  try { return { ...DEFAULTS, ...JSON.parse(localStorage.getItem("hifazat:settings") || "{}") }; }
  catch { return DEFAULTS; }
}

export function AppProvider({ children }) {
  const [settings, setSettingsState] = useState(load);
  const lang = settings.uiLang;
  const meta = LANGS.find((l) => l.code === lang) || LANGS[0];

  const setSettings = (patch) => setSettingsState((s) => {
    const next = { ...s, ...patch };
    try { localStorage.setItem("hifazat:settings", JSON.stringify(next)); } catch { /* ignore */ }
    return next;
  });

  useEffect(() => {
    document.documentElement.lang = lang;
    document.documentElement.dir = meta.dir;
  }, [lang, meta.dir]);

  const value = useMemo(() => ({
    lang, dir: meta.dir, settings, setSettings,
    t: (key, vars) => translate(lang, key, vars),
  }), [lang, meta.dir, settings]);

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export const useApp = () => useContext(Ctx);
