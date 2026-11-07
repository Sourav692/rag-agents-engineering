# Production AI Engineering: proposed curriculum

Draft for review, 7 November 2026. This is the companion track to the AI Engineering course in [CURRICULUM.v2.md](CURRICULUM.v2.md): the course teaches how to build LLM applications, RAG systems and agents; this track teaches how to know they work, keep them safe and watch them in production. It enhances the existing `production-ai` track on forwarddeployedprep.com (slug frozen) and will be built later from two local source repositories. Nothing here has been built yet.

## Sources

| Key | Repository (local, under `~/Github_Repos/1. AIE_DEMYSTIFIED/`) | What it gives this track |
|---|---|---|
| `EV` | `Agent_Evaluation_Demystified` | `new_course/`: a finished 16-week evaluation track on one customer-support refund agent; every week has theory, an offline hands-on lab (`lab.py`, notebook, tests) and a dataset. `courses/01`, `03`, `04`: the same ideas in DeepEval, RAGAS and LangGraph. `courses/02`: Databricks and MLflow 3 (platform, optional). |
| `PO` | `ai-engineering-demystified-13-production-observability` | 18 notebooks in 10 modules: tracing, cost and tokens, caching and streaming, reliability and fallbacks, testing, safety and guardrails, red teaming, security and PII. Modules 06 (serving) and 10 (DevOps) have no notebooks yet. |

Not used: `EV/archive/` (superseded) and `EV/_personal/third-party/` (third-party Arize Phoenix labs; not ours to republish).

Codes below: `EV w05` is `new_course/weeks/week-05-*`; `EV c01/06` is `courses/01-rag-agent-tool-evaluation/06_*.ipynb`; `PO m07` is `modules/07_safety_and_guardrails/`.

## Design rules

- **One system, start to finish.** The `EV new_course` refund agent is the running example: each module extends the previous one's harness, as the source track does. Framework notebooks (`EV courses`) are the second, optional notebook per module, so each idea is seen in a named tool as well.
- **Offline first.** Every mandatory lab runs with no API key, as `EV new_course` already does. Live, paid or platform runs (OpenAI judges, LangSmith, Databricks) are optional and say so.
- **No duplication with the course.** The course keeps the measurement its labs need: the golden set and baseline in M10, tool-call evaluation in M22.5, guardrails in M28.3 and end-to-end evaluation in M46.2. This track starts where those stop and links back to them.
- **Same layout as the course.** Each module gets `mandatory/{theory,notebook}`, `optional/{theory,notebook}` and `lab/` with `solution/` and `data/`, as in [plan/README.md](plan/README.md).

## Parts and modules

### Part I: Evaluation foundations

| Module | Lessons | Mandatory | Optional |
|---|---|---|---|
| PA01 The evaluation lifecycle | What can be measured and with what scorer; string, schema and rubric checks; offline, online and human evaluation | `EV w01` | `EV c01/00` |
| PA02 Golden datasets and test design | Cases, labels and provenance; stratification by risk and question type; growing the set from production traces | `EV w02` | `EV c03/03`, `EV c02/04` |
| PA03 Model judges and human calibration | Judge prompts and rubrics; G-Eval and custom judges; agreement with human labels; judge drift | `EV w03` | `EV c03/08`, `EV c03/09`, `EV c02/03`, `EV c02/07` |

### Part II: Evaluating RAG

| Module | Lessons | Mandatory | Optional |
|---|---|---|---|
| PA04 Retrieval evaluation | Deterministic metrics (hit rate, recall@k, MRR, nDCG); LLM-judged context precision and recall | `EV w04` | `EV c01/01`, `EV c01/02` |
| PA05 Answer quality and evidence | Faithfulness and groundedness; reference-based and referenceless generator metrics; RAGAS in practice | `EV w05` | `EV c01/03`, `EV c01/04`, `EV c01/06` |
| PA06 RAG regression comparisons | Evaluation inside the pipeline; comparing two system versions on one set; when a difference is real | `EV w06` | `EV c01/05`, `EV c01/07` |

### Part III: Evaluating agents

