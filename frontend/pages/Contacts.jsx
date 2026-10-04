import { useEffect, useState } from "react";
import { api } from "../services/api.js";
import { LANGS } from "../services/i18n.js";
import { useApp } from "../services/AppContext.jsx";

export default function Contacts() {
  const { t, lang } = useApp();
  const empty = { name: "", phone: "", relation: "", language: lang };
  const [list, setList] = useState([]);
  const [form, setForm] = useState(empty);
  const load = () => api.getContacts().then(setList).catch(() => {});
  useEffect(() => { load(); }, []);

  const add = async (e) => {
    e.preventDefault();
    if (!form.name.trim() || !form.phone.trim()) return;
    await api.addContact(form);
    setForm({ ...empty, language: form.language });
    load();
  };

  return (
    <div className="dash">
      <section className="panel tablepanel s8">
        {list.length === 0 ? <p className="empty muted">{t("no_contacts")}</p> : (
          <div className="tablewrap">
            <table className="tbl">
              <thead>
                <tr><th>{t("name")}</th><th>{t("phone")}</th><th>{t("col_lang")}</th><th><span className="sr-only">{t("delete")}</span></th></tr>
              </thead>
              <tbody>
                {list.map((c) => (
                  <tr key={c.id}>
                    <td data-label={t("name")}><div><b>{c.name}</b>{c.relation && <div className="small muted">{c.relation}</div>}</div></td>
                    <td data-label={t("phone")}><span dir="ltr">{c.phone}</span></td>
                    <td data-label={t("col_lang")}><span className="chip nm">{LANGS.find((l) => l.code === c.language)?.label}</span></td>
                    <td className="act">
                      <button className="btn ghost sm" onClick={async () => { await api.deleteContact(c.id); load(); }}>{t("delete")}</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <form className="panel form s4 first-on-small" onSubmit={add}>
        <h3>{t("new_contact")}</h3>
        <label>{t("name")}<input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required /></label>
        <label>{t("phone")}<input dir="ltr" inputMode="tel" placeholder="+92 3xx xxxxxxx" value={form.phone}
          onChange={(e) => setForm({ ...form, phone: e.target.value })} required /></label>
        <label>{t("relation")}<input value={form.relation} onChange={(e) => setForm({ ...form, relation: e.target.value })} /></label>
        <label>{t("sms_language")}
          <select value={form.language} onChange={(e) => setForm({ ...form, language: e.target.value })}>
            {LANGS.map((l) => <option key={l.code} value={l.code}>{l.label}</option>)}
          </select>
        </label>
        <button className="btn primary" type="submit">{t("add")}</button>
      </form>
    </div>
  );
}
