# Capstone run log — smoke

- Produced by: `capstone_eval.py::main` (one file, all runs)
- Failures injected by: `capstone_stub.py` (a fake model server)
- Request path: `serve.py::ask` → `agent.py::run_agent` → `generate.py::generate`
- Log lines written by: `serve.py::_log_request`
- Runs: 1 · when: 2026-11-13 13:22
- Request log for this file: `results\capstone_2026-11-13_1319_smoke_requests.jsonl`

Cells and verdicts below are computed by the script from the checks in
`capstone_eval.py`. A criterion is MET only if every run meets its target.

| Criterion | Target | Run 1 | Verdict |
|---|---|---|---|
| 1. A temporary model failure recovers | 3 of 3 trials | 3/3 | MET |
| 2. A persistent model failure ends with a readable error, in time | 3 of 3 trials | 0/3 | MISSED |
| 3. Retries never exceed the limit | 3 of 3 trials | 3/3 | MET |
| 4. A hung call or an empty reply is treated as a failure | 3 of 3 trials per case | hang 3/3 · empty 3/3 | MET |
| 5. Every request writes one valid log entry, including failures | 3 of 3 batches | PASS (12/12 lines valid) | MET |

---

## What actually happened

# Run 1

## Criterion 1 — temporary failure recovers

**1 failure(s) then ok** — stub script `['503', 'ok']`

- stub received 3 call(s): 503, ok, ok
- took 5.77s
- **PASS**

Response:

```json
{
  "http_status": 200,
  "error": null,
  "fit_card": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.",
  "selected_item": "Y2K Baby Tee — Butterfly Print"
}
```

Log line(s) written for this request:

```
{"timestamp": "2026-11-13T18:19:43.360062+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 5767, "attempts": 2}
```

**2 failure(s) then ok** — stub script `['503', '503', 'ok']`

- stub received 4 call(s): 503, 503, ok, ok
- took 5.38s
- **PASS**

Response:

```json
{
  "http_status": 200,
  "error": null,
  "fit_card": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.",
  "selected_item": "Y2K Baby Tee — Butterfly Print"
}
```

Log line(s) written for this request:

```
{"timestamp": "2026-11-13T18:19:48.746466+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 5379, "attempts": 3}
```

**3 failure(s) then ok** — stub script `['503', '503', '503', 'ok']`

- stub received 5 call(s): 503, 503, 503, ok, ok
- took 9.3s
- **PASS**

Response:

```json
{
  "http_status": 200,
  "error": null,
  "fit_card": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.",
  "selected_item": "Y2K Baby Tee — Butterfly Print"
}
```

Log line(s) written for this request:

```
{"timestamp": "2026-11-13T18:19:58.055953+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 9301, "attempts": 4}
```

## Criteria 2 and 3 — every attempt fails

**every attempt: 503** — stub script `['503']`

- stub received 4 call(s): 503, 503, 503, 503
- took 7.09s
- criterion 2: **FAIL** (HTTP 500)
- criterion 3: **PASS** (attempts in log: 4, expected 4)

Response:

```json
{
  "http_status": 500,
  "error": "ModelUnavailable: The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.",
  "fit_card": null,
  "selected_item": null
}
```

Log line(s) written for this request:

```
{"timestamp": "2026-11-13T18:20:05.150795+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "ModelUnavailable: The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "failed", "duration_ms": 7087, "attempts": 4}
```

**every attempt: drop** — stub script `['drop']`

- stub received 4 call(s): drop, drop, drop, drop
- took 7.09s
- criterion 2: **FAIL** (HTTP 500)
- criterion 3: **PASS** (attempts in log: 4, expected 4)

Response:

```json
{
  "http_status": 500,
  "error": "ModelUnavailable: The model kept failing: RemoteProtocolError: Server disconnected without sending a response. (gave up after 3 retries). Try again in a moment.",
  "fit_card": null,
  "selected_item": null
}
```

Log line(s) written for this request:

```
{"timestamp": "2026-11-13T18:20:12.244155+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "ModelUnavailable: The model kept failing: RemoteProtocolError: Server disconnected without sending a response. (gave up after 3 retries). Try again in a moment.", "status": "failed", "duration_ms": 7085, "attempts": 4}
```

**every attempt: empty** — stub script `['empty']`

- stub received 4 call(s): empty, empty, empty, empty
- took 7.08s
- criterion 2: **FAIL** (HTTP 500)
- criterion 3: **PASS** (attempts in log: 4, expected 4)

Response:

```json
{
  "http_status": 500,
  "error": "ModelUnavailable: The model kept failing: EmptyReply: The model returned an empty reply. (gave up after 3 retries). Try again in a moment.",
  "fit_card": null,
  "selected_item": null
}
```

Log line(s) written for this request:

```
{"timestamp": "2026-11-13T18:20:19.326148+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "ModelUnavailable: The model kept failing: EmptyReply: The model returned an empty reply. (gave up after 3 retries). Try again in a moment.", "status": "failed", "duration_ms": 7074, "attempts": 4}
```

## Criterion 4 — hung call and empty reply

**hang, trial 1** — stub script `['hang', 'ok']`

