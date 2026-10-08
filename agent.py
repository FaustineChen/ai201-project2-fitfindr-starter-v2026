"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls all three tools no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. **That branch is the graded part of this unit.**

Build and test your three tools in `tools.py` first. Then come here.

    python agent.py          runs both example paths below
"""

import config
from trace import step, start_trace, get_trace, check_iterations
from tools import search_listings, suggest_outfit, create_fit_card
from generate import ModelUnavailable
import re
from mcp_client import call_tool


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.

    The session is the single source of truth for a run. Every tool result goes
    in here, and the next tool reads it back out.

    You could pass values straight from one call to the next. It would work,
    and you would not be able to test it — you can't print a variable you have
    already overwritten. Going through the session is what makes the state
    visible, and unit 4 has you write a criterion about exactly that.

    Add fields if you need them.
    """
    return {
        "query": query,              # what the user typed
        "parsed": {},                # description / size / max_price you pulled out of it
        "search_results": [],        # everything search_listings returned
        "selected_item": None,       # the one you chose — goes into suggest_outfit
        "wardrobe": wardrobe,        # the user's wardrobe
        "outfit_suggestion": None,   # what suggest_outfit returned
        "fit_card": None,            # what create_fit_card returned
        "error": None,               # set when the run ended early
    }


# ── planning loop ─────────────────────────────────────────────────────────────
SIZE_WORDS = {
    "small": "S",
    "medium": "M",
    "large": "L",
    "extra large": "XL",
    "x large": "XL",
}

def parse_query(query: str) -> dict:
    """Pull description, size, and max_price out of a plain-language query."""
    text = query
    max_price = None
    size = None

    # price: "under $30", "below 30", or a bare "$30"
    m = (re.search(r"(?:under|below|less than|max|up to)\s*\$?\s*(\d+(?:\.\d+)?)", text, re.I)
         or re.search(r"\$\s*(\d+(?:\.\d+)?)", text))
    if m:
        max_price = float(m.group(1))
        text = text.replace(m.group(0), " ")

    # size: "one size" first, then "size M", "in size 8", "size W30"
    m = re.search(r"\bone[\s-]size\b", text, re.I)
    if m:
        size = "one size"
        text = text.replace(m.group(0), " ")
    else:
        # m = re.search(r"\b(?:in\s+)?size\s+([A-Za-z0-9/]+)", text, re.I)
        # if m:
        #     size = m.group(1)
        #     text = text.replace(m.group(0), " ")

        m = re.search(
            r"\b(?:in\s+)?size\s+"
            r"(extra[\s-]large|x[\s-]large|small|medium|large|[A-Za-z0-9/]+)\b",
            text, re.I,
        )
        if m:
            raw = m.group(1)
            key = re.sub(r"[\s-]+", " ", raw.lower())
            size = SIZE_WORDS.get(key, raw)  # map to S/M/L/XL
            text = text.replace(m.group(0), " ")

    # drop filler words, keep the rest as the description
    text = re.sub(r"\b(looking for|i want|i need|find me|a|an|the|in|for)\b", " ", text, flags=re.I)
    description = " ".join(text.split())

    return {"description": description, "size": size, "max_price": max_price}

