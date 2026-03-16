const apiBase =
  window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
    ? "http://localhost:8000"
    : `${window.location.protocol}//${window.location.hostname}:8000`;

const queryEl = document.getElementById("query");
const kindEl = document.getElementById("kind");
const resultsEl = document.getElementById("results");
const detailEl = document.getElementById("detail");

const algoTypeEl = document.getElementById("algoType");
const algoArrayEl = document.getElementById("algoArray");
const algoTargetEl = document.getElementById("algoTarget");
const arrayStateEl = document.getElementById("arrayState");
const stepCaptionEl = document.getElementById("stepCaption");
const stepMetaEl = document.getElementById("stepMeta");
const stepCounterEl = document.getElementById("stepCounter");
const speedRangeEl = document.getElementById("speedRange");

let traceSteps = [];
let currentIndex = -1;
let playTimer = null;
let playing = false;

function renderResults(items) {
  resultsEl.innerHTML = "";
  if (!items.length) {
    resultsEl.innerHTML = '<div class="item"><p>No results.</p></div>';
    return;
  }

  items.forEach((item) => {
    const card = document.createElement("article");
    card.className = "item";
    card.innerHTML = `
      <h3>${item.title}</h3>
      <p>[${item.type}] ${item.snippet}</p>
    `;
    card.addEventListener("click", () => loadDetail(item));
    resultsEl.appendChild(card);
  });
}

async function loadDetail(item) {
  const endpoint = item.type === "theorem" ? `/api/theorems/${item.id}` : `/api/formulas/${item.id}`;
  const res = await fetch(`${apiBase}${endpoint}`);
  if (!res.ok) {
    detailEl.textContent = "Failed to load detail.";
    return;
  }

  const data = await res.json();
  detailEl.textContent = JSON.stringify(data, null, 2);
}

async function search() {
  const query = queryEl.value.trim();
  if (!query) {
    detailEl.textContent = "Type a query first.";
    return;
  }

  const url = new URL(`${apiBase}/api/search`);
  url.searchParams.set("q", query);
  url.searchParams.set("type", kindEl.value);
  url.searchParams.set("top_k", "20");

  const res = await fetch(url.toString());
  if (!res.ok) {
    detailEl.textContent = "Search request failed.";
    return;
  }

  const data = await res.json();
  renderResults(data.items || []);
}

function parseArrayInput(raw) {
  return raw
    .split(",")
    .map((x) => x.trim())
    .filter((x) => x.length > 0)
    .map((x) => Number(x));
}

function renderCurrentStep() {
  arrayStateEl.innerHTML = "";

  if (traceSteps.length === 0 || currentIndex < 0) {
    stepCounterEl.textContent = "step 0/0";
    stepCaptionEl.textContent = "No trace yet.";
    stepMetaEl.textContent = "";
    return;
  }

  const step = traceSteps[currentIndex];
  const highlightSet = new Set(step.highlight || []);

  step.state.forEach((value, idx) => {
    const cell = document.createElement("div");
    cell.className = highlightSet.has(idx) ? "cell highlight" : "cell";
    cell.textContent = String(value);
    arrayStateEl.appendChild(cell);
  });

  stepCounterEl.textContent = `step ${currentIndex + 1}/${traceSteps.length}`;
  stepCaptionEl.textContent = step.caption || "";
  stepMetaEl.textContent = JSON.stringify(step, null, 2);
}

function stopPlayback() {
  if (playTimer) {
    clearInterval(playTimer);
    playTimer = null;
  }
  playing = false;
  document.getElementById("playPauseBtn").textContent = "Play";
}

function playNext() {
  if (traceSteps.length === 0) {
    stopPlayback();
    return;
  }

  if (currentIndex >= traceSteps.length - 1) {
    stopPlayback();
    return;
  }

  currentIndex += 1;
  renderCurrentStep();
}

function startPlayback() {
  if (traceSteps.length === 0) {
    return;
  }

  if (currentIndex >= traceSteps.length - 1) {
    currentIndex = -1;
  }

  stopPlayback();
  playing = true;
  document.getElementById("playPauseBtn").textContent = "Pause";
  playTimer = setInterval(playNext, Number(speedRangeEl.value));
}

async function generateTrace() {
  const algorithm = algoTypeEl.value;
  const array = parseArrayInput(algoArrayEl.value);
  const target = Number(algoTargetEl.value);

  if (!array.length || array.some((x) => Number.isNaN(x))) {
    stepCaptionEl.textContent = "Array input is invalid.";
    return;
  }

  const payload = { algorithm, array };
  if (algorithm === "binary_search") {
    if (Number.isNaN(target)) {
      stepCaptionEl.textContent = "Target is required for binary_search.";
      return;
    }
    payload.target = target;
  }

  const res = await fetch(`${apiBase}/api/animations/trace`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    stepCaptionEl.textContent = "Trace generation failed.";
    return;
  }

  const data = await res.json();
  traceSteps = data.steps || [];
  currentIndex = traceSteps.length ? 0 : -1;
  stopPlayback();
  renderCurrentStep();
}

document.getElementById("searchBtn").addEventListener("click", search);
queryEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    search();
  }
});

document.getElementById("genTraceBtn").addEventListener("click", generateTrace);
document.getElementById("prevStepBtn").addEventListener("click", () => {
  if (traceSteps.length === 0) {
    return;
  }
  stopPlayback();
  currentIndex = Math.max(0, currentIndex - 1);
  renderCurrentStep();
});
document.getElementById("nextStepBtn").addEventListener("click", () => {
  if (traceSteps.length === 0) {
    return;
  }
  stopPlayback();
  currentIndex = Math.min(traceSteps.length - 1, currentIndex + 1);
  renderCurrentStep();
});
document.getElementById("playPauseBtn").addEventListener("click", () => {
  if (playing) {
    stopPlayback();
  } else {
    startPlayback();
  }
});

speedRangeEl.addEventListener("change", () => {
  if (playing) {
    startPlayback();
  }
});

renderCurrentStep();
