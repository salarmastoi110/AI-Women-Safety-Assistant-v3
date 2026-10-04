const BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function req(path, options = {}) {
  const res = await fetch(BASE + path, { headers: { "Content-Type": "application/json" }, ...options });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}
const post = (path, body) => req(path, { method: "POST", body: JSON.stringify(body ?? {}) });

export const api = {
  getContacts: () => req("/api/contacts"),
  addContact: (c) => post("/api/contacts", c),
  deleteContact: (id) => req(`/api/contacts/${id}`, { method: "DELETE" }),
  analyze: (payload) => post("/api/analyze", payload),
  assessRisk: (payload) => post("/api/risk/assess", payload),
  sos: (payload) => post("/api/alerts/sos", payload),
  alerts: () => req("/api/alerts"),
  pushLocation: (token, latitude, longitude) => post(`/api/alerts/${token}/location`, { latitude, longitude }),
  resolve: (token) => post(`/api/alerts/${token}/resolve`),
};

export function getLocation() {
  return new Promise((resolve) => {
    if (!navigator.geolocation) return resolve(null);
    navigator.geolocation.getCurrentPosition(
      (p) => resolve({ latitude: p.coords.latitude, longitude: p.coords.longitude }),
      () => resolve(null),
      { timeout: 6000, enableHighAccuracy: true, maximumAge: 10000 }
    );
  });
}
