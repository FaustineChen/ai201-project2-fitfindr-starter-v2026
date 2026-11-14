# Capstone run log — before

- Produced by: `capstone_eval.py::main` (one file, all runs)
- Failures injected by: `capstone_stub.py` (a fake model server)
- Request path: `serve.py::ask` → `agent.py::run_agent` → `generate.py::generate`
- Log lines written by: `serve.py::_log_request`
- Runs: 3 · when: 2026-11-13 13:52
- Request log for this file: `results\capstone_2026-11-13_1344_before_requests.jsonl`

Cells and verdicts below are computed by the script from the checks in
`capstone_eval.py`. A criterion is MET only if every run meets its target.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. A temporary model failure recovers | 3 of 3 trials | 3/3 | 3/3 | 3/3 | MET |
| 2. A persistent model failure ends with a readable error, in time | 3 of 3 trials | 0/3 | 0/3 | 0/3 | MISSED |
| 3. Retries never exceed the limit | 3 of 3 trials | 3/3 | 3/3 | 3/3 | MET |
| 4. A hung call or an empty reply is treated as a failure | 3 of 3 trials per case | hang 3/3 · empty 3/3 | hang 3/3 · empty 3/3 | hang 3/3 · empty 3/3 | MET |
| 5. Every request writes one valid log entry, including failures | 3 of 3 batches | PASS (12/12 lines valid) | PASS (12/12 lines valid) | PASS (12/12 lines valid) | MET |

---

## What actually happened

# Run 1

## Criterion 1 — temporary failure recovers

**1 failure(s) then ok** — stub script `['503', 'ok']`

