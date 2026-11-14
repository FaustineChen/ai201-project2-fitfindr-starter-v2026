#!/usr/bin/env python3
"""
Run the five capstone criteria against a failing fake model, and write the run log.

    python capstone_eval.py --label before     three runs, the default
    python capstone_eval.py --label after      after your fix
    python capstone_eval.py --runs 1           a quick single run

Each run goes through every criterion once, so one invocation produces the
Run 1 / Run 2 / Run 3 columns of the table. The result is ONE file in
results/, with a section per run.

How it works: capstone_stub.py plays the model and fails on command.
generate.py is pointed at it with MODEL_BASE_URL, and the requests go through
serve.py's real /ask route (Flask's test client, no network port needed), so
the real log code and the real retry code are what get tested. The MCP
subprocess inherits the same environment, so it talks to the stub too.

The real GEMINI_API_KEY is never used here: it is replaced with a dummy
before anything is imported.
"""

import os

# ── environment first, before config / generate / serve are imported ─────────
os.environ["GEMINI_API_KEY"] = "stub-key"   # never send the real key to a stub
os.environ["AI201_CACHE"] = "0"             # a cached answer would hide a failure
                                            # (also read by the MCP subprocess)

import argparse
import datetime as dt
import json
import sys
import time

import config

config.CACHE_ENABLED = False
config.REQUESTS_PER_MINUTE = 10**6          # the limiter is for the real API
config.SESSION_REQUEST_BUDGET = 10**6       # one run makes many (fake) calls

import capstone_stub
import serve

QUERY = "vintage graphic tee under $30"
LOG_FIELDS = ("timestamp", "query", "status", "error", "duration_ms", "attempts")
CUT_OFF_LIMIT_S = 22   # criterion 4: the 20 s timeout plus 2 s of overhead
RETRY_LIMIT = 1 + config.TRANSIENT_MAX_RETRIES   # criterion 3: 1 try + 3 retries


# ── one request ───────────────────────────────────────────────────────────────

def _log_lines():
    if not serve.LOG_PATH.exists():
        return []
    return serve.LOG_PATH.read_text(encoding="utf-8").splitlines()


def ask(client, stub, script, body):
    """Send one /ask request while the stub follows `script`. Return everything."""
    stub.set_script(script)
    lines_before = len(_log_lines())
    started = time.perf_counter()
    response = client.post("/ask", json=body)
    elapsed = time.perf_counter() - started
    text = response.get_data(as_text=True)
    return {
        "script": script,
        "body": body,
        "status": response.status_code,
        "text": text,
        "data": response.get_json(silent=True),
        "elapsed_s": round(elapsed, 2),
        "new_log_lines": _log_lines()[lines_before:],
        "stub_calls": [dict(c) for c in stub.calls],
    }


def _data(r):
    return r["data"] if isinstance(r["data"], dict) else {}


def _has_fit_card(r):
    card = _data(r).get("fit_card")
    return isinstance(card, str) and bool(card.strip())


def _log_entry(r):
    """The one log line this request wrote, parsed, or None."""
    if len(r["new_log_lines"]) != 1:
        return None
    try:
        return json.loads(r["new_log_lines"][0])
    except json.JSONDecodeError:
        return None


# ── the five criteria ─────────────────────────────────────────────────────────

def criterion_1(client, stub):
    """A temporary failure recovers: fail 1, 2, 3 times, then answer."""
    trials = []
    for failures in (1, 2, 3):
        r = ask(client, stub, ["503"] * failures + ["ok"], {"query": QUERY})
        r["label"] = f"{failures} failure(s) then ok"
        r["passed"] = (r["status"] == 200 and _data(r).get("error") is None
                       and _has_fit_card(r))
        trials.append(r)
    return trials


def criterion_2_and_3(client, stub):
    """
    Every attempt fails (503, dropped connection, empty reply).

    The same three requests are judged twice: criterion 2 looks at what the
    caller sees, criterion 3 at the attempts field in the log.
    """
    trials = []
    for kind in ("503", "drop", "empty"):
        r = ask(client, stub, [kind], {"query": QUERY})
        r["label"] = f"every attempt: {kind}"
        error = _data(r).get("error")
        r["passed_2"] = (r["status"] != 500 and isinstance(error, str)
                         and bool(error.strip()) and "Traceback" not in r["text"])
        entry = _log_entry(r)
        r["attempts"] = entry.get("attempts") if entry else None
        r["passed_3"] = r["attempts"] == RETRY_LIMIT
        trials.append(r)
    return trials