def _no_results_message(parsed: dict) -> str:
    tips = ["use broader keywords (e.g. 'jacket' instead of a specific style)"]
    if parsed["size"]:
        tips.append(f"try a different size than '{parsed['size']}'")
    if parsed["max_price"] is not None:
        tips.append(f"raise your price limit above ${parsed['max_price']:.0f}")
    return "No listings matched. You could:\n" + "\n".join(f"  - {t}" for t in tips)

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Run the loop once and return the finished session.

    Args:
        query:    what the user asked for, in plain language
                  (e.g. "vintage graphic tee under $30, size M").
        wardrobe: a wardrobe dict — get_example_wardrobe() or
                  get_empty_wardrobe() from utils/data_loader.py.

    Returns:
        The session dict. **Check session["error"] first** — if it isn't None,
        the run ended early and the later fields will still be None.

    ─────────────────────────────────────────────────────────────────────────
    TODO — build this, following the branch rule you wrote in Milestone 2.

      1. Start a session with new_session().

      2. Count the times round the loop, and call trace.check_iterations(count)
         on each one before you go again. It raises when the count passes
         MAX_ITERATIONS in config.py — see trace.py.

      3. Parse the query into a description, a size, and a max_price. Regex,
         string splitting, or asking the model are all fine — say which you
         chose in your README. Put the result in session["parsed"].

      4. Call search_listings() with what you parsed.
         Put the results in session["search_results"].

         ⚠️ THIS IS THE BRANCH. If nothing came back:
              - put a message in session["error"] saying what the user could
                change — "No results" is not that message
              - return the session
              - do NOT call suggest_outfit with nothing

      5. Choose an item — the first result is fine. Put it in
         session["selected_item"].

      6. Call suggest_outfit() with the selected item and the wardrobe.
         Put the result in session["outfit_suggestion"].

      7. Call create_fit_card() with the outfit and the item.
         Put the result in session["fit_card"].

      8. Return the session.

    ─────────────────────────────────────────────────────────────────────────
    IN UNIT 4 you come back and add two things:

      • Trace calls. One per step. `trace.step("search_listings", inputs=...,
        returned=...)` — see trace.py. Your README needs the output.

      • A handler for ModelUnavailable, so a bad key produces a message rather
        than a stack trace. The import is already at the top of this file.
    """
    start_trace()

    session = new_session(query, wardrobe)
    state = "parse"
    count = 0

    while state != "done":
        count += 1
        check_iterations(count)

        if state == "parse":
            session["parsed"] = parse_query(session["query"])
            step("parse_query",
                 inputs={"query": session["query"]},
                 returned=session["parsed"])
            state = "search"
            
        elif state == "search":
            session["search_results"] = search_listings(**session["parsed"])
            step("search_listings",
                 inputs=session["parsed"],
                 returned=session["search_results"])
            
            if not session["search_results"]:          # THE BRANCH
                session["error"] = _no_results_message(session["parsed"])
                step("branch: no results",
                     note="stopping before suggest_outfit / create_fit_card")
                
                get_trace()
                return session
            state = "select"

        elif state == "select":
            session["selected_item"] = session["search_results"][0]
            step("select_item",
                 inputs=f"{len(session['search_results'])} results",
                 returned=session["selected_item"],
                 note="results found, picking the first")
            
            state = "outfit"

        elif state == "outfit":
            session["outfit_suggestion"] = suggest_outfit(
                session["selected_item"], session["wardrobe"]
            )
            step("suggest_outfit",
                 inputs={"item": session["selected_item"].get("title"),
                         "wardrobe_items": len(session["wardrobe"].get("items", []))
                         if isinstance(session["wardrobe"], dict) else "wrong data type of wardrobe, need to be dict"},
                 returned=session["outfit_suggestion"])
            
            state = "card"

        elif state == "card":
            # session["fit_card"] = create_fit_card(
            #     session["outfit_suggestion"], session["selected_item"]
            # )

            session["fit_card"] = call_tool(
                "create_fit_card",{
                "outfit": session["outfit_suggestion"],
                "new_item": session["selected_item"]
            })
            step("create_fit_card (via MCP)",
                 inputs=(f"item: {session['selected_item'].get('title')} "
                         f"(${session['selected_item'].get('price')}, "
                         f"{session['selected_item'].get('platform')}) | "
                         f"outfit: {str(session['outfit_suggestion'])[:60]}…"),
                 returned=session["fit_card"])
            
            state = "done"

    get_trace()

    return session


# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(f"  fit_card is {session['fit_card']!r} — it should still be None here")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))

    print("\n=== A query it can't ===")
    _show(run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    ))

    print(
        "\nThe second one should stop before the fit card. If both paths look "
        "the same,\nthe branch isn't doing anything yet."
    )
