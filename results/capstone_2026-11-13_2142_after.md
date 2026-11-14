# Capstone run log — after

- Produced by: `capstone_eval.py::main` (one file, all runs)
- Failures injected by: `capstone_stub.py` (a fake model server)
- Request path: `serve.py::ask` → `agent.py::run_agent` → `generate.py::generate`
- Log lines written by: `serve.py::_log_request`
- Runs: 3 · when: 2026-11-13 21:52
- Request log for this file: `results\capstone_2026-11-13_2142_after_requests.jsonl`

Cells and verdicts below are computed by the script from the checks in
`capstone_eval.py`. A criterion is MET only if every run meets its target.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. A temporary model failure recovers | 3 of 3 trials | 3/3 | 3/3 | 3/3 | MET |
| 2. A persistent model failure ends with a readable error, in time | 3 of 3 trials | 3/3 | 3/3 | 3/3 | MET |
| 3. Retries never exceed the limit | 3 of 3 trials | 3/3 | 3/3 | 3/3 | MET |
| 4. A hung call or an empty reply is treated as a failure | 3 of 3 trials per case | hang 3/3 · empty 3/3 | hang 3/3 · empty 3/3 | hang 3/3 · empty 3/3 | MET |
| 5. Every request writes one valid log entry, including failures | 3 of 3 batches | PASS (12/12 lines valid) | PASS (12/12 lines valid) | PASS (12/12 lines valid) | MET |

---

## What actually happened

# Run 1

## Criterion 1 — temporary failure recovers

**1 failure(s) then ok** — stub script `['503', 'ok']`