- stub received 3 call(s): hang, ok, ok
- took 23.27s
- cut off after: 20.0s (limit 22s)
- **PASS**

Response:

```json
{
  "http_status": 200,
  "error": null,
  "fit_card": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.",
  "selected_item": "Y2K Baby Tee — Butterfly Print"
}
```

Log line(s) written for this request:

```
{"timestamp": "2026-11-13T18:20:42.601542+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 23265, "attempts": 2}
```

**hang, trial 2** — stub script `['hang', 'ok']`

- stub received 3 call(s): hang, ok, ok
- took 23.34s
- cut off after: 20.01s (limit 22s)
- **PASS**

Response:

```json
{
  "http_status": 200,
  "error": null,
  "fit_card": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.",
  "selected_item": "Y2K Baby Tee — Butterfly Print"
}
```

Log line(s) written for this request:

```
{"timestamp": "2026-11-13T18:21:05.943266+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 23333, "attempts": 2}
```

**hang, trial 3** — stub script `['hang', 'ok']`

- stub received 3 call(s): hang, ok, ok
- took 23.28s
- cut off after: 20.01s (limit 22s)
- **PASS**

Response:

```json
{
  "http_status": 200,
  "error": null,
  "fit_card": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.",
  "selected_item": "Y2K Baby Tee — Butterfly Print"
}
```

Log line(s) written for this request:

```
{"timestamp": "2026-11-13T18:21:29.223088+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 23273, "attempts": 2}
```

**empty reply, trial 1** — stub script `['empty', 'ok']`

- stub received 3 call(s): empty, ok, ok
- took 3.27s
- **PASS**

Response:

```json
{
  "http_status": 200,
  "error": null,
  "fit_card": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.",
  "selected_item": "Y2K Baby Tee — Butterfly Print"
}
```

Log line(s) written for this request:

```
{"timestamp": "2026-11-13T18:21:32.497286+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3265, "attempts": 2}
```

**empty reply, trial 2** — stub script `['empty', 'ok']`

- stub received 3 call(s): empty, ok, ok
- took 3.27s
- **PASS**

Response:

```json
{
  "http_status": 200,
  "error": null,
  "fit_card": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.",
  "selected_item": "Y2K Baby Tee — Butterfly Print"
}
```

Log line(s) written for this request:

```
{"timestamp": "2026-11-13T18:21:35.775187+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3271, "attempts": 2}
```

**empty reply, trial 3** — stub script `['empty', 'ok']`

- stub received 3 call(s): empty, ok, ok
- took 3.3s
- **PASS**

Response:

```json
{
  "http_status": 200,
  "error": null,
  "fit_card": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.",
  "selected_item": "Y2K Baby Tee — Butterfly Print"
}
```

Log line(s) written for this request:

```
{"timestamp": "2026-11-13T18:21:39.084852+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3302, "attempts": 2}
```

## Criterion 5 — one log line per request

Batch of 12 requests — **PASS**

| # | Request | HTTP | Log lines | Valid |
|---|---|---|---|---|
| 1 | success | 200 | 1 | yes |
| 2 | success | 200 | 1 | yes |
| 3 | success | 200 | 1 | yes |
| 4 | success | 200 | 1 | yes |
| 5 | missing query | 400 | 1 | yes |
| 6 | blank query | 400 | 1 | yes |
| 7 | temporary failure | 200 | 1 | yes |
| 8 | temporary failure | 200 | 1 | yes |
| 9 | temporary failure | 200 | 1 | yes |
| 10 | persistent failure | 500 | 1 | yes |
| 11 | persistent failure | 500 | 1 | yes |
| 12 | persistent failure | 500 | 1 | yes |

The log lines from this batch:

```
{"timestamp": "2026-11-13T18:21:41.343778+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 2251, "attempts": 1}
{"timestamp": "2026-11-13T18:21:43.620472+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 2270, "attempts": 1}
{"timestamp": "2026-11-13T18:21:45.878894+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 2249, "attempts": 1}
{"timestamp": "2026-11-13T18:21:48.166840+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 2280, "attempts": 1}
{"timestamp": "2026-11-13T18:21:48.173925+00:00", "query": null, "output": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "status": "bad_request", "duration_ms": 0, "attempts": 0}
{"timestamp": "2026-11-13T18:21:48.180574+00:00", "query": "   ", "output": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "status": "bad_request", "duration_ms": 0, "attempts": 0}
{"timestamp": "2026-11-13T18:21:51.519742+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3331, "attempts": 2}
{"timestamp": "2026-11-13T18:21:54.960079+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3431, "attempts": 2}
{"timestamp": "2026-11-13T18:21:58.258844+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3291, "attempts": 2}
{"timestamp": "2026-11-13T18:22:05.345114+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "ModelUnavailable: The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "failed", "duration_ms": 7079, "attempts": 4}
{"timestamp": "2026-11-13T18:22:12.419768+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "ModelUnavailable: The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "failed", "duration_ms": 7063, "attempts": 4}
{"timestamp": "2026-11-13T18:22:19.481857+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "ModelUnavailable: The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "failed", "duration_ms": 7052, "attempts": 4}
```
