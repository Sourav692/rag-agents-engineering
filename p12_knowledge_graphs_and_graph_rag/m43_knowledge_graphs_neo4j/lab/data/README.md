# M43 lab data

All files were written for this course and carry the repository's licence. Larkspur Cloud, its teams, people and incidents are fictional.

| Path | Source | Licence |
|---|---|---|
| [larkspur/](larkspur/README.md) | Unchanged copy of `data/larkspur/`: the 13 handbook files and the golden set | Repository licence |
| [extra_docs/](extra_docs/) | Seven internal records written for this lab, numbered after the handbook so the corpus is 20 documents: three team records (`14_team_platform.md`, `15_team_network.md`, `16_team_billing_systems.md`: lead, owned services, regions on call) and four incident records (`17_incident_inc104.md` to `20_incident_inc140.md`: date, region, service, monthly availability) | Repository licence |
| [multihop.jsonl](multihop.jsonl) | Five multi-hop questions written by the author: `id` (`m1` to `m5`), `question`, `hops` (the fact each document contributes) and `reference_answer` | Repository licence |

The records are written so that no question can be answered from one document. An incident record names a service and a region but never the team; a team record names its services and regions but no incident. The answer needs a join, which a graph query does in one hop per relationship and top-k vector retrieval can only do if every document on the path lands in the top k.