def criterion_4(client, stub):
    """A hung call is cut off in time; an empty reply is retried, never passed on."""
    hang, empty = [], []
    for i in range(1, 4):
        r = ask(client, stub, ["hang", "ok"], {"query": QUERY})
        r["label"] = f"hang, trial {i}"
        first = r["stub_calls"][0] if r["stub_calls"] else {}
        r["cut_off_s"] = first.get("cut_off_s")
        r["passed"] = (r["cut_off_s"] is not None and r["cut_off_s"] <= CUT_OFF_LIMIT_S
                       and r["status"] != 500 and _has_fit_card(r))
        hang.append(r)
    for i in range(1, 4):
        r = ask(client, stub, ["empty", "ok"], {"query": QUERY})
        r["label"] = f"empty reply, trial {i}"
        r["passed"] = (len(r["stub_calls"]) >= 2 and r["status"] != 500
                       and _has_fit_card(r))
        empty.append(r)
    return hang, empty


def criterion_5(client, stub):
    """A mixed batch of 12 requests: each must leave exactly one valid log line."""
    good = {"query": QUERY}
    batch = (
        [(["ok"], good, "success")] * 4
        + [(["ok"], {}, "missing query"),
           (["ok"], {"query": "   "}, "blank query")]
        + [(["503", "ok"], good, "temporary failure")] * 3
        + [(["503"], good, "persistent failure")] * 3
    )
    requests = []
    for script, body, label in batch:
        r = ask(client, stub, script, body)
        r["label"] = label
        entry = _log_entry(r)
        r["entry"] = entry
        r["valid"] = bool(entry) and all(f in entry for f in LOG_FIELDS)
        requests.append(r)
    passed = len(requests) >= 12 and all(r["valid"] for r in requests)
    return {"requests": requests, "passed": passed}


# ── the report ────────────────────────────────────────────────────────────────

def _count(trials, key="passed"):
    return sum(1 for t in trials if t[key])


def _summary(r):
    data = _data(r)
    item = data.get("selected_item") or {}
    return json.dumps({
        "http_status": r["status"],
        "error": data.get("error"),
        "fit_card": data.get("fit_card"),
        "selected_item": item.get("title"),
    }, ensure_ascii=False, indent=2)


def _trial_block(r, extra=""):
    calls = ", ".join(c["behavior"] for c in r["stub_calls"]) or "(none)"
    out = [
        f"**{r['label']}** — stub script `{r['script']}`",
        "",
        f"- stub received {len(r['stub_calls'])} call(s): {calls}",
        f"- took {r['elapsed_s']}s",
    ]
    if extra:
        out.append(extra)
    out += ["", "Response:", "", "```json", _summary(r), "```", "",
            "Log line(s) written for this request:", "", "```"]
    out += r["new_log_lines"] or ["(none)"]
    out += ["```", ""]
    return out