- stub received 3 call(s): 503, ok, ok
- took 16.18s
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
{"timestamp": "2026-11-14T02:43:08.283028+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 16170, "attempts": 2}
```

**2 failure(s) then ok** — stub script `['503', '503', 'ok']`

- stub received 4 call(s): 503, 503, ok, ok
- took 6.55s
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
{"timestamp": "2026-11-14T02:43:14.834025+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 6542, "attempts": 3}
```

**3 failure(s) then ok** — stub script `['503', '503', '503', 'ok']`

- stub received 5 call(s): 503, 503, 503, ok, ok
- took 11.72s
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
{"timestamp": "2026-11-14T02:43:26.562729+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 11720, "attempts": 4}
```

## Criteria 2 and 3 — every attempt fails

**every attempt: 503** — stub script `['503']`

- stub received 4 call(s): 503, 503, 503, 503
- took 7.1s
- criterion 2: **PASS** (HTTP 200)
- criterion 3: **PASS** (attempts in log: 4, expected 4)

Response:

```json
{
  "http_status": 200,
  "error": "The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.",
  "fit_card": null,
  "selected_item": "Y2K Baby Tee — Butterfly Print"
}
```

Log line(s) written for this request:

```
{"timestamp": "2026-11-14T02:43:33.664179+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "stopped_early", "duration_ms": 7093, "attempts": 4}
```

**every attempt: drop** — stub script `['drop']`

- stub received 4 call(s): drop, drop, drop, drop
- took 7.08s
- criterion 2: **PASS** (HTTP 200)
- criterion 3: **PASS** (attempts in log: 4, expected 4)

Response:

```json
{
  "http_status": 200,
  "error": "The model kept failing: RemoteProtocolError: Server disconnected without sending a response. (gave up after 3 retries). Try again in a moment.",
  "fit_card": null,
  "selected_item": "Y2K Baby Tee — Butterfly Print"
}
```

Log line(s) written for this request:

```
{"timestamp": "2026-11-14T02:43:40.751291+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "The model kept failing: RemoteProtocolError: Server disconnected without sending a response. (gave up after 3 retries). Try again in a moment.", "status": "stopped_early", "duration_ms": 7076, "attempts": 4}
```

**every attempt: empty** — stub script `['empty']`

- stub received 4 call(s): empty, empty, empty, empty
- took 7.1s
- criterion 2: **PASS** (HTTP 200)
- criterion 3: **PASS** (attempts in log: 4, expected 4)

Response:

```json
{
  "http_status": 200,
  "error": "The model kept failing: EmptyReply: The model returned an empty reply. (gave up after 3 retries). Try again in a moment.",
  "fit_card": null,
  "selected_item": "Y2K Baby Tee — Butterfly Print"
}
```

Log line(s) written for this request:

```
{"timestamp": "2026-11-14T02:43:47.864428+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "The model kept failing: EmptyReply: The model returned an empty reply. (gave up after 3 retries). Try again in a moment.", "status": "stopped_early", "duration_ms": 7100, "attempts": 4}
```

## Criterion 4 — hung call and empty reply

**hang, trial 1** — stub script `['hang', 'ok']`

- stub received 3 call(s): hang, ok, ok
- took 24.76s
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
{"timestamp": "2026-11-14T02:44:12.634550+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 24754, "attempts": 2}
```

**hang, trial 2** — stub script `['hang', 'ok']`

- stub received 3 call(s): hang, ok, ok
- took 26.46s
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
{"timestamp": "2026-11-14T02:44:39.105018+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 26459, "attempts": 2}
```

**hang, trial 3** — stub script `['hang', 'ok']`

- stub received 3 call(s): hang, ok, ok
- took 25.56s
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
{"timestamp": "2026-11-14T02:45:04.678155+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 25560, "attempts": 2}
```

**empty reply, trial 1** — stub script `['empty', 'ok']`

- stub received 3 call(s): empty, ok, ok
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
{"timestamp": "2026-11-14T02:45:09.974934+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 5286, "attempts": 2}
```

**empty reply, trial 2** — stub script `['empty', 'ok']`

- stub received 3 call(s): empty, ok, ok
- took 5.03s
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
{"timestamp": "2026-11-14T02:45:15.010354+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 5024, "attempts": 2}
```

**empty reply, trial 3** — stub script `['empty', 'ok']`

- stub received 3 call(s): empty, ok, ok
- took 5.28s
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
{"timestamp": "2026-11-14T02:45:20.294935+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 5275, "attempts": 2}
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
| 10 | persistent failure | 200 | 1 | yes |
| 11 | persistent failure | 200 | 1 | yes |
| 12 | persistent failure | 200 | 1 | yes |

The log lines from this batch:

```
{"timestamp": "2026-11-14T02:45:24.391630+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 4086, "attempts": 1}
{"timestamp": "2026-11-14T02:45:28.475742+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 4073, "attempts": 1}
{"timestamp": "2026-11-14T02:45:33.022302+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 4535, "attempts": 1}
{"timestamp": "2026-11-14T02:45:37.278304+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 4245, "attempts": 1}
{"timestamp": "2026-11-14T02:45:37.288235+00:00", "query": null, "output": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "status": "bad_request", "duration_ms": 0, "attempts": 0}
{"timestamp": "2026-11-14T02:45:37.298720+00:00", "query": "   ", "output": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "status": "bad_request", "duration_ms": 0, "attempts": 0}
{"timestamp": "2026-11-14T02:45:42.157700+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 4847, "attempts": 2}
{"timestamp": "2026-11-14T02:45:47.562165+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 5393, "attempts": 2}
{"timestamp": "2026-11-14T02:45:52.581212+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 5010, "attempts": 2}
{"timestamp": "2026-11-14T02:45:59.645044+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "stopped_early", "duration_ms": 7054, "attempts": 4}
{"timestamp": "2026-11-14T02:46:06.740385+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "stopped_early", "duration_ms": 7083, "attempts": 4}
{"timestamp": "2026-11-14T02:46:13.833655+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "stopped_early", "duration_ms": 7081, "attempts": 4}
```

# Run 2

## Criterion 1 — temporary failure recovers

**1 failure(s) then ok** — stub script `['503', 'ok']`

- stub received 3 call(s): 503, ok, ok
- took 4.82s
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
{"timestamp": "2026-11-14T02:46:18.662972+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 4814, "attempts": 2}
```

**2 failure(s) then ok** — stub script `['503', '503', 'ok']`

- stub received 4 call(s): 503, 503, ok, ok
- took 6.74s
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
{"timestamp": "2026-11-14T02:46:25.408446+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 6731, "attempts": 3}
```

**3 failure(s) then ok** — stub script `['503', '503', '503', 'ok']`

- stub received 5 call(s): 503, 503, 503, ok, ok
- took 11.15s
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
{"timestamp": "2026-11-14T02:46:36.564657+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 11143, "attempts": 4}
```

## Criteria 2 and 3 — every attempt fails

**every attempt: 503** — stub script `['503']`

- stub received 4 call(s): 503, 503, 503, 503
- took 7.1s
- criterion 2: **PASS** (HTTP 200)
- criterion 3: **PASS** (attempts in log: 4, expected 4)

Response:

```json
{
  "http_status": 200,
  "error": "The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.",
  "fit_card": null,
  "selected_item": "Y2K Baby Tee — Butterfly Print"
}
```

Log line(s) written for this request:

```
{"timestamp": "2026-11-14T02:46:43.674963+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "stopped_early", "duration_ms": 7098, "attempts": 4}
```

**every attempt: drop** — stub script `['drop']`

- stub received 4 call(s): drop, drop, drop, drop
- took 7.1s
- criterion 2: **PASS** (HTTP 200)
- criterion 3: **PASS** (attempts in log: 4, expected 4)

Response:

```json
{
  "http_status": 200,
  "error": "The model kept failing: RemoteProtocolError: Server disconnected without sending a response. (gave up after 3 retries). Try again in a moment.",
  "fit_card": null,
  "selected_item": "Y2K Baby Tee — Butterfly Print"
}
```

Log line(s) written for this request:

```
{"timestamp": "2026-11-14T02:46:50.778194+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "The model kept failing: RemoteProtocolError: Server disconnected without sending a response. (gave up after 3 retries). Try again in a moment.", "status": "stopped_early", "duration_ms": 7092, "attempts": 4}
```

**every attempt: empty** — stub script `['empty']`

- stub received 4 call(s): empty, empty, empty, empty
- took 7.1s
- criterion 2: **PASS** (HTTP 200)
- criterion 3: **PASS** (attempts in log: 4, expected 4)

Response:

```json
{
  "http_status": 200,
  "error": "The model kept failing: EmptyReply: The model returned an empty reply. (gave up after 3 retries). Try again in a moment.",
  "fit_card": null,
  "selected_item": "Y2K Baby Tee — Butterfly Print"
}
```

Log line(s) written for this request:

```
{"timestamp": "2026-11-14T02:46:57.887086+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "The model kept failing: EmptyReply: The model returned an empty reply. (gave up after 3 retries). Try again in a moment.", "status": "stopped_early", "duration_ms": 7092, "attempts": 4}
```

## Criterion 4 — hung call and empty reply

**hang, trial 1** — stub script `['hang', 'ok']`

- stub received 3 call(s): hang, ok, ok
- took 24.7s
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
{"timestamp": "2026-11-14T02:47:22.595954+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 24697, "attempts": 2}
```

**hang, trial 2** — stub script `['hang', 'ok']`

- stub received 3 call(s): hang, ok, ok
- took 24.93s
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
{"timestamp": "2026-11-14T02:47:47.528923+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 24922, "attempts": 2}
```

**hang, trial 3** — stub script `['hang', 'ok']`

- stub received 3 call(s): hang, ok, ok
- took 24.57s
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
{"timestamp": "2026-11-14T02:48:12.107779+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 24562, "attempts": 2}
```

**empty reply, trial 1** — stub script `['empty', 'ok']`

- stub received 3 call(s): empty, ok, ok
- took 5.24s
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
{"timestamp": "2026-11-14T02:48:17.360333+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 5231, "attempts": 2}
```

**empty reply, trial 2** — stub script `['empty', 'ok']`

- stub received 3 call(s): empty, ok, ok
- took 6.54s
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
{"timestamp": "2026-11-14T02:48:23.908667+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 6535, "attempts": 2}
```

**empty reply, trial 3** — stub script `['empty', 'ok']`

- stub received 3 call(s): empty, ok, ok
- took 4.77s
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
{"timestamp": "2026-11-14T02:48:28.685740+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 4763, "attempts": 2}
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
| 10 | persistent failure | 200 | 1 | yes |
| 11 | persistent failure | 200 | 1 | yes |
| 12 | persistent failure | 200 | 1 | yes |

The log lines from this batch:

```
{"timestamp": "2026-11-14T02:48:32.812257+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 4114, "attempts": 1}
{"timestamp": "2026-11-14T02:48:36.978823+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 4145, "attempts": 1}
{"timestamp": "2026-11-14T02:48:40.630739+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3638, "attempts": 1}
{"timestamp": "2026-11-14T02:48:44.572617+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3929, "attempts": 1}
{"timestamp": "2026-11-14T02:48:44.590746+00:00", "query": null, "output": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "status": "bad_request", "duration_ms": 0, "attempts": 0}
{"timestamp": "2026-11-14T02:48:44.606130+00:00", "query": "   ", "output": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "status": "bad_request", "duration_ms": 0, "attempts": 0}
{"timestamp": "2026-11-14T02:48:50.308965+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 5688, "attempts": 2}
{"timestamp": "2026-11-14T02:48:55.318754+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 4997, "attempts": 2}
{"timestamp": "2026-11-14T02:49:00.085746+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 4753, "attempts": 2}
{"timestamp": "2026-11-14T02:49:07.184019+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "stopped_early", "duration_ms": 7084, "attempts": 4}
{"timestamp": "2026-11-14T02:49:14.326876+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "stopped_early", "duration_ms": 7128, "attempts": 4}
{"timestamp": "2026-11-14T02:49:21.395745+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "stopped_early", "duration_ms": 7055, "attempts": 4}
```

# Run 3

## Criterion 1 — temporary failure recovers

**1 failure(s) then ok** — stub script `['503', 'ok']`

- stub received 3 call(s): 503, ok, ok
- took 5.47s
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
{"timestamp": "2026-11-14T02:49:26.879783+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 5471, "attempts": 2}
```

**2 failure(s) then ok** — stub script `['503', '503', 'ok']`

- stub received 4 call(s): 503, 503, ok, ok
- took 6.74s
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
{"timestamp": "2026-11-14T02:49:33.629733+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 6738, "attempts": 3}
```

**3 failure(s) then ok** — stub script `['503', '503', '503', 'ok']`

- stub received 5 call(s): 503, 503, 503, ok, ok
- took 10.78s
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
{"timestamp": "2026-11-14T02:49:44.417890+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 10773, "attempts": 4}
```

## Criteria 2 and 3 — every attempt fails

**every attempt: 503** — stub script `['503']`

- stub received 4 call(s): 503, 503, 503, 503
- took 7.06s
- criterion 2: **PASS** (HTTP 200)
- criterion 3: **PASS** (attempts in log: 4, expected 4)

Response:

```json
{
  "http_status": 200,
  "error": "The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.",
  "fit_card": null,
  "selected_item": "Y2K Baby Tee — Butterfly Print"
}
```

Log line(s) written for this request:

```
{"timestamp": "2026-11-14T02:49:51.490195+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "stopped_early", "duration_ms": 7058, "attempts": 4}
```

**every attempt: drop** — stub script `['drop']`

- stub received 4 call(s): drop, drop, drop, drop
- took 7.07s
- criterion 2: **PASS** (HTTP 200)
- criterion 3: **PASS** (attempts in log: 4, expected 4)

Response:

```json
{
  "http_status": 200,
  "error": "The model kept failing: RemoteProtocolError: Server disconnected without sending a response. (gave up after 3 retries). Try again in a moment.",
  "fit_card": null,
  "selected_item": "Y2K Baby Tee — Butterfly Print"
}
```

Log line(s) written for this request:

```
{"timestamp": "2026-11-14T02:49:58.569664+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "The model kept failing: RemoteProtocolError: Server disconnected without sending a response. (gave up after 3 retries). Try again in a moment.", "status": "stopped_early", "duration_ms": 7061, "attempts": 4}
```

**every attempt: empty** — stub script `['empty']`

- stub received 4 call(s): empty, empty, empty, empty
- took 7.07s
- criterion 2: **PASS** (HTTP 200)
- criterion 3: **PASS** (attempts in log: 4, expected 4)

Response:

```json
{
  "http_status": 200,
  "error": "The model kept failing: EmptyReply: The model returned an empty reply. (gave up after 3 retries). Try again in a moment.",
  "fit_card": null,
  "selected_item": "Y2K Baby Tee — Butterfly Print"
}
```

Log line(s) written for this request:

```
{"timestamp": "2026-11-14T02:50:05.647487+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "The model kept failing: EmptyReply: The model returned an empty reply. (gave up after 3 retries). Try again in a moment.", "status": "stopped_early", "duration_ms": 7063, "attempts": 4}
```

## Criterion 4 — hung call and empty reply

**hang, trial 1** — stub script `['hang', 'ok']`

- stub received 3 call(s): hang, ok, ok
- took 24.7s
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
{"timestamp": "2026-11-14T02:50:30.355301+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 24692, "attempts": 2}
```

**hang, trial 2** — stub script `['hang', 'ok']`

- stub received 3 call(s): hang, ok, ok
- took 24.8s
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
{"timestamp": "2026-11-14T02:50:55.162316+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 24794, "attempts": 2}
```

**hang, trial 3** — stub script `['hang', 'ok']`

- stub received 3 call(s): hang, ok, ok
- took 24.93s
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
{"timestamp": "2026-11-14T02:51:20.107821+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 24929, "attempts": 2}
```

**empty reply, trial 1** — stub script `['empty', 'ok']`

- stub received 3 call(s): empty, ok, ok
- took 5.43s
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
{"timestamp": "2026-11-14T02:51:25.548283+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 5425, "attempts": 2}
```

**empty reply, trial 2** — stub script `['empty', 'ok']`

- stub received 3 call(s): empty, ok, ok
- took 4.75s
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
{"timestamp": "2026-11-14T02:51:30.310822+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 4746, "attempts": 2}
```

**empty reply, trial 3** — stub script `['empty', 'ok']`

- stub received 3 call(s): empty, ok, ok
- took 4.89s
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
{"timestamp": "2026-11-14T02:51:35.208909+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 4885, "attempts": 2}
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
| 10 | persistent failure | 200 | 1 | yes |
| 11 | persistent failure | 200 | 1 | yes |
| 12 | persistent failure | 200 | 1 | yes |

The log lines from this batch:

```
{"timestamp": "2026-11-14T02:51:39.199003+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3976, "attempts": 1}
{"timestamp": "2026-11-14T02:51:43.250896+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 4039, "attempts": 1}
{"timestamp": "2026-11-14T02:51:47.635638+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 4372, "attempts": 1}
{"timestamp": "2026-11-14T02:51:51.466961+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 3815, "attempts": 1}
{"timestamp": "2026-11-14T02:51:51.481969+00:00", "query": null, "output": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "status": "bad_request", "duration_ms": 0, "attempts": 0}
{"timestamp": "2026-11-14T02:51:51.500683+00:00", "query": "   ", "output": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "status": "bad_request", "duration_ms": 0, "attempts": 0}
{"timestamp": "2026-11-14T02:51:56.346819+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 4828, "attempts": 2}
{"timestamp": "2026-11-14T02:52:01.235501+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 4873, "attempts": 2}
{"timestamp": "2026-11-14T02:52:06.246062+00:00", "query": "vintage graphic tee under $30", "output": "Just scored this tee for $12.00 on Depop and it pairs perfectly with my everyday jeans. Total thrift win.", "error": null, "status": "ok", "duration_ms": 4995, "attempts": 2}
{"timestamp": "2026-11-14T02:52:13.330799+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "stopped_early", "duration_ms": 7070, "attempts": 4}
{"timestamp": "2026-11-14T02:52:20.521515+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "stopped_early", "duration_ms": 7036, "attempts": 4}
{"timestamp": "2026-11-14T02:52:27.612427+00:00", "query": "vintage graphic tee under $30", "output": null, "error": "The model kept failing: ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'status': 'UNAVAILABLE', 'message': 'The model is overloaded. Please try again later.'}} (gave up after 3 retries). Try again in a moment.", "status": "stopped_early", "duration_ms": 7076, "attempts": 4}
```
