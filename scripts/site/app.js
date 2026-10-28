/*__DATA__*/
(function () {
  const mods = Array.from(document.querySelectorAll(".module"));
  const parts = Array.from(document.querySelectorAll(".part"));
  const nodes = Array.from(document.querySelectorAll(".node"));
  const panel = document.getElementById("stage-panel");
  const note = document.getElementById("filter-note");
  const state = { level: new Set(), repo: new Set(), stage: null };
  const LEVEL_NAMES = { foundation: "Foundation", core: "Core", advanced: "Advanced", expert: "Expert" };

  function store(get, key, val) {
    try {
      if (get) return localStorage.getItem(key);
      localStorage.setItem(key, val);
    } catch (e) { return null; }
  }

  function apply() {
    let shown = 0;
    mods.forEach((m) => {
      const lv = m.dataset.level, repos = m.dataset.repos.split(" "), stages = m.dataset.stages.split(" ");
      const ok = (!state.level.size || state.level.has(lv)) &&
        (!state.repo.size || repos.some((r) => state.repo.has(r))) &&
        (!state.stage || stages.includes(state.stage));
      m.classList.toggle("hide", !ok);
      if (ok) shown++;
    });
    parts.forEach((p) => p.classList.toggle("empty", !p.querySelector(".module:not(.hide)")));
    const active = state.level.size || state.repo.size || state.stage;
    note.hidden = !active;
    if (active) {
      const bits = [];
      if (state.stage) bits.push("stage “" + DATA.stages[state.stage].label + "”");
      if (state.level.size) bits.push([...state.level].map((l) => LEVEL_NAMES[l]).join(" or "));
      if (state.repo.size) bits.push("repo " + [...state.repo].join(" or "));
      note.innerHTML = "";
      note.append("Showing " + shown + " of " + mods.length + " modules for " + bits.join(", ") + ". ");
      const b = document.createElement("button");
      b.className = "tbtn"; b.textContent = "Clear filters";
      b.addEventListener("click", clearAll);
      note.append(b);
    }
  }

  function clearAll() {
    state.level.clear(); state.repo.clear();
    document.querySelectorAll(".fchip").forEach((c) => c.setAttribute("aria-pressed", "false"));
    selectStage(null);
  }

  function selectStage(id) {
    state.stage = state.stage === id ? null : id;
    nodes.forEach((n) => n.classList.toggle("active", n.dataset.stage === state.stage));
    panel.innerHTML = "";
    if (!state.stage) {
      const p = document.createElement("p");
      p.className = "hint"; p.textContent = "No stage selected. Showing all modules.";
      panel.append(p);
    } else {
      const st = DATA.stages[state.stage];
      const h = document.createElement("h3");
      h.textContent = st.label + " · " + st.mods.length + (st.mods.length === 1 ? " module" : " modules");
      const row = document.createElement("div");
      row.className = "sp-row";
      st.mods.forEach((n) => {
        const a = document.createElement("a");
        a.className = "sp-mod"; a.href = "#m" + n;
        const b = document.createElement("b"); b.textContent = "M" + String(n).padStart(2, "0");
        const lv = document.createElement("span"); lv.className = "dot lvl-" + DATA.levels[n];
        a.append(b, lv, document.createTextNode(DATA.titles[n]));
        a.addEventListener("click", (e) => { e.preventDefault(); openModule(n); });
        row.append(a);
      });
      const clr = document.createElement("button");
      clr.className = "tbtn clear-btn"; clr.textContent = "Clear stage";
      clr.addEventListener("click", () => selectStage(state.stage));
      row.append(clr);
      panel.append(h, row);
    }
    apply();
  }

  function openModule(n) {
    const el = document.getElementById("m" + n);
    if (!el) return;
    el.classList.remove("hide");
    el.open = true;
    el.scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "start" });
    el.classList.remove("flash"); void el.offsetWidth; el.classList.add("flash");
  }

  nodes.forEach((n) => {
    n.addEventListener("click", () => selectStage(n.dataset.stage));
    n.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); selectStage(n.dataset.stage); } });
  });

  document.querySelectorAll(".fchip").forEach((c) => c.addEventListener("click", () => {
    const set = state[c.dataset.filter], v = c.dataset.value;
    set.has(v) ? set.delete(v) : set.add(v);
    c.setAttribute("aria-pressed", set.has(v) ? "true" : "false");
    apply();
  }));

  const optBox = document.getElementById("show-opt");
  optBox.addEventListener("change", () => document.body.classList.toggle("hide-opt", !optBox.checked));
  document.getElementById("expand-all").addEventListener("click", () => mods.forEach((m) => { if (!m.classList.contains("hide")) m.open = true; }));
  document.getElementById("collapse-all").addEventListener("click", () => mods.forEach((m) => (m.open = false)));

  // progress (per-viewer, localStorage)
  const boxes = Array.from(document.querySelectorAll(".done input"));
  let done = {};
  try { done = JSON.parse(store(true, "rag-curriculum-done") || "{}"); } catch (e) { done = {}; }
  function renderProgress() {
    const n = boxes.filter((b) => b.checked).length;
    document.getElementById("prog-text").textContent = n + " of " + boxes.length + " modules done";
    document.getElementById("prog-bar").style.width = (100 * n / boxes.length) + "%";
  }
  boxes.forEach((b) => {
    b.checked = !!done[b.dataset.mod];
    b.closest(".module").classList.toggle("is-done", b.checked);
    b.addEventListener("click", (e) => e.stopPropagation());
    b.addEventListener("change", () => {
      done[b.dataset.mod] = b.checked;
      b.closest(".module").classList.toggle("is-done", b.checked);
      store(false, "rag-curriculum-done", JSON.stringify(done));
      renderProgress();
    });
  });
  document.querySelectorAll(".done").forEach((l) => l.addEventListener("click", (e) => e.stopPropagation()));
  renderProgress();

  document.querySelectorAll('a[href^="#m"]').forEach((a) => {
    if (a.classList.contains("sp-mod")) return;
    a.addEventListener("click", (e) => { e.preventDefault(); openModule(a.getAttribute("href").slice(2)); });
  });
})();
