"""Render curriculum.yaml to CURRICULUM.md, docs/site/index.html and the README in every Part, module, lab and capstone folder.

    uv run python scripts/build_curriculum.py

Run it after scripts/migrate.py, or after editing curriculum.yaml by hand.
"""
import html
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_docs  # noqa: E402
import build_theory_html  # noqa: E402
from curriculum_lib import ROOT, THEORY_DIR, items, lesson_folder, load, module_dir, source_module, theory_dir  # noqa: E402

GH = "https://github.com/Sourav692"
COURSE_REPO = "rag-agents-engineering"
SITE = ROOT / "scripts/site"
THEORY = THEORY_DIR  # hand-written theory pages, laid out like course/; only theory/README.md is generated

CUR = load()
COURSE = CUR["course"]
LEVELS = CUR["levels"]
STAGES = CUR["stages"]
CAP_HOURS = CUR["capstone_hours"]
REPOS = {k: (v["repo"], v["topic"]) for k, v in CUR["sources"].items()}
REASONS = {k: (v["label"], v["description"]) for k, v in CUR["tiers"].items() if k != "mandatory"}
PARTS = CUR["parts"]
CAPSTONES = CUR["capstones"]
ASSESSMENT = [(a["component"], a["weight"], a["detail"]) for a in CUR["assessment"]]
GAPS = CUR["gaps"]
ITEMS = items(CUR)
MODULES = CUR["modules"]
by_lesson = defaultdict(list)
for it in ITEMS:
    by_lesson[(it.module["num"], it.lesson_no)].append(it)
for m in MODULES:
    m["lessons_r"] = [(les["title"], by_lesson[(m["num"], i)]) for i, les in enumerate(m["lessons"], 1)]
    m["lab_r"] = by_lesson[(m["num"], 0)]
BASE = next(m["num"] for m in MODULES if m["key"] == "lifecycle")  # the module whose lab sets the baseline
BASE_M = f"M{BASE:02d}"
N_WEEKS = int(re.findall(r"\d+", PARTS[-1]["weeks"])[-1])

# The HTML site links to files on GitHub; Markdown links are relative to the file being written.
LINK_BASE = None  # set per output by rel_link()


def rel_link(it, from_dir):
    return os.path.relpath(ROOT / it.dest, ROOT / from_dir).replace(os.sep, "/")


def parse_ref(it):
    kind = "tree" if not os.path.splitext(it.file)[1] else "blob"
    return {"repo": it.repo, "mod": it.folder, "name": os.path.splitext(it.file)[0], "file": it.file,
            "url": f"{GH}/{COURSE_REPO}/{kind}/main/{it.dest}", "optional": it.optional,
            "reason": None if not it.optional else it.tier, "path": it.source_path, "item": it}


def theory_of(m):
    """The module's theory page, its lesson pages and labs under theory/<part>/<module>/, or None if it has none yet."""
    d = theory_dir(m)
    if not (ROOT / d / "README.md").exists():
        return None
    lessons = {}  # lesson number -> its theory page
    for n, les in enumerate(m["lessons"], 1):
        page = f"{d}/{lesson_folder(n, les['title'])}/README.md"
        if (ROOT / page).exists():
            lessons[n] = page
    concepts = {}  # key concept -> the page with its `##` heading
    for page in [f"{d}/README.md", *lessons.values()]:
        heads = re.findall(r"^## (.+?)\s*$", (ROOT / page).read_text(), re.M)
        concepts.update({c: page for c in m["concepts"] if c in heads and c not in concepts})
    labs = []
    for p in sorted((ROOT / d).glob("**/interactive/*.html")):
        title = re.search(r"<title>(.*?)</title>", p.read_text(), re.S)
        labs.append((title.group(1).strip() if title else p.stem, p.relative_to(ROOT).as_posix()))
    return {"readme": f"{d}/README.md", "lessons": lessons, "concepts": concepts, "labs": labs}


def concept_page(t, c):
    return f"{t['concepts'].get(c, t['readme'])}#{anchor(c)}"


def anchor(heading):
    """GitHub's anchor for a Markdown heading; theory pages give each key concept its own `##` heading."""
    return re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")


def short(mod):
    return mod


nb_items = [it for it in ITEMS if it.is_notebook]
n_nb = len(nb_items)
n_core = sum(1 for it in nb_items if not it.optional)
n_opt = n_nb - n_core
reason_counts = Counter(it.tier for it in nb_items if it.optional)
n_nb_by_repo = Counter(it.repo for it in nb_items)


def mod_counts(m):
    its = [it for _, rs in m["lessons_r"] for it in rs] + m["lab_r"]
    return sum(1 for it in its if not it.optional), sum(1 for it in its if it.optional)


total_hours = sum(m["hours"] for m in MODULES) + CAP_HOURS
n_lessons = sum(len(m["lessons"]) for m in MODULES)
stage_mods = defaultdict(list)
primary = defaultdict(list)
for m in MODULES:
    for st in m["stages"]:
        stage_mods[st].append(m["num"])
    primary[m["stages"][0]].append(m["num"])


def ranges(nums):
    out, run = [], []
    for n in sorted(nums):
        if run and n == run[-1] + 1:
            run.append(n)
        else:
            if run:
                out.append(run)
            run = [n]
    if run:
        out.append(run)
    return " · ".join(f"M{r[0]}" if len(r) == 1 else f"M{r[0]}–M{r[-1]}" for r in out)


mods_by_part = defaultdict(list)
for m in MODULES:
    mods_by_part[m["part"]].append(m)

coverage = defaultdict(set)
src_counts = Counter()
src_core = Counter()
for it in ITEMS:
    coverage[(it.repo, source_module(it.source_path))].add(it.module["num"])
for it in nb_items:
    key = (it.repo, source_module(it.source_path))
    src_counts[key] += 1
    if not it.optional:
        src_core[key] += 1


MD_FROM = ""  # folder the Markdown file being rendered lives in, relative to ROOT


def md_href(it):
    return rel_link(it, MD_FROM)


