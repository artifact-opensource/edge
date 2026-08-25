const SESSION = localStorage.getItem("edge_session") || "edge-local-dev";

async function req(path, opts = {}) {
  const options = { ...opts, headers: { ...(opts.headers || {}), "Content-Type": "application/json", "X-EDGE-SESSION": SESSION } };
  const res = await fetch(path, options);
  return res.json();
}

function asPretty(obj) {
  return JSON.stringify(obj, null, 2);
}

async function refresh() {
  const [health, bootstrap, connectivity] = await Promise.all([
    req("/health"),
    req("/bootstrap/usb"),
    req("/connectivity"),
  ]);
  document.getElementById("health").textContent = asPretty(health);
  document.getElementById("bootstrap").textContent = asPretty(bootstrap);
  document.getElementById("connState").textContent = `Connectivity: ${connectivity.state}${connectivity.last_error ? ` (${connectivity.last_error})` : ""}`;
}

async function loadConfig() {
  const cfg = await req("/config");
  const form = document.getElementById("configForm");
  form.ssid.value = cfg.wifi.ssid || "";
  form.password.value = "";
  form.backend.value = cfg.backend.endpoint || "";
  form.provider.value = cfg.llm.provider || "openai";
  form.llm_base_url.value = cfg.llm.base_url || "";
  form.credentials_ref.value = "";
}

document.getElementById("configForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const f = e.target;
  const payload = {
    wifi: { ssid: f.ssid.value },
    backend: { endpoint: f.backend.value },
    llm: {
      provider: f.provider.value,
      base_url: f.llm_base_url.value,
    },
  };
  if (f.password.value) {
    payload.wifi.password = f.password.value;
  }
  if (f.credentials_ref.value) {
    payload.llm.credentials_ref = f.credentials_ref.value;
  }
  const res = await req("/config", { method: "PUT", body: JSON.stringify(payload) });
  if (res.ok) {
    await req("/connectivity/event", { method: "POST", body: JSON.stringify({ event: "wifi_credentials_saved" }) });
    await refresh();
    alert("Configuration saved");
  } else {
    alert(res.error || "Failed to save config");
  }
});

document.getElementById("commandForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const target = e.target.target.value;
  const payload = {
    id: (window.crypto && window.crypto.randomUUID) ? window.crypto.randomUUID() : `cmd-${Date.now()}-${Math.random()}`,
    action: "intent",
    payload: { type: "move", target },
  };
  const res = await req("/command", { method: "POST", body: JSON.stringify(payload) });
  document.getElementById("commandResult").textContent = asPretty(res);
});

document.getElementById("refreshStatus").addEventListener("click", refresh);
document.getElementById("connectWifi").addEventListener("click", async () => {
  await req("/connectivity/event", { method: "POST", body: JSON.stringify({ event: "sta_connected" }) });
  await refresh();
});
document.getElementById("recoverAp").addEventListener("click", async () => {
  await req("/connectivity/event", { method: "POST", body: JSON.stringify({ event: "recover_ap" }) });
  await refresh();
});

loadConfig().then(refresh);
