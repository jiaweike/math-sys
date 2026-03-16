const apiBase = (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
  ? "http://localhost:8000"
  : `${window.location.protocol}//${window.location.hostname}:8000`;

const queryEl = document.getElementById("query");
const kindEl = document.getElementById("kind");
const resultsEl = document.getElementById("results");
const detailEl = document.getElementById("detail");

function renderResults(items) {
  resultsEl.innerHTML = "";
  if (!items.length) {
    resultsEl.innerHTML = "<div class=\"item\"><p>No results.</p></div>";
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
  const endpoint = item.type === "theorem"
    ? `/api/theorems/${item.id}`
    : `/api/formulas/${item.id}`;

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

document.getElementById("searchBtn").addEventListener("click", search);
queryEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    search();
  }
});