# ---------- Markdown ----------
def build_md():
    L = []
    a = L.append
    a(f"# {COURSE['title']}\n")
    a(f"*{COURSE['subtitle']}*\n")
    a(f"Built from {len(REPOS)} repositories. Every notebook in them is mapped to exactly one lesson below.\n")
    a("| Repo | Topic | Notebooks |")
    a("|---|---|---|")
    for k, (name, topic) in REPOS.items():
        a(f"| [`{name}`]({GH}/{name}) | {topic} | {n_nb_by_repo[k]} |")
    a("")

    a("## Course at a glance\n")
    a("| Parts | Modules | Lessons | Notebooks mapped | Mandatory | Optional | Suggested effort | Pace |")
    a("|---|---|---|---|---|---|---|---|")
    a(f"| {len(PARTS)} | {len(MODULES)} + capstone | {n_lessons} | {n_nb} | {n_core} | {n_opt} | ~{total_hours} hours | {N_WEEKS} weeks at ~{round(total_hours / N_WEEKS)} h/week |\n")

    a("## Who this course is for\n")
    for x in COURSE["audience"]:
        a(f"- {x}")
    a("\n## Prerequisites\n")
    for x in COURSE["prereqs"]:
        a(f"- {x}")
    a("\n## Learning outcomes\n\nBy the end of the course you can:\n")
    for i, x in enumerate(COURSE["outcomes"], 1):
        a(f"{i}. {x}")

    a("\n## How to read this syllabus\n")
    a("- **Levels:** Foundation → Core → Advanced → Expert.")
    a("- **Notebooks:** every lesson lists its notebooks as `repo/module/notebook`, split into **Mandatory** and **Optional** columns (see below).")
    a(f"- **Baseline-first:** the {BASE_M} lab produces a baseline. Every later lab reports its change against it on the same golden question set.")
    a("- **Hours** are suggested study time for the mandatory notebooks plus the lab. Optional notebooks are extra.\n")
    a("## Mandatory vs optional notebooks\n")
    a(f"You do not need every notebook. **{n_core} of {n_nb} notebooks are mandatory**; the other {n_opt} are optional.\n")
    a("**Rule:** each lesson keeps the one notebook (two, when they teach two distinct ideas) that you need for the lesson objective and the module lab. Everything else is optional for one of three reasons:\n")
    a("| Optional reason | Meaning | Notebooks |")
    a("|---|---|---|")
    for k, (lab_, desc) in REASONS.items():
        a(f"| **{lab_}** | {desc} | {reason_counts[k]} |")
    a("\nIf a lesson has no mandatory notebook, the whole lesson is optional.\n")

    a("## Course map\n")
    a("```mermaid")
    a("flowchart LR")
    a("  subgraph OFF[Offline: indexing]")
    a(f"    L[Load<br/>{lbl('load')}] --> C[Chunk<br/>{lbl('chunk')}] --> E[Embed<br/>{lbl('embed')}] --> S[Store / Index<br/>{lbl('store')}]")
    a("  end")
    a("  subgraph ON[Online: answering]")
    a(f"    Q[User query] --> T[Transform query<br/>{lbl('query')}] --> R[Retrieve<br/>{lbl('retrieve')}] --> P[Rerank & compress<br/>{lbl('post')}] --> G[Generate & cite<br/>{lbl('generate')}]")
    a("  end")
    a("  S --> R")
    a(f"  A{{{{Agents: plan · grade · route<br/>{lbl('agent')}}}}} -.retry / rewrite.-> T")
    a(f"  M[(Memory & multi-agent<br/>{lbl('memory')})] -.history / shared state.-> A")
    a("  G -.check.-> A")
    a(f"  K[(Trees & graphs<br/>{lbl('graph')})] --> R")
    a(f"  X[[Protocols: MCP · A2A<br/>{lbl('protocols')}]] -.tools & agents as services.-> A")
    a(f"  F([Foundations & concepts<br/>{lbl('concepts')}]) -.-> Q")
    a("```\n")

    a("## Roadmap\n")
    a("| Part | Title | When | Level | Modules |")
    a("|---|---|---|---|---|")
    for p in PARTS:
        ms = ", ".join(f"M{m['num']}" for m in mods_by_part[p["id"]])
        if p["id"] == "capstone":
            ms += ", Capstone"
        a(f"| {p['num']} | {p['title']} | {p['weeks']} | {LEVELS[p['level']]} | {ms} |")
    a("")

    for p in PARTS:
        a(f"---\n\n## Part {p['num']} — {p['title']}\n")
        a(f"**{p['weeks']} · {LEVELS[p['level']]}** — {p['summary']}\n")
        for m in mods_by_part[p["id"]]:
            srcs = ", ".join(f"`{s.split(':')[0]}/{s.split(':')[1]}`" for s in m["sources"])
            a(f"### Module {m['num']} — {m['title']}\n")
            mc, oc = mod_counts(m)
            a(f"**Level:** {LEVELS[m['level']]} · **Time:** ~{m['hours']} h · **Notebooks:** {mc} mandatory, {oc} optional · **Source:** {srcs}\n")
            a(f"**Why it matters.** {m['why']}\n")
            a("**Learning objectives**\n")
            for o in m["objectives"]:
                a(f"- {o}")
            a("\n**Lessons**\n")
            a("| # | Topic | Mandatory | Optional |")
            a("|---|---|---|---|")
            for i, (t, refs) in enumerate(m["lessons_r"], 1):
                core, opt = [], []
                for r in refs:
                    pr = parse_ref(r)
                    link = f"[`{pr['name']}`]({md_href(r)})"
                    (opt if pr["optional"] else core).append(link + (f" *({REASONS[pr['reason']][0].lower()})*" if pr["optional"] else ""))
                if not refs:
                    core = ["*Lecture / discussion*"]
                title = t + (" *(optional lesson)*" if refs and not core else "")
                a(f"| {m['num']}.{i} | {title} | {'<br>'.join(core) or '—'} | {'<br>'.join(opt) or '—'} |")
            lab = m["lab"]
            if m["lab_r"]:
                pr = parse_ref(m["lab_r"][0])
                lab += f" Notebook: [`{pr['name']}`]({md_href(m['lab_r'][0])})."
            a(f"\n**Hands-on lab.** {lab}\n")
            a(f"**Key concepts:** {' · '.join(m['concepts'])}\n")
        a(f"**Part {p['num']} checkpoint:** concept quiz plus one design question (for example, “Your hit rate is fine but answers are wrong — which stage do you inspect first and why?”).\n")

    a(f"---\n\n## Capstone projects ({PARTS[-1]['weeks']}, ~{CAP_HOURS} h)\n")
    a("Pick one. Each capstone must ship a working system, an evaluation report against a golden question set, and a 10-minute demo.\n")
    for i, c in enumerate(CAPSTONES, 1):
        a(f"### Capstone {chr(64 + i)} — {c['title']} ({LEVELS[c['level']]})\n")
        a(f"{c['brief']}\n")
        a("**Must include:**\n")
        for r in c["requires"]:
            a(f"- {r}")
        a("")

    a("## Assessment\n")
    a("| Component | Weight | What is assessed |")
    a("|---|---|---|")
    for c, w, d in ASSESSMENT:
        a(f"| {c} | {w} | {d} |")

    a("\n## Recommended additions (not covered by the source repos)\n")
    a("A top course would also cover the topics below. They are outside the scope of these repositories and are listed so the gaps are explicit.\n")
    a("| Topic | Status in repos | What to add |")
    a("|---|---|---|")
    for g in GAPS:
        a(f"| **{g['title']}** | {g['status']} | {g['detail']} |")

    a("\n## Appendix — source coverage\n")
    a("Every notebook in the source repositories, by source module, and the course modules that use it.\n")
    a("| Repo | Source module | Notebooks | Mandatory | Course modules |")
    a("|---|---|---|---|---|")
    for key in sorted(set(list(src_counts) + list(coverage))):
        cm = ", ".join(f"M{n}" for n in sorted(coverage.get(key, [])))
        a(f"| {key[0]} | `{key[1]}` | {src_counts.get(key, 0)} | {src_core.get(key, 0)} | {cm or '—'} |")
    a("| 09 | `12_cacherag` | 0 | 0 | — (planned in repo) |")
    a("")
    return "\n".join(L)


