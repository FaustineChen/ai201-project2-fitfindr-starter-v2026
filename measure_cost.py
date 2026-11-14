#!/usr/bin/env python3
"""
Measure what one FitFindr run costs, in tokens and (if you give prices) dollars.

    python measure_cost.py                                  tokens only
    python measure_cost.py --input-price 0.10 --output-price 0.40
                                                            prices are USD per
                                                            1,000,000 tokens —
                                                            copy them from the
                                                            provider's pricing page

It runs the same steps run_agent() runs, with the cache off so every run is a
real model call: parse_query, search_listings, suggest_outfit, create_fit_card.
They are called directly rather than through run_agent() because run_agent()
makes the fit-card call inside the MCP subprocess, which keeps its own token
counter; counting from here would miss that call. The prompts are the same.

⚠️ This calls the real model: two calls per run, twenty for ten runs.
"""

import argparse
import datetime as dt
import sys
import time

import config

config.CACHE_ENABLED = False   # ten runs have to be ten real calls

import generate
import serve
from agent import parse_query
from tools import search_listings, suggest_outfit, create_fit_card
from utils.data_loader import get_example_wardrobe


def one_run(query, write_log=True):
    """One full run. Returns (prompt_tokens, output_tokens, model_calls)."""
    before = generate.token_counts()
    calls_before = generate.call_count()
    retries_before = generate.retry_count()
    started = time.perf_counter()

    parsed = parse_query(query)
    results = search_listings(**parsed)
    if not results:
        raise RuntimeError(f"no listings matched {query!r}; pick a query that matches")
    item = results[0]
    outfit = suggest_outfit(item, get_example_wardrobe())
    card = create_fit_card(outfit, item)

    duration = time.perf_counter() - started
    if write_log:
        # The same function /ask uses, so the line has the same shape. This run
        # did not come through HTTP, which is why measure_cost.py writes it.
        serve._log_request(query, {"fit_card": card, "error": None}, None,
                           duration, generate.retry_count() - retries_before)

    after = generate.token_counts()
    return (after["prompt"] - before["prompt"],
            after["output"] - before["output"],
            generate.call_count() - calls_before)


def main():
    parser = argparse.ArgumentParser(description="Measure the cost of one run.")
    parser.add_argument("--runs", type=int, default=10)
    parser.add_argument("--query", default="vintage graphic tee under $30")
    parser.add_argument("--input-price", type=float, default=None,
                        help="USD per 1,000,000 input tokens")
    parser.add_argument("--output-price", type=float, default=None,
                        help="USD per 1,000,000 output tokens")
    parser.add_argument("--no-log", action="store_true",
                        help="don't append a line to logs/requests.jsonl per run")
    parser.add_argument("--users", type=int, default=100)
    parser.add_argument("--runs-per-user-per-day", type=float, default=1.0)
    args = parser.parse_args()

    rows = []
    for i in range(1, args.runs + 1):
        prompt_t, output_t, calls = one_run(args.query, write_log=not args.no_log)
        rows.append((prompt_t, output_t, calls))
        print(f"run {i:>2}: {prompt_t} input + {output_t} output tokens, {calls} model calls")

    n = len(rows)
    avg_in = sum(r[0] for r in rows) / n
    avg_out = sum(r[1] for r in rows) / n
    avg_calls = sum(r[2] for r in rows) / n

    lines = [
        f"# Cost measurement — {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "- Produced by: `measure_cost.py::main`",
        f"- Model: `{config.MODEL}`, cache off, {n} runs, query: `{args.query}`",
        "- Tokens read from `generate.py::token_counts()` before and after each run",
        "",
        "| Run | Input tokens | Output tokens | Model calls |",
        "|---|---|---|---|",
    ]
    lines += [f"| {i} | {r[0]} | {r[1]} | {r[2]} |" for i, r in enumerate(rows, 1)]
    lines += ["", f"**Average per run:** {avg_in:.1f} input + {avg_out:.1f} output "
                  f"tokens over {avg_calls:.1f} model calls", ""]

    if args.input_price is not None and args.output_price is not None:
        in_cost = avg_in * args.input_price / 1_000_000
        out_cost = avg_out * args.output_price / 1_000_000
        per_run = in_cost + out_cost
        per_day = args.users * args.runs_per_user_per_day * per_run
        lines += [
            f"Prices used: ${args.input_price} per 1M input tokens, "
            f"${args.output_price} per 1M output tokens.",
            "",
            f"- Input:  {avg_in:.1f} × ${args.input_price} ÷ 1,000,000 = ${in_cost:.6f}",
            f"- Output: {avg_out:.1f} × ${args.output_price} ÷ 1,000,000 = ${out_cost:.6f}",
            f"- **Per run: ${per_run:.6f}**",
            f"- {args.users} users × {args.runs_per_user_per_day:g} run/user/day "
            f"× ${per_run:.6f} = **${per_day:.4f} per day** "
            f"(${per_day * 30:.2f} per 30 days)",
            "",
        ]
    else:
        lines += ["No prices given, so no dollar figure. Re-run with "
                  "`--input-price` and `--output-price`.", ""]

    text = "\n".join(lines)
    print("\n" + text)

    config.RESULTS_DIR.mkdir(exist_ok=True)
    path = config.RESULTS_DIR / f"cost_{dt.datetime.now().strftime('%Y-%m-%d_%H%M')}.md"
    path.write_text(text, encoding="utf-8")
    print(f"Wrote {path.relative_to(config.ROOT)}")
    print(generate.usage())


if __name__ == "__main__":
    sys.exit(main())
