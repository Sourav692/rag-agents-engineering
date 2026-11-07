# API limits

The Larkspur API limits how many requests each API key can make per minute:

| Plan | Requests per minute |
|---|---|
| Starter | 60 |
| Business | 600 |
| Enterprise | 3,000 |

When a key goes over its limit, the API answers with status 429 and a Retry-After header that says how many seconds to wait. Requests that were rejected do not count towards the limit.

List endpoints return at most 100 items per page; use the next-page token to read the rest. A bulk endpoint counts as one request, however many servers it changes.

Limits apply per key, so splitting work across several keys in one project raises the total. Enterprise accounts can ask for a higher limit through a ticket in the Technical category.