# ---------- HTML ----------
E = html.escape


def code_fmt(s):
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", E(s, quote=False))


NODES = {
    # id: (x, y, w, h)
    "load": (40, 70, 120, 52),
    "chunk": (190, 70, 120, 52),
    "embed": (340, 70, 120, 52),
    "store": (490, 70, 140, 52),
    "graph": (490, 250, 140, 52),
    "query": (40, 196, 130, 52),
    "retrieve": (672, 170, 130, 52),
    "post": (664, 254, 146, 52),
    "generate": (832, 254, 114, 52),
    "agent": (724, 52, 222, 52),
    "concepts": (40, 330, 200, 52),
    "memory": (262, 330, 200, 52),
    "protocols": (484, 330, 200, 52),
}
NODE_TITLE = {
    "load": "Load", "chunk": "Chunk", "embed": "Embed", "store": "Store / index", "graph": "Trees & graphs",
    "query": "Transform query", "retrieve": "Retrieve", "post": "Rerank & compress", "generate": "Generate & cite",
    "agent": "Agents: plan · grade · route", "concepts": "Foundations & concepts", "memory": "Memory & multi-agent",
    "protocols": "Protocols: MCP · A2A",
}


def lbl(stage):
    return ranges(primary[stage])


def svg_diagram():
    s = []
    s.append('<svg viewBox="0 0 970 420" role="img" aria-labelledby="dg-t dg-d" class="pipeline">')
    s.append('<title id="dg-t">RAG pipeline map</title><desc id="dg-d">Offline indexing lane (load, chunk, embed, store) feeds online retrieval (transform query, retrieve, rerank, generate). An agent layer plans, grades and routes; memory and multi-agent systems share state; trees and graphs provide structural indexes. Each stage lists the course modules that teach it.</desc>')
    s.append('<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="arrowhead"/></marker></defs>')
    # lane bands
    s.append('<rect x="20" y="28" width="630" height="112" rx="10" class="lane"/>')
    s.append('<text x="34" y="52" class="lane-label">OFFLINE · INDEXING</text>')
    s.append('<rect x="20" y="152" width="930" height="248" rx="10" class="lane lane-on"/>')
    s.append('<text x="34" y="176" class="lane-label">ONLINE · ANSWERING</text>')

    def mid(n, side):
        x, y, w, h = NODES[n]
        return {"r": (x + w, y + h / 2), "l": (x, y + h / 2), "t": (x + w / 2, y), "b": (x + w / 2, y + h)}[side]

    def line(a, b, cls="edge", curve=None):
        (x1, y1), (x2, y2) = a, b
        if curve:
            s.append(f'<path d="M{x1},{y1} {curve} {x2},{y2}" class="{cls}" marker-end="url(#arr)"/>')
        else:
            s.append(f'<path d="M{x1},{y1} L{x2},{y2}" class="{cls}" marker-end="url(#arr)"/>')

    line(mid("load", "r"), mid("chunk", "l"))
    line(mid("chunk", "r"), mid("embed", "l"))
    line(mid("embed", "r"), mid("store", "l"))
    sx, sy = mid("store", "r")
    rx, ry = mid("retrieve", "t")
    line((sx, sy), (rx - 20, ry), curve=f"C{sx + 60},{sy} {rx - 20},{ry - 50}")
    qx, qy = mid("query", "r")
    lx, ly = mid("retrieve", "l")
    line((qx, qy), (lx, ly))
    line(mid("graph", "r"), (lx, ly + 18), curve=f"C{mid('graph', 'r')[0] + 30},{mid('graph', 'r')[1]} {lx - 30},{ly + 18}")
    line(mid("retrieve", "b"), mid("post", "t"))
    line(mid("post", "r"), mid("generate", "l"))
    gx, gy = mid("generate", "t")
    ax, ay = mid("agent", "b")
    line((gx + 20, gy), (ax + 60, ay), cls="edge loop")
    line((ax - 50, ay), (rx + 20, ry), cls="edge loop")
    s.append(f'<text x="{ax - 38}" y="{ay + 30}" class="edge-label">rewrite · route</text>')
    s.append(f'<text x="{gx + 12}" y="{ay + 70}" class="edge-label" text-anchor="end">check answer</text>')
    gx2, gy2 = mid("generate", "b")
    s.append(f'<text x="{gx2 - 34}" y="{gy2 + 22}" class="edge-label">answer + citations</text>')
    s.append(f'<text x="{qx + 14}" y="{qy - 8}" class="edge-label">user question</text>')

    for n, (x, y, w, h) in NODES.items():
        title, mods = NODE_TITLE[n], lbl(n)
        s.append(f'<g class="node" data-stage="{n}" tabindex="0" role="button" aria-label="{E(title)}: show modules {E(mods)}">')
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>')
        if h >= 50:
            s.append(f'<text x="{x + w / 2}" y="{y + 22}" class="n-title">{E(title)}</text>')
            s.append(f'<text x="{x + w / 2}" y="{y + 40}" class="n-mods">{E(mods)}</text>')
        else:
            s.append(f'<text x="{x + w / 2}" y="{y + 25}" class="n-title">{E(title)} <tspan class="n-mods">{E(mods)}</tspan></text>')
        s.append("</g>")
    s.append("</svg>")
    return "\n".join(s)


