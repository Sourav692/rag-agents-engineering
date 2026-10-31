"""Render each module's theory pages into one HTML page: theory/<part>/<module>/index.html.

A Mermaid block followed by `<!-- animated: diagrams/<name>.anim.html -->` is drawn as that animated SVG fragment
instead, with the controller from scripts/site/theory-anim.{css,js}; the README keeps the Mermaid for GitHub.

A `<!-- lab: interactive/<name>.html -->` line embeds that lab at that spot, in both pages, as a lazy frame with an
"Open full screen" link; the lab hides its own bar and intro when framed and posts its height to the page.

The module page (README.md) and the lesson pages it lists are joined in lesson order and set in the
Almanac design from scripts/site/theory.template.html. Labs and diagrams are linked relatively, so the
page works opened from disk; notebooks and Markdown pages link to GitHub. Called by build_curriculum.py;
never edit the output by hand.
"""
from __future__ import annotations

import html
import os
import re
from pathlib import Path

import markdown

from curriculum_lib import ROOT, load, theory_dir

GH = "https://github.com/Sourav692/rag-agents-engineering/blob/main/"
TEMPLATE = Path(__file__).parent / "site" / "theory.template.html"
ANIM_CSS = Path(__file__).parent / "site" / "theory-anim.css"
ANIM_JS = Path(__file__).parent / "site" / "theory-anim.js"
MARK = re.compile(r"<!-- animated: (\S+) -->")
LAB = re.compile(r"<!-- lab: (\S+) -->")


def slug(s):
    """GitHub's anchor for a heading, so a README link like `page.md#top-k` maps onto this page's ids."""
    return re.sub(r"[^\w\- ]", "", s.lower()).strip().replace(" ", "-")


def absolute(md, page):
    """Rewrite a page's relative links as repo-absolute ("/course/..."), so pages from different folders can be joined."""
    def fix(m):
        label, target = m.group(1), m.group(2)
        if target.startswith(("http", "#")):
            return m.group(0)
        path, _, frag = target.partition("#")
        full = os.path.normpath(os.path.join(os.path.dirname(page), path))
        return f"{label}(/{full}{'#' + frag if frag else ''})"
    for mark, name in ((MARK, "animated"), (LAB, "lab")):
        md = mark.sub(lambda m: f"<!-- {name}: /{os.path.normpath(os.path.join(os.path.dirname(page), m.group(1)))} -->", md)
    return re.sub(r"(!?\[[^\]]*\])\(([^)\s]+)\)", fix, md)


def flatten(d):
    """The module page with its Lessons table replaced by the lesson pages it links, in order."""
    md = absolute((ROOT / d / "README.md").read_text(), f"{d}/README.md")
    md = re.sub(r" Each idea has a page in the folder of the lesson that teaches it, listed under \[Lessons\]\(/?#lessons\)\. "
                r"This page has the overview, the interview questions and the takeaways\.", "", md)
    table = re.search(r"(?ms)^## Lessons\n.*?(?=^## |\Z)", md)
    if not table:
        return md
    lessons = []
    for num, title, cell in re.findall(r"^\| (\d+\.\d+) \| (.+?) \| (.+?) \|$", table.group(0), re.M):
        hit = re.search(r"\]\((/[^)#]+/README\.md)", cell)
        if not hit:
            continue
        page = hit.group(1)[1:]
        body = absolute((ROOT / page).read_text(), page)
        nbs = re.search(r" · Notebooks: (.*?) · \[All theory pages\]", body)
        body = body[body.index("\n## ") + 1:body.index("\n---\n*Previous")]
        # the lesson's name and notebooks sit under its first heading, so they read as part of that section
        head, rest = body.strip().split("\n", 1)
        tag = f"Lesson {num}: {html.escape(title)}" + (f". Notebooks: {nbs.group(1)}" if nbs else "")
        lessons.append(f'{head}\n\n<p class="lesson-of" markdown="span">{tag}</p>\n{rest}\n')
    return md.replace(table.group(0), "\n".join(lessons) + "\n")


