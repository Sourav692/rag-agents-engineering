#!/usr/bin/env python3
"""Render a content-write Markdown lesson into a self-contained HTML page in the Forward Deployed house style.

Usage:
    python3 build_site.py lesson.md [lesson.html]

What it does:
  1. Reads the YAML frontmatter (title, subtitle, track, module_*, lessons, ...).
  2. Renders every ```mermaid block twice (light + dark) with mermaid-cli, using ../assets/mermaid-*.json.
  3. Embeds Bricolage Grotesque + Inter as base64 woff2 (from @fontsource-variable npm packages).
  4. Writes one HTML file that works offline, with a Light/Dark toggle.

Requirements: python3 with `markdown` and `pyyaml`; node + npm; a Chrome/Chromium for mermaid-cli.
Missing npm pieces are installed once into ~/.cache/content-write.
"""
import base64, html, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

import markdown
import yaml

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"
CACHE = Path(os.environ.get("CONTENT_WRITE_CACHE", Path.home() / ".cache" / "content-write"))
NPM_PKGS = ["@mermaid-js/mermaid-cli", "@fontsource-variable/bricolage-grotesque", "@fontsource-variable/inter"]


def ensure_npm() -> Path:
    mods = CACHE / "node_modules"
    if not all((mods / p).exists() for p in NPM_PKGS):
        CACHE.mkdir(parents=True, exist_ok=True)
        env = dict(os.environ)
        chrome = find_chrome()
        if chrome:
            env["PUPPETEER_SKIP_DOWNLOAD"] = "1"
        subprocess.run(["npm", "i", "--prefix", str(CACHE), *NPM_PKGS], check=True, env=env,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return mods


def find_chrome():
    for c in [os.environ.get("CHROME_PATH"), "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser",
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]:
        if c and Path(c).exists():
            return c
    return None


def render_mermaid(blocks, mods: Path, tmp: Path):
    mmdc = shutil.which("mmdc") or str(mods / ".bin" / "mmdc")
    pconf = tmp / "puppeteer.json"
    chrome = find_chrome()
    pconf.write_text(json.dumps({"args": ["--no-sandbox"], **({"executablePath": chrome} if chrome else {})}))
    out = []
    for i, code in enumerate(blocks):
        src = tmp / f"d{i}.mmd"
        src.write_text(code)
        pair = {}
        for theme in ("light", "dark"):
            dst = tmp / f"d{i}-{theme}.svg"
            r = subprocess.run([mmdc, "-p", str(pconf), "-c", str(ASSETS / f"mermaid-{theme}.json"), "-b", "transparent",
                                "-i", str(src), "-o", str(dst)], capture_output=True, text=True)
            if r.returncode != 0:
                sys.exit(f"Mermaid block {i + 1} failed to render ({theme}):\n{code}\n{r.stderr[-800:]}")
            svg = re.sub(r"<\?xml[^>]*>", "", dst.read_text()).replace("my-svg", f"mmd-{i}-{theme}")
            pair[theme] = svg
        out.append(pair)
    return out


def font_face(path: Path, family: str, weight: str, style="normal", stretch=None) -> str:
    b64 = base64.b64encode(path.read_bytes()).decode()
    return (f"@font-face{{font-family:'{family}';font-style:{style};font-weight:{weight};font-display:swap;"
            + (f"font-stretch:{stretch};" if stretch else "")
            + f"src:url(data:font/woff2;base64,{b64}) format('woff2-variations');}}")


def main():
    md_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else md_path.with_suffix(".html")
    src = md_path.read_text(encoding="utf-8")

    m = re.match(r"---\n(.*?)\n---\n", src, re.S)
    fm = yaml.safe_load(m.group(1)) if m else {}
    src = src[m.end():] if m else src
    g = lambda k, d="": fm.get(k, d) if fm.get(k) is not None else d

    mods = ensure_npm()
    blocks = re.findall(r"```mermaid\n(.*?)```", src, re.S)
    with tempfile.TemporaryDirectory() as t:
        svgs = render_mermaid(blocks, mods, Path(t))

    it = iter(svgs)
    def mermaid_sub(_):
        pair = next(it)
        inner = "".join(f'<div class="dg {th}">{pair[th]}</div>' for th in ("light", "dark"))
        return f'\n<figure class="diagram" markdown="0">{inner}</figure>\n'
    src = re.sub(r"```mermaid\n.*?```", mermaid_sub, src, flags=re.S)
    src = re.sub(r"^# .*\n(\n\*.*\*\n)?", "", src.lstrip(), count=1)   # h1 (+ italic subtitle) go in the header

    src = src.replace("<details>\n", '<details markdown="1">\n')   # Check yourself answers are Markdown
    body = markdown.markdown(src, extensions=["tables", "fenced_code", "toc", "md_in_html"])
    body = re.sub(r'<pre><code class="language-text">#### OUTPUT ####\n',
                  '<pre class="output"><span class="out-label">Output</span><code>', body)
    body = re.sub(r"<p><em>((?:Figure|Table) \d+:.*?)</em></p>", r'<p class="caption">\1</p>', body)
    body = re.sub(r"(<table>)", r'<div class="table-wrap">\1', body).replace("</table>", "</table></div>")

    def callout(mo):
        inner = mo.group(1)
        kind = "warn" if ("⚠️" in inner or "<strong>Pitfall" in inner) else "learn" if "What you'll learn" in inner else "note"
        return f'<aside class="callout {kind}">{re.sub(r"(👉|⚠️|💡)\s*", "", inner)}</aside>'
    body = re.sub(r"<blockquote>(.*?)</blockquote>", callout, body, flags=re.S)

    sections = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body))
    lessons = g("lessons", [g("title")])
    lesson_no = int(str(g("lesson", "1")).split()[0])
    total = len(lessons)
    side = "".join(
        f'<li class="{"active" if n == lesson_no else ""}"><span class="num">{n}</span><span>{html.escape(t)}</span></li>'
        + (f'<ul class="sections">{sections}</ul>' if n == lesson_no else "")
        for n, t in enumerate(lessons, 1))

    F = mods / "@fontsource-variable"
    fonts = (font_face(F / "bricolage-grotesque/files/bricolage-grotesque-latin-wdth-normal.woff2",
                       "Bricolage Grotesque", "200 800", stretch="75% 100%")
             + font_face(F / "inter/files/inter-latin-wght-normal.woff2", "Inter", "100 900")
             + font_face(F / "inter/files/inter-latin-wght-italic.woff2", "Inter", "100 900", "italic"))

    e = lambda k, d="": html.escape(str(g(k, d)))
    crumbs = " › ".join(html.escape(c) for c in ["Learn", g("track"), g("module_group"), g("module_name")] if c)
    meta4_label, meta4_value = ("Last updated", e("last_updated")) if g("last_updated") else ("Level", e("level").capitalize())
    css = (ASSETS / "site.css").read_text()

    page = f"""<!DOCTYPE html>
<html lang="en" data-theme="light"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e('title')} · {e('module_name')} · Forward Deployed</title>
<style>{fonts}
{css}</style></head>
<body>
<header class="topbar"><div class="brand"><i></i>Forward Deployed</div>
<nav class="nav"><span>Choose Your Path</span><span class="on">Learn</span><span>Casebook</span><span>Practice</span><span>Interview</span></nav>
<div class="spacer"></div><button class="theme" onclick="var r=document.documentElement;r.dataset.theme=r.dataset.theme==='dark'?'light':'dark'">Light / Dark</button></header>
<div class="crumbs">{crumbs} › <b>{e('title')}</b></div>
<div class="layout">
<aside class="side"><div class="back">← {e('module_group')}</div><div class="mod"><span>{e('module_code')}</span><span>{e('module_name')}</span></div>
<h6>Lessons</h6><ol>{side}</ol></aside>
<article>
<div class="strip"><b>{e('module_name')}</b><span>Lesson {lesson_no} of {total}</span><div class="bar"></div><span>0 of {total} read</span></div>
<div class="badge">Learn</div>
<h1>{e('title')}</h1>
<p class="subtitle">{e('subtitle')}</p>
<div class="meta"><div><small>Reading time</small>{e('reading_time')}</div><div><small>Source</small>{e('source', 'From the RAG & Agents Engineering course')}</div>
<div><small>By</small>{e('author', 'Sourav Banerjee')}</div><div><small>{meta4_label}</small>{meta4_value}</div></div>
<a class="report" href="#">Report an issue</a>
<hr class="rule">
<div class="prose">
{body}
</div></article></div></body></html>"""
    out_path.write_text(page, encoding="utf-8")
    print(f"wrote {out_path} ({len(page) // 1024} kB, {len(svgs)} diagrams)")


if __name__ == "__main__":
    main()