def nb_link(r):
    p = parse_ref(r)
    opt = f' data-optional="1" data-reason="{p["reason"]}"' if p["optional"] else ""
    tag = (f'<span class="opt opt-{p["reason"]}" title="{E(REASONS[p["reason"]][1])}">Optional · {REASONS[p["reason"]][0]}</span>'
           if p["optional"] else '<span class="req">Mandatory</span>')
    return (f'<li class="nb"{opt}><a href="{p["url"]}" target="_blank" rel="noopener">'
            f'<span class="repo r{p["repo"]}">{p["repo"]}</span><span class="nb-path">{E(p["mod"])}/{E(p["file"])}</span></a>{tag}</li>')


def module_card(m):
    repos = sorted({s.split(":")[0] for s in m["sources"]})
    stages = " ".join(m["stages"])
    out = []
    out.append(f'<details class="module" id="m{m["num"]}" data-level="{m["level"]}" data-repos="{" ".join(repos)}" data-stages="{stages}">')
    out.append('<summary>')
    out.append(f'<span class="m-num">M{m["num"]:02d}</span>')
    out.append(f'<span class="m-head"><span class="m-title">{E(m["title"])}</span>'
               f'<span class="m-meta"><span class="lvl lvl-{m["level"]}">{LEVELS[m["level"]]}</span>'
               f'<span>~{m["hours"]} h</span><span>{len(m["lessons"])} lessons</span><span>{mod_counts(m)[0]} mandatory · {mod_counts(m)[1]} optional</span>'
               + "".join(f'<span class="repo r{r}">{r}</span>' for r in repos) + '</span></span>')
    out.append(f'<label class="done" title="Mark module complete"><input type="checkbox" id="done-m{m["num"]}" data-mod="{m["num"]}"><span>Done</span></label>')
    out.append('</summary>')
    out.append('<div class="m-body">')
    out.append(f'<p class="why">{code_fmt(m["why"])}</p>')
    out.append('<div class="m-cols"><div><h4>Learning objectives</h4><ul class="obj">')
    out += [f"<li>{code_fmt(o)}</li>" for o in m["objectives"]]
    out.append('</ul><h4>Key concepts</h4><ul class="chips">')
    t = theory_of(m)
    if t:
        url = f"{GH}/{COURSE_REPO}/blob/main/{t['readme']}"
        out += [f'<li><a href="{GH}/{COURSE_REPO}/blob/main/{concept_page(t, c)}" target="_blank" rel="noopener">{E(c)}</a></li>'
                for c in m["concepts"]]
        out.append(f'</ul><h4>Theory</h4><ul class="theory"><li><a href="{url}" target="_blank" rel="noopener">Theory page</a></li>')
        # the site is opened from docs/site/, so labs are linked relative to it and run locally
        out += [f'<li><a href="../../{path}" target="_blank" rel="noopener">Lab · {E(title)}</a></li>' for title, path in t["labs"]]
    else:
        out += [f"<li>{E(c)}</li>" for c in m["concepts"]]
    out.append('</ul></div><div><h4>Lessons</h4><ol class="lessons">')
    for i, (t, refs) in enumerate(m["lessons_r"], 1):
        all_opt = bool(refs) and all(parse_ref(x)["optional"] for x in refs)
        lcls = ' class="l-opt"' if all_opt else ""
        ltag = ' <span class="opt">Optional lesson</span>' if all_opt else ""
        out.append(f'<li{lcls}><span class="l-num">{m["num"]}.{i}</span><div class="l-body"><span class="l-title">{code_fmt(t)}{ltag}</span>')
        if refs:
            ordered = sorted(refs, key=lambda x: parse_ref(x)["optional"])
            out.append('<ul class="nbs">' + "".join(nb_link(r) for r in ordered) + "</ul>")
        else:
            out.append('<span class="lecture">Lecture and discussion</span>')
        out.append("</div></li>")
    out.append("</ol></div></div>")
    lab_nb = ""
    if m["lab_r"]:
        lab_nb = '<ul class="nbs">' + "".join(nb_link(r) for r in m["lab_r"]) + "</ul>"
    out.append(f'<div class="lab"><span class="lab-tag">Hands-on lab</span><p>{code_fmt(m["lab"])}</p>{lab_nb}</div>')
    out.append("</div></details>")
    return "\n".join(out)