def write_report(runs, args, stamp):
    path = config.RESULTS_DIR / f"capstone_{stamp}_{args.label}.md"
    n = len(runs)
    headers = " | ".join(f"Run {i}" for i in range(1, n + 1))

    def cells(fn):
        return [fn(run) for run in runs]

    c1 = cells(lambda r: f"{_count(r['c1'])}/3")
    c2 = cells(lambda r: f"{_count(r['c23'], 'passed_2')}/3")
    c3 = cells(lambda r: f"{_count(r['c23'], 'passed_3')}/3")
    c4 = cells(lambda r: f"hang {_count(r['hang'])}/3 · empty {_count(r['empty'])}/3")
    c5 = cells(lambda r: ("PASS " if r["c5"]["passed"] else "FAIL ")
               + f"({sum(1 for x in r['c5']['requests'] if x['valid'])}"
               f"/{len(r['c5']['requests'])} lines valid)")

    ok1 = all(_count(r["c1"]) == 3 for r in runs)
    ok2 = all(_count(r["c23"], "passed_2") == 3 for r in runs)
    ok3 = all(_count(r["c23"], "passed_3") == 3 for r in runs)
    ok4 = all(_count(r["hang"]) == 3 and _count(r["empty"]) == 3 for r in runs)
    ok5 = all(r["c5"]["passed"] for r in runs)
    verdict = lambda ok: "MET" if ok else "MISSED"

    lines = [
        f"# Capstone run log — {args.label}",
        "",
        "- Produced by: `capstone_eval.py::main` (one file, all runs)",
        "- Failures injected by: `capstone_stub.py` (a fake model server)",
        "- Request path: `serve.py::ask` → `agent.py::run_agent` → `generate.py::generate`",
        "- Log lines written by: `serve.py::_log_request`",
        f"- Runs: {n} · when: {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- Request log for this file: `{serve.LOG_PATH.relative_to(config.ROOT)}`",
        "",
        "Cells and verdicts below are computed by the script from the checks in",
        "`capstone_eval.py`. A criterion is MET only if every run meets its target.",
        "",
        f"| Criterion | Target | {headers} | Verdict |",
        f"|---|---|{'|'.join(['---'] * n)}|---|",
        f"| 1. A temporary model failure recovers | 3 of 3 trials | {' | '.join(c1)} | {verdict(ok1)} |",
        f"| 2. A persistent model failure ends with a readable error, in time | 3 of 3 trials | {' | '.join(c2)} | {verdict(ok2)} |",
        f"| 3. Retries never exceed the limit | 3 of 3 trials | {' | '.join(c3)} | {verdict(ok3)} |",
        f"| 4. A hung call or an empty reply is treated as a failure | 3 of 3 trials per case | {' | '.join(c4)} | {verdict(ok4)} |",
        f"| 5. Every request writes one valid log entry, including failures | 3 of 3 batches | {' | '.join(c5)} | {verdict(ok5)} |",
        "",
        "---",
        "",
        "## What actually happened",
        "",
    ]

    for i, run in enumerate(runs, 1):
        lines += [f"# Run {i}", ""]

        lines += ["## Criterion 1 — temporary failure recovers", ""]
        for r in run["c1"]:
            lines += _trial_block(r, f"- **{'PASS' if r['passed'] else 'FAIL'}**")

        lines += ["## Criteria 2 and 3 — every attempt fails", ""]
        for r in run["c23"]:
            extra = (f"- criterion 2: **{'PASS' if r['passed_2'] else 'FAIL'}** "
                     f"(HTTP {r['status']})\n"
                     f"- criterion 3: **{'PASS' if r['passed_3'] else 'FAIL'}** "
                     f"(attempts in log: {r['attempts']}, expected {RETRY_LIMIT})")
            lines += _trial_block(r, extra)

        lines += ["## Criterion 4 — hung call and empty reply", ""]
        for r in run["hang"]:
            extra = (f"- cut off after: {r['cut_off_s']}s (limit {CUT_OFF_LIMIT_S}s)\n"
                     f"- **{'PASS' if r['passed'] else 'FAIL'}**")
            lines += _trial_block(r, extra)
        for r in run["empty"]:
            lines += _trial_block(r, f"- **{'PASS' if r['passed'] else 'FAIL'}**")

        lines += ["## Criterion 5 — one log line per request", ""]
        batch = run["c5"]["requests"]
        lines += [f"Batch of {len(batch)} requests — "
                  f"**{'PASS' if run['c5']['passed'] else 'FAIL'}**", "",
                  "| # | Request | HTTP | Log lines | Valid |", "|---|---|---|---|---|"]
        for k, r in enumerate(batch, 1):
            lines.append(f"| {k} | {r['label']} | {r['status']} | "
                         f"{len(r['new_log_lines'])} | {'yes' if r['valid'] else 'NO'} |")
        lines += ["", "The log lines from this batch:", "", "```"]
        lines += [ln for r in batch for ln in r["new_log_lines"]] or ["(none)"]
        lines += ["```", ""]

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Run the capstone criteria.")
    parser.add_argument("--label", default="run", help="e.g. before / after")
    parser.add_argument("--runs", type=int, default=3, help="how many runs (default 3)")
    args = parser.parse_args()

    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    serve.LOG_PATH = config.RESULTS_DIR / f"capstone_{stamp}_{args.label}_requests.jsonl"
    if serve.LOG_PATH.exists():
        serve.LOG_PATH.unlink()

    stub = capstone_stub.Stub()
    os.environ["MODEL_BASE_URL"] = stub.start()   # generate.py and the MCP subprocess read this
    print(f"Fake model listening at {stub.url}. Real model is never called.\n")

    client = serve.app.test_client()
    runs = []
    try:
        for i in range(1, args.runs + 1):
            print(f"=== Run {i} of {args.runs} ===")
            run = {}

            print("  criterion 1: temporary failures ...")
            run["c1"] = criterion_1(client, stub)
            print(f"    {_count(run['c1'])}/3")

            print("  criteria 2 and 3: every attempt fails ...")
            run["c23"] = criterion_2_and_3(client, stub)
            print(f"    c2 {_count(run['c23'], 'passed_2')}/3 · "
                  f"c3 {_count(run['c23'], 'passed_3')}/3")

            print("  criterion 4: hang and empty reply (about a minute) ...")
            run["hang"], run["empty"] = criterion_4(client, stub)
            print(f"    hang {_count(run['hang'])}/3 · empty {_count(run['empty'])}/3")

            print("  criterion 5: mixed batch of 12 ...")
            run["c5"] = criterion_5(client, stub)
            print(f"    {'PASS' if run['c5']['passed'] else 'FAIL'}\n")

            runs.append(run)
    finally:
        stub.stop()

    path = write_report(runs, args, stamp)
    print(f"Wrote {path.relative_to(config.ROOT)}")
    print("Commit that file and the _requests.jsonl next to it. They are the evidence.")


if __name__ == "__main__":
    main()
