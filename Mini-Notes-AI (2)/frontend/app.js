const API_BASE = "http://localhost:8000";

async function fetchNotes() {
  const res = await fetch(`${API_BASE}/notes`);
  const notes = await res.json();
  const container = document.getElementById("notesList");
  container.innerHTML = "";
  if (notes.length === 0) {
    container.innerHTML = "<div class='small'>No notes yet</div>";
    return;
  }
  notes.forEach(n => {
    const el = document.createElement("div");
    el.className = "note";
    el.innerHTML = `<strong>${escapeHtml(n.title)}</strong><div class="small">${escapeHtml(n.content)}</div>`;
    container.appendChild(el);
  });
}

function escapeHtml(s) {
  return s.replace(/[&<>"']/g, function(m){return {"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[m];});
}

document.getElementById("noteForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const title = document.getElementById("title").value;
  const content = document.getElementById("content").value;
  const resp = await fetch(`${API_BASE}/notes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, content })
  });
  if (resp.ok) {
    document.getElementById("title").value = "";
    document.getElementById("content").value = "";
    await fetchNotes();
    alert("Note added");
  } else {
    const err = await resp.json();
    alert("Error: " + (err.detail || resp.statusText));
  }
});

document.getElementById("searchBtn").addEventListener("click", async () => {
  const q = document.getElementById("query").value;
  if (!q.trim()) {
    alert("Enter a query");
    return;
  }
  const resp = await fetch(`${API_BASE}/search`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query: q, top_k: 5 })
  });
  const results = await resp.json();
  const div = document.getElementById("searchResults");
  div.innerHTML = "";
  if (results.length === 0) {
    div.innerHTML = "<div class='small'>No matches</div>";
    return;
  }
  results.forEach(r => {
    const el = document.createElement("div");
    el.className = "note";
    el.innerHTML = `<strong>${escapeHtml(r.title)}</strong> <span class="small">(score: ${r.score})</span><div class="small">${escapeHtml(r.content)}</div>`;
    div.appendChild(el);
  });
});

document.getElementById("refreshBtn").addEventListener("click", fetchNotes);

fetchNotes();
