"""Build a notebook-grounded, one-page LangGraph reference in four formats."""
from pathlib import Path
import ast
import base64
import html
import io
import json
import tokenize

import fitz
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A3, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
FONTS = Path('/Users/sourav/.codex/skills/synced/7e618d16-82ee-46e4-b1da-ea23f2d020f1_7288f2e3-a48e-4650-a7a6-374ad2a79f90/canvas-design/canvas-fonts')
for name, file in [('Sans', 'InstrumentSans-Regular.ttf'), ('Bold', 'InstrumentSans-Bold.ttf'), ('Mono', 'IBMPlexMono-Regular.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONTS / file)))

GROUPS = [
    ('STATE', 'What moves through the graph', '#176355'),
    ('FLOW', 'Where execution goes next', '#32599C'),
    ('RUNTIME', 'How each run executes', '#965119'),
    ('PERSISTENCE', 'How work pauses and returns', '#754792'),
]

# Each entry: heading, module provenance, one-sentence explanation, code fragment.
CARDS = [
('State + reducers', '01, 12', 'Plain keys overwrite; reducers merge updates, so return only the new delta.', '''class State(TypedDict):
    n: int
    events: Annotated[list[str], add]
def step(s):
    return {"n": s["n"] + 1,
            "events": ["step"]}'''),
('Build, compile, invoke', '01', 'Nodes return partial updates; edges order work; compile creates the runnable.', '''g = StateGraph(State)
g.add_node("step", step)
g.add_edge(START, "step")
g.add_edge("step", END)
app = g.compile()
app.invoke({"n": 0, "events": []})'''),
('MessagesState + LLM node', '01, 02', 'add_messages appends new IDs and replaces matching IDs; return the new reply.', '''class Chat(MessagesState):
    topic: str
def chat(s):
    reply = llm.invoke(s["messages"])
    return {"messages": [reply]}
g = StateGraph(Chat)'''),
('Choose a state schema', '03', 'TypedDict is hints; dataclass adds defaults; Pydantic validates node inputs.', '''from dataclasses import dataclass
from pydantic import BaseModel
@dataclass
class Defaults: n: int = 0
class Validated(BaseModel):
    n: int = 0'''),
('Input / internal / output', '07', 'Separate the public I/O contract from internal channels; schemas are not access control.', '''class Input(TypedDict): question: str
class Output(TypedDict): answer: str
class Internal(Input, Output): calls: int
g = StateGraph(Internal,
    input_schema=Input,
    output_schema=Output)'''),
('Prune model context', '12', 'RemoveMessage deletes by ID with add_messages; preserve valid tool-call pairs.', '''from langchain_core.messages import RemoveMessage
def trim(s):
    old = s["messages"][:-2]
    return {"messages": [
        RemoveMessage(id=m.id) for m in old
    ]}'''),

('Conditional edges', '02', 'A router reads state and selects a registered destination without updating state.', '''def route(s):
    return "yes" if s["n"] > 0 else "no"
g.add_conditional_edges("check", route,
    {"yes": "accept", "no": "reject"})'''),
('Command = update + route', '04', 'Command changes state and chooses the next node; static outgoing edges still run.', '''def decide(s) -> Command[Literal["done"]]:
    return Command(
        update={"n": s["n"] + 1},
        goto="done")'''),
('Guard a cycle', '11', 'Loop until success or an explicit cap; recursion_limit counts supersteps, not node calls.', '''def again(s):
    stop = s["ok"] or s["n"] >= 3
    return END if stop else "work"
g.add_conditional_edges("check", again)
g.add_edge("work", "check")
app.invoke(inputs, {"recursion_limit": 20})'''),
('Subgraph: shared keys', '08', 'A compiled child can be a parent node when their state channels overlap.', '''child = child_builder.compile()
g.add_node("child", child)
g.add_edge(START, "child")
g.add_edge("child", END)'''),
('Subgraph: map schemas', '08', 'Wrap the child invocation to translate the parent input and child output.', '''def adapt(s):
    out = child.invoke({"text": s["task"]})
    return {"result": out["answer"]}
g.add_node("child_adapter", adapt)'''),
('Tool-call loop', '06, 08, 09', 'Bind tools to the model; route AI tool calls to ToolNode, then return to the LLM.', '''from langgraph.prebuilt import (
    ToolNode, tools_condition)
llm = llm.bind_tools(tools)
g.add_node("tools", ToolNode(tools))
g.add_conditional_edges("assistant", tools_condition)
g.add_edge("tools", "assistant")'''),

('Per-run configuration', '04, 07', 'RunnableConfig carries thread identity, tracing settings, and configurable run options.', '''from langchain_core.runnables import RunnableConfig
def node(s, config: RunnableConfig):
    lang = config["configurable"]["language"]
    return {"answer": lang}
app.invoke(inputs, {"configurable": {
    "thread_id": "t1", "language": "Hindi"}})'''),
('Runtime context', '04', 'Inject read-only run dependencies through context; graph updates belong in state.', '''from langgraph.runtime import Runtime
class Ctx(TypedDict): user_id: str
def node(s, runtime: Runtime[Ctx]):
    return {"owner": runtime.context["user_id"]}
g = StateGraph(S, context_schema=Ctx)
app.invoke(inputs, context={"user_id": "u1"})'''),
('Async node + ainvoke', '09, 12', 'Await I/O in async nodes and use ainvoke for the completed graph result.', '''async def chat(s):
    reply = await llm.ainvoke(s["messages"])
    return {"messages": [reply]}
g.add_node("assistant", chat)
result = await app.ainvoke(inputs, cfg)'''),
('Stream updates / values / tokens', '02, 09', 'updates emits node deltas; values emits full state; messages emits LLM chunks + metadata.', '''for state in app.stream(inputs, cfg,
    stream_mode="values"): print(state)
async for delta in app.astream(inputs, cfg,
    stream_mode="updates"): print(delta)
async for chunk, meta in app.astream(inputs, cfg,
    stream_mode="messages"): print(chunk.content)'''),
('Retry transient failures', '10, 12', 'Retry only matching errors with backoff; max_attempts includes the first attempt.', '''g.add_node("fetch", fetch,
    retry_policy=RetryPolicy(
        max_attempts=3, initial_interval=1,
        backoff_factor=2, max_interval=10,
        jitter=True, retry_on=ConnectionError))'''),
('Parallel fan-out + merge', '12', 'Same-step writes to one plain key conflict; use a suitable reducer and explicit join.', '''class Totals(TypedDict):
    score: Annotated[int, add]
g.add_edge(START, "a")
g.add_edge(START, "b")
g.add_edge(["a", "b"], "join")'''),

('Checkpoint + thread identity', '05, 12', 'Reuse thread_id to restore progress; RAM is for tests, SQLite persists to disk.', '''app = g.compile(checkpointer=InMemorySaver())
cfg = {"configurable": {"thread_id": "t1"}}
app.invoke(inputs, cfg)
with SqliteSaver.from_conn_string("ck.db") as db:
    app = g.compile(checkpointer=db)
    app.invoke(inputs, cfg)'''),
('Inspect, replay, fork', '05, 12', 'Inspect values/next/tasks; replay reruns later work; update_state applies reducers and forks.', '''snap = app.get_state(cfg)
hist = list(app.get_state_history(cfg))
prior = next(cp for cp in hist if cp.next)
app.invoke(None, prior.config)
fork = app.update_state(prior.config, {"n": 99})
app.invoke(None, fork)'''),
('Interrupt: approve / reject', '06', 'A dynamic pause needs a saver and thread; resume restarts the node from its beginning.', '''def review(s):
    decision = interrupt("Approve?")
    return Command(goto="yes" if
        decision == "approve" else "no")
app.invoke(Command(resume="approve"), cfg)'''),
('Interrupt: edit / validate', '06', 'Resume supplies the interrupt return value; validate it before returning an update.', '''def edit(s):
    text = interrupt({"draft": s["draft"]})
    while not isinstance(text, str):
        text = interrupt("Enter text")
    return {"draft": text}
app.invoke(Command(resume="new draft"), cfg)'''),
('Breakpoint / crash recovery', '06, 12', 'Static pauses and repaired failures continue with None; dynamic pauses use Command(resume=...).', '''app = g.compile(
    checkpointer=InMemorySaver(),
    interrupt_before=["review"])
app.invoke(inputs, cfg)
app.update_state(cfg, {"n": 7})
app.invoke(None, cfg)'''),
('Idempotent effects', '12', 'Retries can repeat effects; use durable atomic deduplication or a provider idempotency key.', '''ledger = {}  # Single-process sketch only
def pay_once(key):
    if key not in ledger:
        ledger[key] = provider_pay(key)
    return ledger[key]'''),
]

IMPORTS = '''from typing import Annotated, Literal, TypedDict
from operator import add
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import Command, interrupt, RetryPolicy
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver'''
ASSUMPTIONS = 'Independent patterns: g = builder; app = compiled graph. Supply named nodes, schemas, llm/tools, and inputs; cfg carries thread_id.'
RECALL = 'Interview recall: state stores data | edges choose work | reducers merge writes | checkpoints save progress | interrupts pause durably.'
TRAPS = 'Watch for: returning full history to an append reducer; effects before interrupt(); expecting checkpoints to guarantee exactly-once effects.'
DOCS = [
    ('Graph API', 'https://docs.langchain.com/oss/python/langgraph/graph-api'),
    ('Interrupts', 'https://docs.langchain.com/oss/python/langgraph/interrupts'),
    ('Streaming', 'https://docs.langchain.com/oss/python/langgraph/streaming'),
    ('Persistence', 'https://docs.langchain.com/oss/python/langgraph/persistence'),
]

def check_syntax():
    for title, _, _, code in CARDS:
        # Top-level await is permitted in notebooks; compile its AST without execution.
        compile(code, title, 'exec', ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
    assert len(CARDS) == 24

def markdown():
    parts = ['# LangGraph fundamentals - interview cheatsheet',
             '24 patterns from 19 notebooks across all 12 repository modules. Print the PDF on A3 landscape.',
             ASSUMPTIONS, '## Core imports', f'```python\n{IMPORTS}\n```']
    for gi, (group, subtitle, _) in enumerate(GROUPS):
        parts.append(f'## {group.title()} - {subtitle}')
        for i in range(gi * 6, gi * 6 + 6):
            title, mods, line, code = CARDS[i]
            parts.extend([f'### {i+1:02d}. {title} (modules {mods})', line, f'```python\n{code}\n```'])
    parts.extend(['## Interview recall', RECALL, TRAPS, '## Notebook sources'])
    for p in sorted((ROOT / 'modules').glob('*/notebooks/*.ipynb')):
        parts.append(f'- [{p.parent.parent.name}: {p.stem}]({Path("../..") / p.relative_to(ROOT)})')
    parts.extend(['## API checks', 'Examples follow the repository environment: LangGraph 1.2.12.'])
    parts.extend(f'- [{name}]({url})' for name, url in DOCS)
    (OUT / 'langgraph-interview-cheatsheet.md').write_text('\n\n'.join(parts) + '\n')

INK = '#1B2A31'
MUTED = '#4D5D66'

def pdf():
    w, h = landscape(A3)
    path = OUT / 'langgraph-interview-cheatsheet.pdf'
    c = canvas.Canvas(str(path), pagesize=(w,h))
    c.setTitle('LangGraph Fundamentals | Interview Cheatsheet')
    c.setAuthor('AI Engineering Demystified')
    c.setFillColor(HexColor('#F8F8F3')); c.rect(0,0,w,h,fill=1,stroke=0)

    def text(x, y, s, font='Sans', size=9, color=INK):
        assert 0 <= y <= h and 0 <= x <= w
        assert pdfmetrics.stringWidth(s, font, size) <= w-x-20, (s, 'page overflow')
        c.setFillColor(HexColor(color)); c.setFont(font,size); c.drawString(x,h-y,s)

    def wrap(s, font, size, width):
        lines=[]; current=''
        for word in s.split():
            new=(current+' '+word).strip()
            if pdfmetrics.stringWidth(new,font,size) > width and current:
                lines.append(current); current=word
            else: current=new
        return lines+[current]

    def code(x, y, s, width, size=8.0, leading=9.2):
        # Color tokens without altering literal code, whitespace, or indentation.
        lines=s.splitlines()
        for ln in lines:
            assert pdfmetrics.stringWidth(ln, 'Mono', size) <= width, (ln, width)
        spans = {i: [] for i in range(1,len(lines)+1)}
        try:
            for t in tokenize.generate_tokens(io.StringIO(s).readline):
                kind, val, start, end, _ = t
                if start[0] != end[0] or not val.strip(): continue
                col = INK
                if kind == tokenize.STRING: col = '#256850'
                elif kind == tokenize.COMMENT: col = '#63727A'
                elif kind == tokenize.NUMBER: col = '#985221'
                elif kind == tokenize.NAME and val in {'from','import','class','def','return','if','else','for','in','with','as','await','async','while','not','or','True','False','None'}: col = '#5F4895'
                spans[start[0]].append((start[1],end[1],col))
        except tokenize.TokenError: pass
        for i, ln in enumerate(lines,1):
            text(x,y+(i-1)*leading,ln,'Mono',size)
            for start,end,col in spans[i]:
                offset=pdfmetrics.stringWidth(ln[:start],'Mono',size)
                text(x+offset,y+(i-1)*leading,ln[start:end],'Mono',size,col)

    text(28,25,'AI ENGINEERING DEMYSTIFIED  /  REPO 04', 'Bold', 8.7, '#176355')
    text(28,57,'LangGraph fundamentals', 'Bold', 30)
    text(28,77,'INTERVIEW CHEATSHEET     24 code patterns  /  19 notebooks  /  12 modules', 'Sans', 10.1, MUTED)
    # A compact flow motif carries the visual graph reference.
    for j,(label,col) in enumerate([('STATE','#176355'),('NODE','#32599C'),('UPDATE','#965119'),('NEXT','#754792')]):
        x=770+j*99
        c.setFillColor(HexColor(col)); c.roundRect(x,h-53,83,24,4,stroke=0,fill=1)
        text(x+12,45,label,'Bold',9,'#FFFFFF')
        if j<3:
            c.setStrokeColor(HexColor('#839099')); c.setLineWidth(.7)
            c.line(x+85,h-41,x+96,h-41)
            c.line(x+93,h-38,x+96,h-41); c.line(x+93,h-44,x+96,h-41)
    text(770,72,'Read down each column.  Module numbers appear on every card.', 'Sans', 8.8, MUTED)

    c.setFillColor(HexColor('#EAF0ED')); c.roundRect(28,h-127,w-56,38,5,stroke=0,fill=1)
    text(40,103,'CORE IMPORTS', 'Bold', 8, '#176355')
    imports=IMPORTS.splitlines()
    code(135,103,'\n'.join(imports[:3]),505,7.6,9)
    code(665,103,'\n'.join(imports[3:]),485,7.6,9)

    gap=12; cw=(w-56-3*gap)/4
    card_top=163; card_h=99.5; row_gap=5
    for gi,(group,subtitle,accent) in enumerate(GROUPS):
        x=28+gi*(cw+gap)
        text(x,145,group,'Bold',11,accent)
        text(x,157,subtitle,'Sans',8,MUTED)
        for ri in range(6):
            idx=gi*6+ri; title,mods,line,s=CARDS[idx]
            top=card_top+ri*(card_h+row_gap)
            c.setFillColor(HexColor('#FFFFFF')); c.setStrokeColor(HexColor('#D7DEDB')); c.setLineWidth(.45)
            c.roundRect(x,h-top-card_h,cw,card_h,4,stroke=1,fill=1)
            c.setFillColor(HexColor(accent)); c.rect(x,h-top-card_h,2.2,card_h,stroke=0,fill=1)
            text(x+10,top+13,f'{idx+1:02d}', 'Bold',8.5,accent)
            text(x+29,top+13,title,'Bold',9.5)
            mod_label='M'+mods.replace(', ', '/')
            mod_w=pdfmetrics.stringWidth(mod_label,'Sans',6.8)
            text(x+cw-mod_w-8,top+13,mod_label,'Sans',6.8,MUTED)
            title_end=x+29+pdfmetrics.stringWidth(title,'Bold',9.5)
            assert title_end < x+cw-mod_w-12, (title,'title collision')
            desc=wrap(line,'Sans',8.25,cw-20)
            assert len(desc)<=2,(title,desc)
            for li,ln in enumerate(desc): text(x+10,top+26+li*9.2,ln,'Sans',8.25,MUTED)
            code_y=top+48
            code(x+10,code_y,s,cw-20,7.8,9.15)
            assert code_y+(len(s.splitlines())-1)*9.15 < top+card_h-5
    end=card_top+6*card_h+5*row_gap
    assert end < h-51
    text(28, end+15, RECALL, 'Bold', 8.8)
    text(28, end+28, TRAPS, 'Sans', 8.1, MUTED)
    text(28, h-12, ASSUMPTIONS, 'Sans', 7.2, MUTED)
    source='Source: modules 01-12 notebooks | LangGraph 1.2.12 | A3 landscape'
    sw=pdfmetrics.stringWidth(source,'Sans',7)
    text(w-28-sw,h-12,source,'Sans',7,MUTED)
    # Accessible source links remain clickable in the vector PDF.
    c.linkURL(DOCS[0][1], (28,h-29,350,h-15), relative=0, thickness=0)
    c.showPage(); c.save()
    doc=fitz.open(path)
    assert len(doc)==1
    doc[0].get_pixmap(matrix=fitz.Matrix(2.6,2.6),alpha=False).save(OUT/'langgraph-interview-cheatsheet.png')
    preview = ROOT / 'tmp' / 'pdfs'
    preview.mkdir(parents=True, exist_ok=True)
    doc[0].get_pixmap(matrix=fitz.Matrix(1.35,1.35),alpha=False).save(preview/'cheatsheet-preview.png')

def html_doc():
    formatter=HtmlFormatter(nowrap=True)
    def hc(s): return highlight(s,PythonLexer(),formatter)
    columns=[]
    for gi,(group,subtitle,accent) in enumerate(GROUPS):
        cards=[]
        for i in range(gi*6,gi*6+6):
            title,mods,line,code=CARDS[i]
            cards.append(f'<article><h3><span class="num">{i+1:02d}</span>{html.escape(title)}<small>M{mods.replace(", ", "/")}</small></h3><p>{html.escape(line)}</p><pre><code>{hc(code)}</code></pre></article>')
        columns.append(f'<section style="--accent:{accent}"><h2>{group}</h2><div class="sub">{subtitle}</div>{"".join(cards)}</section>')
    sans=base64.b64encode((FONTS/'InstrumentSans-Regular.ttf').read_bytes()).decode()
    bold=base64.b64encode((FONTS/'InstrumentSans-Bold.ttf').read_bytes()).decode()
    mono=base64.b64encode((FONTS/'IBMPlexMono-Regular.ttf').read_bytes()).decode()
    source_items=[]
    for p in sorted((ROOT/'modules').glob('*/notebooks/*.ipynb')):
        source_items.append(f'<li><a href="{html.escape(str(Path("../..")/p.relative_to(ROOT)))}">{html.escape(str(p.relative_to(ROOT)))}</a></li>')
    links=' · '.join(f'<a href="{url}">{name}</a>' for name,url in DOCS)
    css='''
*{box-sizing:border-box}body{margin:0;background:#e6ebe8;color:#1b2a31;font-family:Atlas,sans-serif}.page{margin:24px auto;padding:28px;max-width:1588px;background:#f8f8f3}.eyebrow{color:#176355;letter-spacing:1.5px;font-size:12px;font-weight:700}header{display:flex;justify-content:space-between;align-items:center;gap:20px}h1{font-size:42px;line-height:1;margin:15px 0 13px}header p{font-size:14px;color:#4d5d66}.path{display:flex;gap:9px;align-items:center}.path b{background:#176355;color:white;padding:10px 14px;border-radius:4px;font-size:13px}.path b:nth-of-type(2){background:#32599c}.path b:nth-of-type(3){background:#965119}.path b:nth-of-type(4){background:#754792}.imports{background:#eaf0ed;padding:12px;margin:8px 0 18px;display:flex;align-items:start;gap:24px}.imports strong{font-size:11px;white-space:nowrap;color:#176355}.imports pre{columns:2;column-gap:55px;margin:0;flex:1;font-size:11px;line-height:1.25}.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}h2{font-size:17px;margin:0 0 3px;color:var(--accent)}.sub{font-size:11px;color:#4d5d66;margin-bottom:9px}article{height:174px;margin-bottom:8px;padding:12px;border:1px solid #d7dedb;border-left:3px solid var(--accent);border-radius:5px;background:#fff}h3{display:flex;gap:9px;align-items:center;font-size:13px;line-height:1;margin:0 0 9px}h3 .num{color:var(--accent);font-size:12px}h3 small{margin-left:auto;font-size:9px;font-weight:400;color:#4d5d66;white-space:nowrap}article p{font-size:11px;line-height:1.25;color:#4d5d66;margin:0 0 10px;min-height:28px}pre{font-family:AtlasMono,monospace;font-size:10.4px;line-height:1.2;white-space:pre;margin:0}code{font-family:inherit}footer{padding-top:5px;font-size:11px;color:#4d5d66}footer p{margin:8px 0}footer strong{color:#1b2a31}.sources{max-width:1588px;margin:0 auto 32px;padding:0 28px;font-size:13px}.sources summary{cursor:pointer;font-weight:700}.sources li{margin:7px 0}a{color:#32599c}.k,.kn,.kd,.kc{color:#5f4895}.s,.s1,.s2{color:#256850}.c,.c1{color:#63727a}.mi,.mf{color:#985221}
@media(prefers-color-scheme:dark){body{background:#111c22;color:#e5edea}.page{background:#18252b}.eyebrow{color:#8acbb2}header p,.sub,article p,h3 small,footer{color:#bfcec9}.imports{background:#21372f}.imports strong{color:#8acbb2}article{background:#1e2e35;border-color:#43545a;border-left-color:var(--accent)}h2,.num{filter:brightness(1.7)}footer strong{color:#e5edea}a{color:#8eb7ef}.k,.kn,.kd,.kc{color:#b8a5ef}.s,.s1,.s2{color:#86ceb0}.c,.c1{color:#acbdb5}.mi,.mf{color:#e8b37e}}
@media(max-width:1100px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}header{display:block}.path{margin:15px 0}.imports pre{columns:1}.imports{overflow:auto}article{height:auto;min-height:135px}pre{overflow:auto}}
@media(max-width:600px){.page{margin:0;padding:18px}.grid{grid-template-columns:1fr}h1{font-size:32px}.path b{padding:7px;font-size:11px}.imports{display:block}.imports pre{margin-top:9px}}
@page{size:A3 landscape;margin:0}
@media print{html,body{background:white;color:#1b2a31}.page{width:420mm;height:297mm;max-width:none;margin:0;padding:7mm;background:#f8f8f3;print-color-adjust:exact;-webkit-print-color-adjust:exact}header{height:24mm}h1{font-size:30px}.eyebrow{font-size:9px}header p{font-size:10px}.path b{font-size:9px;padding:7px}.imports{margin:3mm 0 4mm;padding:8px}.imports pre{font-size:8px;line-height:1.3}.imports strong{font-size:8px}.grid{gap:3mm;grid-template-columns:repeat(4,minmax(0,1fr))}h2{font-size:12px}.sub{font-size:8px}article{height:35mm;margin-bottom:2mm;padding:8px;background:white;border-color:#d7dedb}h3{font-size:9px;margin-bottom:6px}h3 .num{font-size:8px}h3 small{font-size:6.5px}article p{font-size:8px;min-height:19px;margin-bottom:7px}pre{font-size:7.8px;line-height:1.2}footer{font-size:8px}footer p{margin:5px 0}.sources{display:none}header p,.sub,article p,h3 small,footer{color:#4d5d66}.imports{background:#eaf0ed}.eyebrow,.imports strong{color:#176355}h2,.num{filter:none}.k,.kn,.kd,.kc{color:#5f4895}.s,.s1,.s2{color:#256850}.c,.c1{color:#63727a}.mi,.mf{color:#985221}footer strong{color:#1b2a31}}
'''
    css += '''@media print{.page{padding:5mm}header{height:18mm}.imports{margin:2mm 0 3mm}article{height:33mm;margin-bottom:1.3mm;padding:7px}h3{font-size:10px;margin-bottom:6px}article p{font-size:9px;min-height:22px;margin-bottom:6px}pre{font-size:9px;line-height:1.15}footer{font-size:8px}footer p{margin:4px 0}}'''
    fonts=f'@font-face{{font-family:Atlas;src:url(data:font/ttf;base64,{sans})}}@font-face{{font-family:Atlas;font-weight:700;src:url(data:font/ttf;base64,{bold})}}@font-face{{font-family:AtlasMono;src:url(data:font/ttf;base64,{mono})}}'
    page=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>LangGraph interview cheatsheet</title><style>{fonts}{css}</style><body><main class="page"><header><div><div class="eyebrow">AI ENGINEERING DEMYSTIFIED / REPO 04</div><h1>LangGraph fundamentals</h1><p>INTERVIEW CHEATSHEET · 24 code patterns · 19 notebooks · 12 modules</p></div><div class="path"><b>STATE</b>→<b>NODE</b>→<b>UPDATE</b>→<b>NEXT</b></div></header><div class="imports"><strong>CORE IMPORTS</strong><pre><code>{hc(IMPORTS)}</code></pre></div><div class="grid">{''.join(columns)}</div><footer><p><strong>{html.escape(RECALL)}</strong></p><p>{html.escape(TRAPS)}</p><p>{html.escape(ASSUMPTIONS)}</p><p>Read down each column. Source: modules 01-12 notebooks · LangGraph 1.2.12 · Print: A3 landscape.</p></footer></main><details class="sources"><summary>Notebook sources and API checks</summary><p>{links}</p><ul>{''.join(source_items)}</ul></details></body></html>'''
    (OUT/'langgraph-interview-cheatsheet.html').write_text(page)

if __name__ == '__main__':
    check_syntax()
    markdown()
    html_doc()
    pdf()
    print('Created PDF, PNG, HTML, Markdown; 24 syntax-checked snippets.')