| Module | Lessons | Mandatory | Optional |
|---|---|---|---|
| PA07 Tools and side effects | Tool selection and argument checks; verifying persisted side effects; dry runs | `EV w07` | `EV c01/09`, `EV c03/05` |
| PA08 Trajectories and task completion | Trajectory scoring; task completion against a goal; handoffs between agents | `EV w08` | `EV c01/10`, `EV c01/12`, `EV c03/06` |
| PA09 Multi-turn state | Conversation-level metrics; state carried across turns; simulated users | `EV w09` | `EV c01/08`, `EV c02/09` |

### Part IV: Release engineering

| Module | Lessons | Mandatory | Optional |
|---|---|---|---|
| PA10 The evaluation harness and CI | One harness for every check; tests for LLM code; running evaluation in CI | `EV w11`, `PO m05` | `EV c01/11` |
| PA11 Release gates and reliable measurement | Gate thresholds per stratum; confidence intervals and sample size; prompt versioning and regression | `EV w12`, `EV w15` | `EV c03/10`, `EV c03/11`, `EV c02/05` |

### Part V: Observability

| Module | Lessons | Mandatory | Optional |
|---|---|---|---|
| PA12 Tracing and observability | Traces, spans and callbacks; tracing a LangGraph agent; logging and monitoring | `PO m01` (5 notebooks) | `EV c02/01` |
| PA13 Online evaluation and production monitoring | Scoring live traffic; turning traces into evaluation cases; the improvement loop | `EV w13` | `EV c02/06`, `EV c03/12`, `EV c02/08` |
| PA14 Cost, latency and performance | Token and cost monitoring; cost optimisation; caching and streaming | `PO m02`, `PO m03` | none |

### Part VI: Safety and security

| Module | Lessons | Mandatory | Optional |
|---|---|---|---|
| PA15 Guardrails and moderation | Moderating chains; rule-based and LLM guardrails; safety and policy checks as tests | `PO m07` | `EV c03/07` |
| PA16 Red teaming and adversarial testing | Faults and adversarial inputs; prompt injection through retrieved text and tool output; red teaming agents and RAG | `EV w10`, `PO m08` | `EV c04/09` |
| PA17 Security, privacy and multi-tenant governance | PII detection and redaction; tenant isolation and access control; audit logging | `EV w14`, `PO m09` | none |

### Part VII: Capstone

| Module | Lessons | Mandatory | Optional |
|---|---|---|---|
| PA18 Production-grade evaluation capstone | A shared evaluation platform for several teams; one system taken from golden set to gated release with tracing and guardrails | `EV w16` | `EV c01/13`, `EV c01/14` |

## How it fits the existing `production-ai` track

The site track today has 8 modules (T4.1 to T4.8) plus an "Agent engineering in production" section of four modules kept from T3. Under the site plan's rule that a lesson duplicates only when another teaches the same concept at equal or greater depth, the proposal is:

| Site module today | This curriculum | Proposal |
|---|---|---|
| T4.3 Evaluation and release gates | PA01 to PA11 | Expand into Parts I to IV; the T4.3 prose becomes their theory where it is deeper |
| T4.5 Observability | PA12, PA13 | Expand into Part V |
| T4.6 Cost and latency | PA14 | Keep T4.6 and add PA14's notebooks to it |
| T4.4 AgentOps | PA15, PA16 | Keep AgentOps for operations and the release pipeline; guardrails and red teaming move to Part VI |
| T4.2 Security and tenancy | PA17 | Merge; PA17 brings notebooks and a lab |
| T4.1 Enterprise RAG and access control, T4.7 Scaling, T4.8 Model adaptation and inference serving, Agent engineering in production | none | Unchanged |

## Gaps the sources do not cover

- **Serving and deployment.** `PO m06` and `PO m10` have no notebooks. T4.7 Scaling and T4.8 serving stay site prose until they do.
- **Reliability patterns** (`PO m04`: fallbacks, retries, async) overlap the course's LangGraph retries (M09.5) and the site's "Robust agents" module. Decide whether they join PA14 or that module before building.
- **Vendor coverage.** Tracing uses LangSmith (`PO m01`) and MLflow (`EV c02`). Arize Phoenix appears only in the third-party labs, which are excluded.

## Decisions before building

1. Approve the 18 modules and the expand-or-merge proposal for T4.2 to T4.6.
2. Confirm `EV new_course` as the spine and `EV courses` as optional depth.
3. Choose where `PO m04` reliability lands.