def build_html():
    css = (SITE / "style.css").read_text()
    js = (SITE / "app.js").read_text()
    h = []
    a = h.append
    a(f"<title>{E(COURSE['title'])}</title>")
    a('<meta name="claude:viewport-fit-sides" content="cover">')
    a('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
    a('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap">')
    a(f"<style>{css}</style>")
    a('<div class="wrap">')
    # header
    a('<header class="hero">')
    a('<p class="eyebrow">Syllabus · built from ' + " + ".join(f'<a href="{GH}/{v[0]}" target="_blank" rel="noopener">repo {k}</a>' for k, v in REPOS.items()) + "</p>")
    a(f"<h1>{E(COURSE['title'])}</h1>")
    a(f'<p class="lede">{E(COURSE["subtitle"])}. {len(PARTS)} parts take you from your first LLM call through retrieval, agents, memory, multi-agent teams and MCP/A2A to knowledge graphs and Microsoft GraphRAG, with every notebook in all {len(REPOS)} repositories placed in exactly one lesson.</p>')
    a('<dl class="stats">')
    for k, v in [("Parts", len(PARTS)), ("Modules", len(MODULES)), ("Notebooks", n_nb), ("Mandatory", n_core), ("Hours", f"~{total_hours}"), ("Weeks", N_WEEKS)]:
        a(f"<div><dt>{k}</dt><dd>{v}</dd></div>")
    a("</dl></header>")

    # about
    a('<section class="about" aria-label="Course overview">')
    a('<div><h2 class="h-sm">Who it is for</h2><ul>' + "".join(f"<li>{code_fmt(x)}</li>" for x in COURSE["audience"]) + "</ul></div>")
    a('<div><h2 class="h-sm">Prerequisites</h2><ul>' + "".join(f"<li>{code_fmt(x)}</li>" for x in COURSE["prereqs"]) + "</ul></div>")
    a('<div class="span2"><h2 class="h-sm">You will be able to</h2><ol class="outcomes">' + "".join(f"<li>{code_fmt(x)}</li>" for x in COURSE["outcomes"]) + "</ol></div>")
    a("</section>")

    # diagram
    a('<section id="map"><div class="sec-head"><h2>Course map</h2><p>Select a stage to see the modules that teach it. The module list below filters to match.</p></div>')
    a('<div class="diagram-wrap">' + svg_diagram() + "</div>")
    a('<div id="stage-panel" class="stage-panel" aria-live="polite"><p class="hint">No stage selected. Showing all modules.</p></div>')
    a("</section>")

    # roadmap
    a(f'<section id="roadmap"><div class="sec-head"><h2>Roadmap</h2><p>{N_WEEKS} weeks at about {round(total_hours / N_WEEKS)} hours a week. Levels rise from Foundation to Expert.</p></div><ol class="road">')
    for p in PARTS:
        ms = mods_by_part[p["id"]]
        hrs = sum(m["hours"] for m in ms) + (CAP_HOURS if p["id"] == "capstone" else 0)
        chips = "".join(f'<a href="#m{m["num"]}" class="mchip">M{m["num"]}</a>' for m in ms)
        if p["id"] == "capstone":
            chips += '<a href="#capstones" class="mchip">Capstone</a>'
        a(f'<li class="road-item lvlb-{p["level"]}"><span class="road-when">{p["weeks"]}</span>'
          f'<a class="road-title" href="#{p["id"]}"><span class="pnum">Part {p["num"]}</span> {E(p["title"])}</a>'
          f'<span class="road-meta"><span class="lvl lvl-{p["level"]}">{LEVELS[p["level"]]}</span> ~{hrs} h</span>'
          f'<span class="road-chips">{chips}</span></li>')
    a("</ol></section>")

    # modules
    a('<section id="modules"><div class="sec-head"><h2>Modules</h2><p>Open a module for objectives, lessons, notebook links and the lab. Tick “Done” to track progress in this browser.</p></div>')
    a('<div class="toolbar" role="group" aria-label="Filter modules">')
    a('<div class="fgroup"><span class="flabel">Level</span>' + "".join(
        f'<button class="fchip" data-filter="level" data-value="{k}" aria-pressed="false"><span class="dot lvl-{k}"></span>{v}</button>' for k, v in LEVELS.items()) + "</div>")
    a('<div class="fgroup"><span class="flabel">Repo</span>' + "".join(
        f'<button class="fchip" data-filter="repo" data-value="{k}" aria-pressed="false"><span class="repo r{k}">{k}</span>{E(v[1])}</button>' for k, v in REPOS.items()) + "</div>")
    a('<div class="fgroup"><label class="toggle"><input type="checkbox" id="show-opt" checked> Show optional notebooks</label>'
      '<button class="tbtn" id="expand-all">Expand all</button><button class="tbtn" id="collapse-all">Collapse all</button></div>')
    a(f'<div class="progress"><span id="prog-text">0 of {len(MODULES)} modules done</span><span class="bar"><span id="prog-bar"></span></span></div>')
    a("</div>")
    a('<div class="tiers"><div class="tier-head"><h3>Mandatory vs optional</h3>'
      f'<p>You do not need every notebook. <strong>{n_core} of {n_nb}</strong> are mandatory: each lesson keeps the one notebook (two, when they teach two distinct ideas) needed for the lesson objective and the module lab. '
      'Untick “Show optional notebooks” for the mandatory-only track.</p></div><div class="tier-grid">'
      f'<div class="tier"><span class="req">Mandatory</span><b>{n_core}</b><p>Do these in order. The labs depend on them.</p></div>'
      + "".join(f'<div class="tier"><span class="opt opt-{k}">Optional · {v[0]}</span><b>{reason_counts[k]}</b><p>{E(v[1])}.</p></div>' for k, v in REASONS.items())
      + '</div></div>')
    a('<p id="filter-note" class="filter-note" hidden></p>')
    for p in PARTS:
        a(f'<div class="part" id="{p["id"]}"><div class="part-head"><span class="part-num">Part {p["num"]}</span>'
          f'<h3>{E(p["title"])}</h3><span class="part-when">{p["weeks"]}</span><p>{E(p["summary"])}</p></div>')
        for m in mods_by_part[p["id"]]:
            a(module_card(m))
        a("</div>")
    a("</section>")

    # capstones
    a('<section id="capstones"><div class="sec-head"><h2>Capstone projects</h2><p>Pick one. Each ships a working system, an evaluation report on a golden question set, and a 10-minute demo.</p></div><div class="caps">')
    for i, c in enumerate(CAPSTONES):
        a(f'<article class="cap"><span class="cap-letter">{chr(65 + i)}</span><span class="lvl lvl-{c["level"]}">{LEVELS[c["level"]]}</span>'
          f'<h3>{E(c["title"])}</h3><p>{E(c["brief"])}</p><ul>' + "".join(f"<li>{E(r)}</li>" for r in c["requires"]) + "</ul></article>")
    a("</div></section>")

    # assessment
    a('<section id="assessment"><div class="sec-head"><h2>Assessment</h2></div><div class="tbl"><table><thead><tr><th>Component</th><th>Weight</th><th>What is assessed</th></tr></thead><tbody>')
    for c, w, d in ASSESSMENT:
        a(f'<tr><td>{E(c)}</td><td class="num">{w}</td><td>{E(d)}</td></tr>')
    a("</tbody></table></div></section>")

    # gaps
    a('<section id="gaps"><div class="sec-head"><h2>Recommended additions</h2><p>Topics a complete RAG course needs that the source repositories do not cover. Listed so the gaps are explicit.</p></div><div class="gaps">')
    for g in GAPS:
        cls = {"Partial": "st-partial", "Planned": "st-planned"}.get(g["status"], "st-missing")
        a(f'<article class="gap"><div class="gap-head"><h3>{E(g["title"])}</h3><span class="status {cls}">{E(g["status"])}</span></div><p>{code_fmt(g["detail"])}</p></article>')
    a("</div></section>")

    # appendix
    a('<section id="coverage"><div class="sec-head"><h2>Source coverage</h2><p>Every source module in the source repositories and the course modules that use its notebooks.</p></div><div class="tbl"><table><thead><tr><th>Repo</th><th>Source module</th><th class="num">Notebooks</th><th class="num">Mandatory</th><th>Course modules</th></tr></thead><tbody>')
    for key in sorted(src_counts):
        cm = " ".join(f'<a href="#m{n}" class="mchip">M{n}</a>' for n in sorted(coverage.get(key, [])))
        a(f'<tr><td><span class="repo r{key[0]}">{key[0]}</span></td><td><code>{E(key[1])}</code></td><td class="num">{src_counts[key]}</td><td class="num">{src_core[key]}</td><td>{cm}</td></tr>')
    a('<tr><td><span class="repo r09">09</span></td><td><code>12_cacherag</code></td><td class="num">0</td><td class="num">0</td><td>Planned in repo</td></tr>')
    a("</tbody></table></div></section>")
    a('<footer class="foot">Notebook links point to this repository’s <code>main</code> branch on GitHub; the source repositories stay canonical. Optional notebooks are alternates, platform-specific variants or extensions; the mandatory track is enough to complete every lab.</footer>')
    a("</div>")
    a(f"<script>{js}</script>")
    return "\n".join(h)




# ---------- folder READMEs ----------
GEN_NOTE = ("> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. "
            "Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).\n")
PART_BY_ID = {p["id"]: p for p in PARTS}


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def write(path, text):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n")


def module_readme(m):
    global MD_FROM
    MD_FROM = module_dir(m)
    p = PART_BY_ID[m["part"]]
    mc, oc = mod_counts(m)
    L = [f"# M{m['num']:02d} — {m['title']}\n", GEN_NOTE,
         f"**Part {p['num']} · {p['title']}** · **Level:** {LEVELS[m['level']]} · **Time:** ~{m['hours']} h · "
         f"**Notebooks:** {mc} mandatory, {oc} optional\n",
         "## Why it matters\n", m["why"] + "\n"]
    t = theory = theory_of(m)
    concepts = " · ".join(m["concepts"])
    if t:
        page = os.path.relpath(ROOT / t["readme"], ROOT / MD_FROM)
        L += ["## Theory\n", f"Read the [theory page]({page}) before the notebooks: the module overview and interview "
              "questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. "
              f"[`index.html`]({os.path.relpath(ROOT / t['readme'].replace('README.md', 'index.html'), ROOT / MD_FROM)}) "
              "has the module and its lessons as one page (open it in a browser).\n"]
        L += [f"- Interactive lab: [{title}]({os.path.relpath(ROOT / path, ROOT / MD_FROM)}) (open the file in a browser)"
              for title, path in t["labs"]]
        L.append("")
        concepts = " · ".join(f"[{c}]({os.path.relpath(ROOT / concept_page(t, c), ROOT / MD_FROM)})" for c in m["concepts"])
    L.append("## Learning objectives\n")
    L += [f"- {o}" for o in m["objectives"]]
    L += ["\n## Lessons\n", "Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.\n",
          "| # | Topic | Mandatory | Optional |", "|---|---|---|---|"]
    for i, (t, refs) in enumerate(m["lessons_r"], 1):
        core = [f"[`{it.file}`]({md_href(it)})" for it in refs if not it.optional]
        opt = [f"[`{it.file}`]({md_href(it)}) *({REASONS[it.tier][0].lower()})*" for it in refs if it.optional]
        if not refs:
            core = ["*Lecture / discussion*"]
        title = t + (" *(optional lesson)*" if refs and not core else "")
        if theory and i in theory["lessons"]:
            title += f" ([theory]({os.path.relpath(ROOT / theory['lessons'][i], ROOT / MD_FROM)}))"
        L.append(f"| {m['num']}.{i} | {title} | {'<br>'.join(core) or '—'} | {'<br>'.join(opt) or '—'} |")
    L += ["\n## Hands-on lab\n", f"{m['lab']} Details: [lab/README.md](lab/README.md).\n",
          "## Key concepts\n", concepts + "\n",
          "## Folder layout\n",
          "- `notebooks/` — mandatory track, plus the helper files those notebooks import",
          "- `optional/` — alternate, platform-specific and extension notebooks",
          "- `exercises/` — exercises and solutions, where the module has them",
          "- `projects/` — runnable sub-projects (e.g. MCP servers and clients), where the module has them",
          "- `assets/` — images and data used by this module's notebooks",
          "- `lab/` — the module lab brief\n",
          "## Where each file comes from\n", "| File | Source repo | Source path |", "|---|---|---|"]
    for _, refs in m["lessons_r"]:
        for it in refs:
            L.append(f"| `{it.folder}/{it.file}` | `{REPOS[it.repo][0]}` | `{it.source_path}` |")
    for it in m["lab_r"]:
        L.append(f"| `{it.folder}/{it.file}` | `{REPOS[it.repo][0]}` | `{it.source_path}` |")
    write(f"{MD_FROM}/README.md", "\n".join(L))
    write(f"{MD_FROM}/lab/README.md", "\n".join([
        f"# Lab — M{m['num']:02d} {m['title']}\n", GEN_NOTE, "## Brief\n", m["lab"] + "\n",
        "## How to report it\n",
        f"- Use the golden question set and the baseline from the {BASE_M} lab.",
        "- Report the change against that baseline: retrieval metrics, answer quality, latency and cost where relevant.",
        "- Put your notebook or script in this folder and record results in a short table.\n",
        "Back to the module: [README.md](../README.md)"]))


def part_readme(p):
    ms = mods_by_part[p["id"]]
    L = [f"# Part {p['num']} — {p['title']}\n", GEN_NOTE, f"**{p['weeks']} · {LEVELS[p['level']]}**\n", p["summary"] + "\n",
         "| Module | Level | Time | Mandatory | Optional |", "|---|---|---|---|---|"]
    for m in ms:
        mc, oc = mod_counts(m)
        L.append(f"| [M{m['num']:02d} {m['title']}]({m['folder']}/README.md) | {LEVELS[m['level']]} | ~{m['hours']} h | {mc} | {oc} |")
    if p["id"] == "capstone":
        L.append(f"\nThen pick one of the [capstone projects](../../capstones/README.md) (~{CAP_HOURS} h).")
    write(f"course/{p['folder']}/README.md", "\n".join(L))


def course_readme():
    L = ["# Course\n", GEN_NOTE, "| Part | Title | When | Level | Modules |", "|---|---|---|---|---|"]
    for p in PARTS:
        ms = ", ".join(f"[M{m['num']:02d}]({p['folder']}/{m['folder']}/README.md)" for m in mods_by_part[p["id"]])
        L.append(f"| [{p['num']}]({p['folder']}/README.md) | {p['title']} | {p['weeks']} | {LEVELS[p['level']]} | {ms} |")
    write("course/README.md", "\n".join(L))


def theory_index():
    L = ["# Theory\n",
         "> The index is generated by `scripts/build_curriculum.py`. The pages are hand-written: edit "
         "`theory/<part>/<module>/README.md` and its lesson folders (see `CLAUDE.md` → Theory pages).\n",
         "Laid out like `course/`: one folder per module, one subfolder per lesson. A module page has the overview, "
         "interview questions and takeaways; each lesson page explains that lesson's concepts with diagrams. Each module's "
         "`index.html` joins its pages into one page to read in a browser. Some lessons "
         "have interactive labs (single HTML files, open them in a browser).\n",
         "| Module | Theory | Lessons with theory | Interactive labs |", "|---|---|---|---|"]
    for p in PARTS:
        L.append(f"| **Part {p['num']} · {p['title']}** | | | |")
        for m in mods_by_part[p["id"]]:
            t = theory_of(m)
            rel = lambda path: os.path.relpath(path, THEORY)  # noqa: E731
            page = (f"[README.md]({rel(t['readme'])})<br>[index.html]({rel(t['readme'].replace('README.md', 'index.html'))})"
                    if t else "*planned*")
            lessons = "<br>".join(f"[{m['num']}.{n} {m['lessons'][n - 1]['title']}]({rel(path)})"
                                  for n, path in t["lessons"].items()) if t else ""
            labs = "<br>".join(f"[{title}]({rel(path)})" for title, path in t["labs"]) if t else ""
            L.append(f"| M{m['num']:02d} {m['title']} | {page} | {lessons or '—'} | {labs or '—'} |")
    write(f"{THEORY}/README.md", "\n".join(L))


def capstone_readmes():
    idx = ["# Capstone projects\n", GEN_NOTE, f"Pick one (~{CAP_HOURS} h). Each ships a working system, an evaluation report on a golden question set, and a 10-minute demo.\n",
           "| | Capstone | Level |", "|---|---|---|"]
    for i, c in enumerate(CAPSTONES):
        folder = f"{chr(65 + i)}_{slugify(c['title'])}"
        idx.append(f"| {chr(65 + i)} | [{c['title']}]({folder}/README.md) | {LEVELS[c['level']]} |")
        write(f"capstones/{folder}/README.md", "\n".join(
            [f"# Capstone {chr(65 + i)} — {c['title']}\n", GEN_NOTE, f"**Level:** {LEVELS[c['level']]}\n", c["brief"] + "\n",
             "## Must include\n"] + [f"- {x}" for x in c["requires"]] +
            ["\n## Deliverables\n", "- A working system (notebook or small app) in this folder",
             f"- An evaluation report on a golden question set, compared with the {BASE_M} baseline",
             "- A 10-minute demo\n", "Assessment weights are in [CURRICULUM.md](../../CURRICULUM.md#assessment)."]))
    write("capstones/README.md", "\n".join(idx))



def notice():
    """NOTICE.md: which files are not under this repo's MIT licence, found from the source repos' curriculum maps."""
    dest = {(it.repo, it.source_path): it.dest for it in ITEMS}
    anthology = []
    for repo in CUR["sources"]:
        cmap = ROOT / f"docs/source/{repo}/curriculum-map.md"
        if not cmap.exists():
            continue
        for line in cmap.read_text().splitlines():
            m = re.search(r"\]\(\.\./(modules/[^)]+\.ipynb)\)", line)
            if line.startswith("|") and "RAG Techniques anthology" in line and m and (repo, m.group(1)) in dest:
                anthology.append(dest[(repo, m.group(1))])
    eco = [it.dest for it in ITEMS if it.source_path.endswith("01_rag_ecosystem.ipynb")]
    L = ["# Notice: third-party content\n", GEN_NOTE,
         "Original content is MIT-licensed (see [LICENSE](LICENSE)). The files below keep their own licences.\n",
         "## RAG Techniques anthology (non-commercial)\n",
         "From Nir Diamant's [RAG_Techniques](https://github.com/NirDiamant/RAG_Techniques), under its non-commercial licence "
         "([docs/third_party/RAG_Techniques_LICENSE.txt](docs/third_party/RAG_Techniques_LICENSE.txt)). This covers the notebooks below "
         "and the helpers, scripts and sample data that come with them.\n"]
    L += [f"- [`{p}`]({p})" for p in sorted(anthology)]
    L += ["\n## RAG Ecosystem (MIT)\n",
          "A fork of [FareedKhan-dev/rag-ecosystem](https://github.com/FareedKhan-dev/rag-ecosystem) "
          "([docs/third_party/RAG_Ecosystem_LICENSE.txt](docs/third_party/RAG_Ecosystem_LICENSE.txt)):\n"]
    L += [f"- [`{p}`]({p})" for p in eco]
    def placed(repo, prefix, pattern=""):
        return sorted({it.dest for it in ITEMS if it.repo == repo and it.source_path.startswith(prefix)
                       and re.search(pattern, it.source_path)})

    mcp = "modules/01_mcp_foundations/"
    third = [
        ("DeepLearning.AI and Anthropic, *MCP: Build Rich-Context AI Apps with Anthropic*",
         placed("10", mcp + "notebooks/0") + placed("10", mcp + "projects/lesson")),
        ("Educative, *MCP Fundamentals* and *Mastering MCP*",
         placed("10", mcp + "projects/wikipedia_assistant") + placed("10", "modules/02_building_mcp_servers/projects/", r"projects/0[123]_")),
        ("*MCP Essential* series (piyushagni5/langgraph-ai), **GPL-3.0**: see the `License` file in the same folder. "
         "Lab 2's `fetch_server` is the MIT-licensed reference server from modelcontextprotocol/servers",
         placed("10", "modules/03_building_mcp_clients/projects/")),
        ("Laxmi Kant Tiwari (KGP Talkie), *MCP Mastery: Build AI Apps with Claude, LangChain and Ollama* (Udemy)",
         placed("10", "modules/04_mcp_applications/projects/")),
    ]
    L += ["\n## Third-party MCP course material (repo 10)\n",
          "Repo 10 reproduces these lessons as found in its source repository; each keeps its original authors' terms, "
          "which have not been independently confirmed. Repo 10's own material (the A2A notebooks, the Databricks Apps server "
          "and the MCP + A2A capstone) is MIT.\n"]
    for title, paths in third:
        L += [f"### {title}\n"] + [f"- [`{p}`]({p})" for p in paths] + [""]
    L += ["## Course material adapted in repos 01, 02 and 04 (MIT repos, attributed)\n",
          "- M01–M02: Analytics Vidhya, *Coding Essentials for Agents*",
          "- M03: Udemy, *Complete Hugging Face Bootcamp* and *Mastering Generative AI with LLMs: A Hugging Face Guide*",
          "- M04: DeepLearning.AI, *Finetuning Large Language Models* (Sharon Zhou, Lamini)",
          "- M05–M06: the *Prompt Engineering Demystified* collection (notebooks credited to Dipanjan (DJ)), referencing Analytics Vidhya *Prompt Engineering Essentials*",
          "- M09–M10: reference course Analytics Vidhya *Building Advanced AI Agents with LangGraph*",
          "",
          "Third-party slides, media and datasets remain the property of their authors; each source repo's `data-sources.md` is archived under [docs/source/](docs/source/)."]
    mk = {m["key"]: m for m in MODULES}

    def mods(*keys):
        return " and ".join(f"M{mk[a]['num']:02d}–M{mk[b]['num']:02d}" if b else f"M{mk[a]['num']:02d}" for a, b in keys)

    L += ["\n## Other adapted material (MIT)\n",
          f"- `agentic_patterns` library by neural-maze, vendored in {mods(('agentloop', None))} (`{module_dir(mk['agentloop'])}/`)",
          f"- Several notebooks in {mods(('workflows', 'appliedagents'), ('ltmemory', 'collab'))} adapted from [FareedKhan-dev/all-agentic-architectures](https://github.com/FareedKhan-dev/all-agentic-architectures)",
          f"- Workflow-pattern notebooks ({mods(('workflows', None))}) follow Anthropic's *Building Effective Agents*\n",
          "## Provenance\n",
          "[docs/content-inventory.csv](docs/content-inventory.csv) maps every file to its source repository and path. "
          "Each source repository's own licence and inventory are archived under [docs/source/](docs/source/)."]
    write("NOTICE.md", "\n".join(L))


if __name__ == "__main__":
    MD_FROM = ""
    write("CURRICULUM.md", build_md())
    html_out = build_html()
    data = {"stages": {k: {"label": STAGES[k], "mods": v} for k, v in stage_mods.items()},
            "titles": {m["num"]: m["title"] for m in MODULES}, "levels": {m["num"]: m["level"] for m in MODULES}}
    write("docs/site/index.html", html_out.replace("/*__DATA__*/", "const DATA = " + json.dumps(data) + ";"))
    course_readme()
    for p in PARTS:
        part_readme(p)
    for m in MODULES:
        module_readme(m)
    theory_index()
    build_theory_html.main()
    capstone_readmes()
    notice()
    build_docs.main()
    print(f"rendered: {len(MODULES)} modules, {n_nb} notebooks ({n_core} mandatory, {n_opt} optional), ~{total_hours} h")
