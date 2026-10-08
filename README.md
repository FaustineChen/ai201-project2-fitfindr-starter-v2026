# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

A user describes a secondhand clothing item in plain language, such as "vintage graphic tee under $30" or "platform sneakers size 8", including constraints like price, size, style, or color.
The agent searches the resale listings for items that match those constraints and returns the best matches, then suggests one or two outfits that pair it with pieces from the user's wardrobe.
It finishes with a short social-post-style caption (a "fit card") about the find.
If nothing in the wordrobe data matches (for example, "designer ballgown size XXS under $5"), it stops and tells the user what to change, such as the keywords, size, or price limit, instead of returning unrelated results.
---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:**  Filters listings by max price (inclusive) and by size (whole-token, case-insensitive match, so "M" matches "S/M" but "s" does not match "us 9"). Scores the rest by the number of description keywords found in `title`, `description`, and `style_tags`, drops zero scores, and ranks by score with ties broken by lower price. Returns at most `config.SEARCH_RESULT_LIMIT` results. It does not call the LLM.
- **Inputs:** `description` (str), `size` (str | None), `max_price` (float | None)
- **Returns:** A list of listing dicts, best match first. Each dict has `id`, `title`, `description`, `category`, `style_tags` (list), `size`, `condition`, `price` (float), `colors` (list), `brand` (str or None), `platform`.
- **When it has nothing:** Returns an empty list (not None, no exception). The loop checks for this, sets `session["error"]` and stops before `suggest_outfit`

### `suggest_outfit`

