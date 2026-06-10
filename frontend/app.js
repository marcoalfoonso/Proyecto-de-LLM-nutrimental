const API_URL      = "http://localhost:8000/chat/admin";
const PROFILES_URL = "http://localhost:8000/profiles";

const form         = document.getElementById("chatForm");
const chat         = document.getElementById("chat");
const metricsGrid  = document.getElementById("metricsGrid");
const profileInfo  = document.getElementById("profileInfo");
const sendBtn      = document.getElementById("sendBtn");
const clearBtn     = document.getElementById("clearBtn");
const loadBtn      = document.getElementById("loadProfileBtn");
const messageInput = document.getElementById("message");
const promptInput  = document.getElementById("system_prompt");
const profileSel   = document.getElementById("copilot_profile");

let profiles = {};

// ── Utilidad HTML ──────────────────────────────────────
function escHtml(t) {
  return String(t)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

// ── Cargar perfiles desde el backend ──────────────────
async function loadProfiles() {
  try {
    const res = await fetch(PROFILES_URL);
    if (!res.ok) throw new Error("No se pudo conectar con /profiles");
    profiles = await res.json();
    applySelectedProfile();
  } catch (err) {
    promptInput.value = "⚠️ No se pudieron cargar los perfiles. Verifica que el backend esté corriendo en http://localhost:8000.";
    console.error(err);
  }
}

function applySelectedProfile() {
  const id = profileSel.value;
  if (profiles[id]) {
    promptInput.value = profiles[id].system_prompt;
  }
}

// ── Config actual ──────────────────────────────────────
function getConfig() {
  return {
    model:           document.getElementById("model").value,
    copilot_profile: profileSel.value,
    system_prompt:   promptInput.value,
    temperature:     parseFloat(document.getElementById("temperature").value),
    top_p:           parseFloat(document.getElementById("top_p").value),
    num_predict:     parseInt(document.getElementById("num_predict").value),
    num_ctx:         parseInt(document.getElementById("num_ctx").value),
    repeat_penalty:  parseFloat(document.getElementById("repeat_penalty").value),
  };
}

// ── Chat UI ────────────────────────────────────────────
function addBubble(role, text, type) {
  const div = document.createElement("div");
  div.className = `message ${type}`;
  div.innerHTML = `<strong>${escHtml(role)}</strong>${escHtml(text)}`;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function addThinking() {
  const el = document.createElement("div");
  el.className = "thinking";
  el.textContent = "Generando respuesta...";
  el.id = "thinking";
  chat.appendChild(el);
  chat.scrollTop = chat.scrollHeight;
}

function removeThinking() {
  const el = document.getElementById("thinking");
  if (el) el.remove();
}

// ── Métricas ───────────────────────────────────────────
function renderMetrics(data) {
  profileInfo.innerHTML = `
    <strong>Perfil:</strong> ${escHtml(data.copilot_label)} &nbsp;|&nbsp;
    <strong>Modelo:</strong> ${escHtml(data.model)}
  `;

  const m = data.metrics;
  const items = [
    ["Tiempo backend",  `${m.wall_time_s.toFixed(2)} s`],
    ["Tiempo Ollama",   `${m.total_duration_s.toFixed(2)} s`],
    ["Carga modelo",    `${m.load_duration_s.toFixed(2)} s`],
    ["Tokens entrada",  m.prompt_eval_count],
    ["Tokens salida",   m.eval_count],
    ["Tokens totales",  m.total_tokens],
    ["Generación",      `${m.eval_duration_s.toFixed(2)} s`],
    ["Tokens/s",        m.tokens_per_second.toFixed(2)],
  ];

  metricsGrid.innerHTML = items.map(([label, val]) => `
    <div class="metric-card">
      <small>${label}</small>
      <strong>${val}</strong>
    </div>
  `).join("");
}

// ── Enviar mensaje ─────────────────────────────────────
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const msg = messageInput.value.trim();
  if (!msg) return;

  addBubble("Tú", msg, "user");
  messageInput.value = "";
  sendBtn.disabled = true;
  sendBtn.textContent = "Generando...";
  addThinking();

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg, ...getConfig() }),
    });

    const data = await res.json();
    removeThinking();

    if (!res.ok) throw new Error(data.detail || "Error del backend");

    addBubble(`Copiloto — ${data.copilot_label}`, data.reply, "assistant");
    renderMetrics(data);

  } catch (err) {
    removeThinking();
    addBubble("Error", err.message, "error");
  } finally {
    sendBtn.disabled = false;
    sendBtn.textContent = "Enviar →";
  }
});

// ── Enter para enviar ──────────────────────────────────
messageInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    form.dispatchEvent(new Event("submit"));
  }
});

// ── Botones ────────────────────────────────────────────
clearBtn.addEventListener("click", () => {
  chat.innerHTML = "";
  profileInfo.textContent = "Sin perfil usado todavía";
  metricsGrid.innerHTML = '<span class="no-data">Sin datos todavía</span>';
});

loadBtn.addEventListener("click", applySelectedProfile);
profileSel.addEventListener("change", applySelectedProfile);

// ── Init ───────────────────────────────────────────────
loadProfiles();