- stub received 3 call(s): 503, ok, ok
- took 5.68s
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
{"timestamp": "2026-11-13T18:44:30.834020+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 5676, "attempts": 2}
```

**2 failure(s) then ok** — stub script `['503', '503', 'ok']`

- stub received 4 call(s): 503, 503, ok, ok
- took 5.37s
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
{"timestamp": "2026-11-13T18:44:36.209925+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 5364, "attempts": 3}
```

**3 failure(s) then ok** — stub script `['503', '503', '503', 'ok']`

- stub received 5 call(s): 503, 503, 503, ok, ok
- took 9.25s
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
{"timestamp": "2026-11-13T18:44:45.471742+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 9250, "attempts": 4}
```

## Criteria 2 and 3 — every attempt fails

**every attempt: 503** — stub script `['503']`

- stub received 4 call(s): 503, 503, 503, 503
- took 7.07s
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
{"timestamp": "2026-11-13T18:44:52.552621+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "ModelUnavailable: The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "failed", "duration_ms": 7070, "attempts": 4}
```

**every attempt: drop** — stub script `['drop']`

- stub received 4 call(s): drop, drop, drop, drop
- took 7.11s
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
{"timestamp": "2026-11-13T18:44:59.671483+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "ModelUnavailable: The model kept failing: RemoteProtocolError: Server disconnected without sending a response. (gave up after 3 retries). Try again in a moment.", "status": "failed", "duration_ms": 7110, "attempts": 4}
```

**every attempt: empty** — stub script `['empty']`

- stub received 4 call(s): empty, empty, empty, empty
- took 7.11s
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
{"timestamp": "2026-11-13T18:45:06.785613+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "ModelUnavailable: The model kept failing: EmptyReply: The model returned an empty reply. (gave up after 3 retries). Try again in a moment.", "status": "failed", "duration_ms": 7107, "attempts": 4}
```

## Criterion 4 — hung call and empty reply

**hang, trial 1** — stub script `['hang', 'ok']`

- stub received 3 call(s): hang, ok, ok
- took 23.29s
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
{"timestamp": "2026-11-13T18:45:30.081787+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 23284, "attempts": 2}
```

**hang, trial 2** — stub script `['hang', 'ok']`

- stub received 3 call(s): hang, ok, ok
- took 23.21s
- cut off after: 20.02s (limit 22s)
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
{"timestamp": "2026-11-13T18:45:53.297502+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 23202, "attempts": 2}
```

**hang, trial 3** — stub script `['hang', 'ok']`

- stub received 3 call(s): hang, ok, ok
- took 23.25s
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
{"timestamp": "2026-11-13T18:46:16.549310+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 23241, "attempts": 2}
```

**empty reply, trial 1** — stub script `['empty', 'ok']`

- stub received 3 call(s): empty, ok, ok
- took 3.25s
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
{"timestamp": "2026-11-13T18:46:19.802865+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3241, "attempts": 2}
```

**empty reply, trial 2** — stub script `['empty', 'ok']`

- stub received 3 call(s): empty, ok, ok
- took 3.23s
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
{"timestamp": "2026-11-13T18:46:23.040136+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3224, "attempts": 2}
```

**empty reply, trial 3** — stub script `['empty', 'ok']`

- stub received 3 call(s): empty, ok, ok
- took 3.25s
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
{"timestamp": "2026-11-13T18:46:26.293969+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3243, "attempts": 2}
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
{"timestamp": "2026-11-13T18:46:28.553245+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 2247, "attempts": 1}
{"timestamp": "2026-11-13T18:46:30.799910+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 2235, "attempts": 1}
{"timestamp": "2026-11-13T18:46:33.073004+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 2261, "attempts": 1}
{"timestamp": "2026-11-13T18:46:35.357222+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 2274, "attempts": 1}
{"timestamp": "2026-11-13T18:46:35.367038+00:00", "query": null, "output": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "status": "bad_request", "duration_ms": 0, "attempts": 0}
{"timestamp": "2026-11-13T18:46:35.376695+00:00", "query": "   ", "output": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "status": "bad_request", "duration_ms": 0, "attempts": 0}
{"timestamp": "2026-11-13T18:46:38.654467+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3268, "attempts": 2}
{"timestamp": "2026-11-13T18:46:41.938191+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3271, "attempts": 2}
{"timestamp": "2026-11-13T18:46:45.208942+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3260, "attempts": 2}
{"timestamp": "2026-11-13T18:46:52.297788+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "ModelUnavailable: The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "failed", "duration_ms": 7078, "attempts": 4}
{"timestamp": "2026-11-13T18:46:59.392211+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "ModelUnavailable: The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "failed", "duration_ms": 7080, "attempts": 4}
{"timestamp": "2026-11-13T18:47:06.474391+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "ModelUnavailable: The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "failed", "duration_ms": 7069, "attempts": 4}
```

# Run 2

## Criterion 1 — temporary failure recovers

**1 failure(s) then ok** — stub script `['503', 'ok']`

- stub received 3 call(s): 503, ok, ok
- took 3.48s
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
{"timestamp": "2026-11-13T18:47:09.963571+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3477, "attempts": 2}
```

**2 failure(s) then ok** — stub script `['503', '503', 'ok']`

- stub received 4 call(s): 503, 503, ok, ok
- took 5.29s
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
{"timestamp": "2026-11-13T18:47:15.262472+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 5287, "attempts": 3}
```

**3 failure(s) then ok** — stub script `['503', '503', '503', 'ok']`

- stub received 5 call(s): 503, 503, 503, ok, ok
- took 9.25s
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
{"timestamp": "2026-11-13T18:47:24.518088+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 9245, "attempts": 4}
```

## Criteria 2 and 3 — every attempt fails

**every attempt: 503** — stub script `['503']`

- stub received 4 call(s): 503, 503, 503, 503
- took 7.11s
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
{"timestamp": "2026-11-13T18:47:31.635600+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "ModelUnavailable: The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "failed", "duration_ms": 7106, "attempts": 4}
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
{"timestamp": "2026-11-13T18:47:38.735491+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "ModelUnavailable: The model kept failing: RemoteProtocolError: Server disconnected without sending a response. (gave up after 3 retries). Try again in a moment.", "status": "failed", "duration_ms": 7089, "attempts": 4}
```

**every attempt: empty** — stub script `['empty']`

- stub received 4 call(s): empty, empty, empty, empty
- took 7.09s
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
{"timestamp": "2026-11-13T18:47:45.830628+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "ModelUnavailable: The model kept failing: EmptyReply: The model returned an empty reply. (gave up after 3 retries). Try again in a moment.", "status": "failed", "duration_ms": 7085, "attempts": 4}
```

## Criterion 4 — hung call and empty reply

**hang, trial 1** — stub script `['hang', 'ok']`

- stub received 3 call(s): hang, ok, ok
- took 23.31s
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
{"timestamp": "2026-11-13T18:48:09.153613+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 23311, "attempts": 2}
```

**hang, trial 2** — stub script `['hang', 'ok']`

- stub received 3 call(s): hang, ok, ok
- took 23.29s
- cut off after: 20.02s (limit 22s)
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
{"timestamp": "2026-11-13T18:48:32.448564+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 23283, "attempts": 2}
```

**hang, trial 3** — stub script `['hang', 'ok']`

- stub received 3 call(s): hang, ok, ok
- took 23.25s
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
{"timestamp": "2026-11-13T18:48:55.709372+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 23249, "attempts": 2}
```

**empty reply, trial 1** — stub script `['empty', 'ok']`

- stub received 3 call(s): empty, ok, ok
- took 3.28s
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
{"timestamp": "2026-11-13T18:48:58.993614+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3273, "attempts": 2}
```

**empty reply, trial 2** — stub script `['empty', 'ok']`

- stub received 3 call(s): empty, ok, ok
- took 3.32s
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
{"timestamp": "2026-11-13T18:49:02.323364+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3319, "attempts": 2}
```

**empty reply, trial 3** — stub script `['empty', 'ok']`

- stub received 3 call(s): empty, ok, ok
- took 3.29s
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
{"timestamp": "2026-11-13T18:49:05.619168+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3284, "attempts": 2}
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
{"timestamp": "2026-11-13T18:49:07.819679+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 2187, "attempts": 1}
{"timestamp": "2026-11-13T18:49:10.060027+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 2228, "attempts": 1}
{"timestamp": "2026-11-13T18:49:12.291684+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 2219, "attempts": 1}
{"timestamp": "2026-11-13T18:49:14.594412+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 2290, "attempts": 1}
{"timestamp": "2026-11-13T18:49:14.606490+00:00", "query": null, "output": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "status": "bad_request", "duration_ms": 0, "attempts": 0}
{"timestamp": "2026-11-13T18:49:14.621616+00:00", "query": "   ", "output": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "status": "bad_request", "duration_ms": 0, "attempts": 0}
{"timestamp": "2026-11-13T18:49:17.851497+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3218, "attempts": 2}
{"timestamp": "2026-11-13T18:49:21.094476+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3231, "attempts": 2}
{"timestamp": "2026-11-13T18:49:24.385189+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3278, "attempts": 2}
{"timestamp": "2026-11-13T18:49:31.462679+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "ModelUnavailable: The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "failed", "duration_ms": 7065, "attempts": 4}
{"timestamp": "2026-11-13T18:49:38.549588+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "ModelUnavailable: The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "failed", "duration_ms": 7073, "attempts": 4}
{"timestamp": "2026-11-13T18:49:45.659501+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "ModelUnavailable: The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "failed", "duration_ms": 7099, "attempts": 4}
```

# Run 3

## Criterion 1 — temporary failure recovers

**1 failure(s) then ok** — stub script `['503', 'ok']`

- stub received 3 call(s): 503, ok, ok
- took 3.54s
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
{"timestamp": "2026-11-13T18:49:49.211633+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3537, "attempts": 2}
```

**2 failure(s) then ok** — stub script `['503', '503', 'ok']`

- stub received 4 call(s): 503, 503, ok, ok
- took 5.21s
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
{"timestamp": "2026-11-13T18:49:54.429557+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 5207, "attempts": 3}
```

**3 failure(s) then ok** — stub script `['503', '503', '503', 'ok']`

- stub received 5 call(s): 503, 503, 503, ok, ok
- took 9.26s
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
{"timestamp": "2026-11-13T18:50:03.702096+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 9262, "attempts": 4}
```

## Criteria 2 and 3 — every attempt fails

**every attempt: 503** — stub script `['503']`

- stub received 4 call(s): 503, 503, 503, 503
- took 7.08s
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
{"timestamp": "2026-11-13T18:50:10.789440+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "ModelUnavailable: The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "failed", "duration_ms": 7078, "attempts": 4}
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
{"timestamp": "2026-11-13T18:50:17.889295+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "ModelUnavailable: The model kept failing: RemoteProtocolError: Server disconnected without sending a response. (gave up after 3 retries). Try again in a moment.", "status": "failed", "duration_ms": 7086, "attempts": 4}
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
{"timestamp": "2026-11-13T18:50:24.976192+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "ModelUnavailable: The model kept failing: EmptyReply: The model returned an empty reply. (gave up after 3 retries). Try again in a moment.", "status": "failed", "duration_ms": 7075, "attempts": 4}
```

## Criterion 4 — hung call and empty reply

**hang, trial 1** — stub script `['hang', 'ok']`

- stub received 3 call(s): hang, ok, ok
- took 23.21s
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
{"timestamp": "2026-11-13T18:50:48.196213+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 23206, "attempts": 2}
```

**hang, trial 2** — stub script `['hang', 'ok']`

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
{"timestamp": "2026-11-13T18:51:11.481203+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 23275, "attempts": 2}
```

**hang, trial 3** — stub script `['hang', 'ok']`

- stub received 3 call(s): hang, ok, ok
- took 23.27s
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
{"timestamp": "2026-11-13T18:51:34.763092+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 23272, "attempts": 2}
```

**empty reply, trial 1** — stub script `['empty', 'ok']`

- stub received 3 call(s): empty, ok, ok
- took 3.26s
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
{"timestamp": "2026-11-13T18:51:38.036497+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3262, "attempts": 2}
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
{"timestamp": "2026-11-13T18:51:41.311224+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3264, "attempts": 2}
```

**empty reply, trial 3** — stub script `['empty', 'ok']`

- stub received 3 call(s): empty, ok, ok
- took 3.38s
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
{"timestamp": "2026-11-13T18:51:44.694772+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3374, "attempts": 2}
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
{"timestamp": "2026-11-13T18:51:46.915000+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 2212, "attempts": 1}
{"timestamp": "2026-11-13T18:51:49.115122+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 2189, "attempts": 1}
{"timestamp": "2026-11-13T18:51:51.363897+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 2239, "attempts": 1}
{"timestamp": "2026-11-13T18:51:53.757392+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 2383, "attempts": 1}
{"timestamp": "2026-11-13T18:51:53.769726+00:00", "query": null, "output": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "status": "bad_request", "duration_ms": 0, "attempts": 0}
{"timestamp": "2026-11-13T18:51:53.783876+00:00", "query": "   ", "output": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "status": "bad_request", "duration_ms": 0, "attempts": 0}
{"timestamp": "2026-11-13T18:51:57.083333+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3287, "attempts": 2}
{"timestamp": "2026-11-13T18:52:00.386475+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3292, "attempts": 2}
{"timestamp": "2026-11-13T18:52:03.639834+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3242, "attempts": 2}
{"timestamp": "2026-11-13T18:52:10.725738+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "ModelUnavailable: The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "failed", "duration_ms": 7073, "attempts": 4}
{"timestamp": "2026-11-13T18:52:17.767406+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "ModelUnavailable: The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "failed", "duration_ms": 7028, "attempts": 4}
{"timestamp": "2026-11-13T18:52:24.914363+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "ModelUnavailable: The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "failed", "duration_ms": 7135, "attempts": 4}
```