- **What it does:** Calls the LLM with the selected listing and the user's wardrobe, and asks for one or two outfits that pair the new item with wardrobe pieces. If the wardrobe is empty, or has no pieces that pair with the item, it asks for general styling advice for the item instead.
- **Inputs:** `new_item` (dict, one listing as returned by `search_listings`: `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, `platform`), `wardrobe` (dict with an `items` key holding a list of owned pieces, each with `id`, `name`, `category`, `colors`, `style_tags`, and optional `notes`; may be empty)
- **Returns:** A non-empty string with one or two outfit suggestions.
- **When it has nothing:** With an empty wardrobe it returns general styling advice(never `""`, and no exception is raised for empty input). If the model returns an empty response twice in a row, it raises `RuntimeError` rather than returning `""`.

### `create_fit_card`

- **What it does:** Calls the LLM to turn the outfit suggestion into a short social-post-style caption about the find, mentioning the item, price, and platform once each, with a specific vibe.
- **Inputs:** `outfit` (str, the output of `suggest_outfit` for this same item), `new_item` (dict, the same selected listing passed to `suggest_outfit`)
- **Returns:** A two-to-four sentence caption (str).
- **When it has nothing:** If `outfit` is empty or whitespace, it returns a descriptive message (e.g. "No outfit suggestion available."), no exception.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If `search_listings` returns an empty list, put a message in `session["error"]` that names what the user could change (keywords, size, price limit) and return the session without calling `suggest_outfit` or `create_fit_card`. Otherwise, take the first result as `selected_item` and go to `suggest_outfit`, then `create_fit_card`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regex (`agent.py::parse_query`). It extracts a price ceiling from phrases like "under $30" or a bare "$30", a size from "size <token>", and treats the remaining text, minus filler words, as the description. No model call.

**What moves through the session:** `query` → `parsed` (description, size, max_price) → `search_results` → `selected_item` → `outfit_suggestion` → `fit_card`. `error` is set only when the run ends early. Each tool reads its inputs from the session and writes its result back.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask '...'

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
```

[{'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-styletee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge','band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform':'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_012', 'title': 'Oversized Crewneck Sweatshirt — Vintage Navy', 'description': 'Perfectly faded navy crewneck. Genuinely vintage — not manufactured distressed. Ribbed cuffs and hem. No graphics, clean.', 'category': 'tops', 'style_tags': ['vintage', 'basics', 'oversized', 'classic'], 'size': 'XL (fits oversized)', 'condition': 'good', 'price': 20.0, 'colors': ['navy'], 'brand': None, 'platform': 'thredUp'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}]

```
$ python -c from tools import suggest_outfit; from utils.data_loader import get_empty_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_empty_wardrobe()))"
```

**Outfit 1: Casual Streetwear**
*   **New item:** Vintage Levi's 501 Jeans
*   **Top:** White ribbed tank top
*   **Outerwear:** Oversized grey crewneck sweatshirt (worn layered over the tank or draped over the shoulders)
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

**Outfit 2: Edgy Casual**
*   **New item:** Vintage Levi's 501 Jeans
*   **Top:** Black cropped zip hoodie
*   **Shoes:** Black combat boots
*   **Accessories:** Brown leather belt

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
```

I finally found the holy grail of denim on depop and grabbed these vintage Levi's 501 jeans in a medium wash. They were only $38.00 and the fit is absolute perfection. I am going to wear them with crisp white sneakers and a simple cotton t shirt for running weekend errands.


---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* I gave Claude the `create_fit_card` docstring and asked for the implementation.
- *What came back:* A prompt that passed the item title, price, and platform. The caption it produced said "I just listed them on depop for $38.00", as if I were the seller.
- *What I changed:* I rewrote the prompt to say the writer is a shopper who just bought the item, and renamed the fields to "Price paid" and "Bought on". The caption then read as a buyer's post.

**Moment 2**

- *What I asked for:* I asked Claude for the `create_fit_card` implementation, and it wrote the prompt with a limit of 2 to 4 sentences. I pointed out that a sentence count alone is vague: a model could chain clauses with dashes (`—` or `-`) into one long sentence, since dashes are not sentence-ending punctuation, and still pass the count.
- *What came back:* A prompt that enforced the 60-word cap. Claude had picked 60 on its own, with no data behind it.
- *What I changed:* I removed the 60-word cap because it felt too rigid. I kept the sentence-ending definition. Dashes are still a known gap, so I plan to run the tool several times, look at real caption lengths, and decide whether a cap based on that data is needed.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
(.venv) PS C:\Users\Faustine Chen\FC\Master\CodePath\AI201\ai201-project2-fitfindr-starter-v2026> python app.py ask 'Y2K era items that is under $30' --trace
```
[1] parse_query
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings
      in:  dict with keys: description, size, max_price
      out: 5 items: Low-Rise Cargo Pants — Khaki, Biker Shorts — Black, Shiny, Mesh Long-Sleeve Top — Black … +2 more
[3] select_item
      in:  5 results
      out: Low-Rise Cargo Pants — Khaki ($27.0, poshmark)
      →    results found, picking the first
[4] suggest_outfit
      in:  dict with keys: item, wardrobe_items
      out: **Outfit 1: Y2K Streetwear** *   **New Item:** Low-Rise Cargo Pants *   **Owned Pieces:** Black cropped zip ho…
[5] create_fit_card (via MCP)
      in:  item: Low-Rise Cargo Pants — Khaki ($27.0, poshmark) | outfit: **Outfit 1: Y2K Streetwear** *   **New Item:** …
      out: Scored these low-rise khaki cargo pants on Poshmark for $27.00 and I am already obsessed with them. I am defin…

  Found:    Low-Rise Cargo Pants — Khaki — $27.0 on poshmark

  Outfit:   **Outfit 1: Y2K Streetwear**
*   **New Item:** Low-Rise Cargo Pants
*   **Owned Pieces:** Black cropped zip hoodie, Chunky white sneakers, Black crossbody bag

**Outfit 2: Casual Contrast**
*   **New Item:** Low-Rise Cargo Pants
*   **Owned Pieces:** White ribbed tank top, Vintage black denim jacket, Black combat boots, Brown leather belt

  Fit card: Scored these low-rise khaki cargo pants on Poshmark for $27.00 and I am already obsessed with them. I am definitely pairing them with my black cropped zip hoodie and chunky white sneakers for a total Y2K streetwear moment. Tomorrow I am switching it up with a white ribbed tank top, my vintage black denim jacket, and combat boots for that effortless casual contrast.

0 model calls this session, 1 served from cache


**Empty search**

```
python app.py ask 'winter parka size XXXL under $1' --trace
```
[1] parse_query
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings
      in:  dict with keys: description, size, max_price
      out: [] (empty)
[3] branch: no results
      →    stopping before suggest_outfit / create_fit_card

  No listings matched. You could:
  - use broader keywords (e.g. 'jacket' instead of a specific style)
  - try a different size than 'XXXL'
  - raise your price limit above $1

0 model calls this session


**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