def render(m, pages):
    """One module's index.html. `pages` maps a module page (theory/.../README.md) to its index.html."""
    d = theory_dir(m)
    here = ROOT / d

    def rel(path):
        return os.path.relpath(ROOT / path, here).replace(os.sep, "/")

    lesson_dirs = {}  # a lesson page of any module -> that module's index.html
    for page, index in pages.items():
        for p in (ROOT / page).parent.glob("*/README.md"):
            lesson_dirs[p.relative_to(ROOT).as_posix()] = index

    def link(target):
        if target.startswith(("http", "#")):
            return target
        path, _, frag = target[1:].partition("#")
        frag = f"#{frag}" if frag else ""
        if "/interactive/" in path or path.endswith(".svg"):
            return rel(path)  # labs and diagrams open from disk
        if path in pages:
            return (frag or "#") if pages[path] == f"{d}/index.html" else rel(pages[path]) + frag
        if path in lesson_dirs:
            return (frag or "#") if lesson_dirs[path] == f"{d}/index.html" else rel(lesson_dirs[path]) + frag
        return GH + path + frag

    md = flatten(d)
    title_line, rest = md.split("\n", 1)
    name = title_line.split(": ", 1)[1]
    num = f"M{m['num']:02d}"
    meta_line = next(line for line in rest.splitlines() if line.startswith("*Part"))
    part = re.match(r"\*(Part [IVX]+) · ([^·]+?) ·", meta_line)
    readme = re.search(r"\[Module README\]\(([^)]+)\)", meta_line).group(1)
    rest = rest.replace(meta_line, "", 1)
    footer = re.search(r"\n---\n\*(Previous:.*?)\*\s*\Z", rest, re.S)
    rest = rest[:footer.start()] if footer else rest

    blocks = []

    def keep(fragment):
        blocks.append(fragment)
        return f"\n\nBLOCK{len(blocks) - 1}X\n\n"

    def svg(path):
        svg_text = (ROOT / path.lstrip("/")).read_text()
        w, h = re.search(r'viewBox="0 0 (\d+) (\d+)"', svg_text).groups()
        alt = re.search(r"<desc[^>]*>(.*?)</desc>", svg_text, re.S)
        alt = html.escape(alt.group(1).strip() if alt else "", quote=True)
        return f'<figure class="diagram"><img src="{link(path)}" width="{w}" height="{h}" alt="{alt}"></figure>'

    def inline_md(text):
        text = re.sub(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)\)", lambda mt: f"[{mt.group(1)}]({link(mt.group(2))})", text)
        return markdown.markdown(text, extensions=["smarty"])

    def anim(path):
        frag = (ROOT / path.lstrip("/")).read_text()
        return re.sub(r"\A\s*<!--.*?-->\s*", "", frag, flags=re.S).strip()  # drop the fragment's own note

    animated = has_animation(m)
    if animated:
        rest = re.sub(r"```mermaid\n(?:(?!```).)*```\n" + MARK.pattern, lambda mt: keep(anim(mt.group(1))), rest, flags=re.S)
    rest = MARK.sub("", rest)

    def lab_frame(path):
        src = link(path)
        title = re.search(r"<title>(.*?)</title>", (ROOT / path.lstrip("/")).read_text(), re.S)
        title = html.escape(title.group(1).strip() if title else Path(path).stem)
        return (f'<figure class="lab-embed"><iframe src="{src}" title="{title}, interactive lab" loading="lazy" height="900"></iframe>'
                f'<figcaption>Interactive lab: {title}. <a href="{src}">Open full screen</a></figcaption></figure>')

    rest = LAB.sub(lambda mt: keep(lab_frame(mt.group(1))), rest)
    rest = re.sub(r"```mermaid\n(.*?)```", lambda mt: keep(
        '<figure class="sheet chart"><pre class="mermaid">' + html.escape(mt.group(1), quote=False) + "</pre></figure>"),
        rest, flags=re.S)
    rest = re.sub(r"!\[[^\]]*\]\((/[^)]+\.svg)\)", lambda mt: keep(svg(mt.group(1))), rest)
    rest = re.sub(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)\)", lambda mt: f"[{mt.group(1)}]({link(mt.group(2))})", rest)
    rest = re.sub(r"(?m)^(?!\s*(?:[-*]|\d+\.) )(?=\S)(.+)\n(\s*(?:[-*]|\d+\.) )", r"\1\n\n\2", rest)  # lists after a line
    rest = rest.replace("<details>\n", '<details markdown="1">\n')  # Check yourself answers are Markdown
    body = markdown.markdown(rest, extensions=["tables", "fenced_code", "sane_lists", "smarty", "md_in_html"])
    for i, frag in enumerate(blocks):
        body = body.replace(f"<p>BLOCK{i}X</p>", frag)
    body = body.replace("<table>", '<div class="sheet scroll"><table>').replace("</table>", "</table></div>")
    body = re.sub(r"<pre><code([^>]*)>", r'<pre class="sheet code"><code\1>', body)
    body = re.sub(r"<h3>(\d+\. )", r'<h3 class="q">\1', body)  # interview questions
    toc = []

    def h2(mt):
        text = re.sub(r"<[^>]+>", "", mt.group(1))
        toc.append((slug(text), html.unescape(text).split(":")[0]))  # text is already escaped HTML
        return f'<h2 id="{slug(text)}">{mt.group(1)}</h2>'

    body = re.sub(r"<h2>(.*?)</h2>", h2, body)
    lede, body = body.split("\n", 1) if body.startswith("<p>") else ("", body)
    lede = lede.replace("<p>", '<p class="module__lede">', 1)
    toc_html = "".join(f'<li><a href="#{hid}">{html.escape(t)}</a></li>' for hid, t in toc)

    meta = [f'<div><dt>Module</dt><dd><a href="{link(readme)}">{num} on GitHub</a></dd></div>',
            f'<div><dt>{part.group(1)}</dt><dd>{html.escape(part.group(2).strip())}</dd></div>']
    for lab in sorted(here.glob("*/interactive/*.html")):
        title = re.search(r"<title>(.*?)</title>", lab.read_text(), re.S)
        title = html.escape(title.group(1).strip() if title else lab.stem)
        meta.append(f'<div><dt>{title}</dt><dd><a class="btn btn--quiet" href="{rel(lab.relative_to(ROOT))}">Open the lab</a></dd></div>')
    page = TEMPLATE.read_text()
    for key, value in {
        "{{TITLE}}": html.escape(f"{num} {name[0].upper() + name[1:]} theory"),
        "{{DESCRIPTION}}": html.escape(f"{num} theory: {name}. Concepts, diagrams, interview questions and the module's labs.", quote=True),
        "{{NUM}}": num,
        "{{NAME}}": html.escape(name[0].upper() + name[1:]),
        "{{LEDE}}": lede,
        "{{META}}": "\n      ".join(meta),
        "{{BODY}}": body,
        "{{TOC}}": toc_html,
        "{{FOOTER}}": inline_md(footer.group(1)).removeprefix("<p>").removesuffix("</p>") if footer else "",
        "{{INDEX}}": GH + "theory/README.md",
    }.items():
        page = page.replace(key, value)
    page = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', page)
    if animated:
        page = page.replace("</style>", ANIM_CSS.read_text() + "</style>", 1)
        page = page.replace("</body>", f"<script>\n{ANIM_JS.read_text()}</script>\n</body>", 1)
    return page


def has_animation(m):
    d = ROOT / theory_dir(m)
    return any(MARK.search(p.read_text()) for p in [d / "README.md", *d.glob("*/README.md")])


def main():
    cur = load()
    mods = [m for m in cur["modules"] if (ROOT / theory_dir(m) / "README.md").exists()]
    pages = {f"{theory_dir(m)}/README.md": f"{theory_dir(m)}/index.html" for m in mods}
    for m in mods:
        (ROOT / theory_dir(m) / "index.html").write_text(render(m, pages))
    return len(mods)


if __name__ == "__main__":
    print(f"theory html: {main()} module page(s)")
