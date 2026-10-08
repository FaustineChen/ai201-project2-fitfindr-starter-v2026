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
### `parse_query`

- **What it does:** Extracts `description`, `size`, and `max_price` from a plain-language query. Spelled-out sizes "small", "medium", "large", and "extra large" are normalized to "S", "M", "L", and "XL" before matching; other size values are passed through unchanged.


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
**Moment 1**

- *What I asked for:* I wanted queries a real user might type, like "size L or M" and "size smaller than M", because I expected the size parsing to struggle with them.
- *What came back:* Claude said these would likely break `parse_query` and suggested defining supported behavior for them in the Tool Inventory (L or M → {L, M}, smaller than M → {XS, S}) so they could go into criterion 5.
- *What I changed:* I questioned that, because changing the spec to fit the queries means the spec is following the test instead of the other way around. I kept the spec as is, left both queries out of the five criteria, and listed them under What's Still Broken as unsupported.

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
| 1. A matching query completes all three tools (matching query completes) | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. An impossible query stops before the second tool(impossible query stops early) | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. The fit card contains what the spec requires (fit card, hoodie) | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. The fit card contains what the spec requires (fit card, empty wardrobe) | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Search results respect the size and price filters (matching query completes) | every query passes | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Search results respect the size and price filters (fit card, hoodie) | every query passes | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Search results respect the size and price filters (fit card, empty wardrobe) | every query passes | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Search results respect the size and price filters (tee or hoodie in size L) | every query passes | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Search results respect the size and price filters (sneakers size 9 under $60) | every query passes | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

- Criterion 3 is not in this table because it is checked by check_loop.py, which spies on the ids reaching each tool (five runs, output below); the other four are read from the run_eval.py run log.
- Rows that name the same scenario are judged from the same five runs.


**Real output from one try**, pasted as text, naming the file and function
that produced it:

**Produced by `check_downstream_tools.py` (spying on `agent.run_agent`):**

```
[1] parse_query
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Vintage Band Tee — Faded Grey, Graphic Tee — 2003 Tour Bootleg Style … +7 more
[3] select_item
      in:  10 results
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
      →    results found, picking the first
[4] suggest_outfit
      in:  dict with keys: item, wardrobe_items
      out: **Outfit 1: Casual Y2K Streetwear** *   **New Item:** Y2K Butterfly Baby Tee *   **Bottoms:** Baggy straight-l…
[5] create_fit_card (via MCP)
      in:  item: Y2K Baby Tee — Butterfly Print ($18.0, depop) | outfit: **Outfit 1: Casual Y2K Streetwear** *   **New It…
      out: I am so obsessed with this Y2K butterfly baby tee that I just scored on depop for $18.00. I am definitely styl…
try 5: PASS  {'selected_item': 'lst_002', 'search_results[0]': 'lst_002', 'suggest_outfit': 'lst_002', 'create_fit_card': 'lst_002'}

5/5
```



**Produced by `python run_eval.py --label before`:**

### matching query completes (Criterion 1, 5)

- Query: `vintage graphic tee under $30`
- Wardrobe: example

**Try 1**

- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Outfit suggestion:

```
**Outfit 1: Casual Y2K Streetwear**
*   **New Item:** Y2K Butterfly Baby Tee
*   **Bottoms:** Baggy straight-leg jeans (dark wash)
*   **Outerwear:** Vintage black denim jacket (slightly cropped)
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

**Outfit 2: Edgy Contrast**
*   **New Item:** Y2K Butterfly Baby Tee
*   **Shoes:** Black combat boots
*   *(Optional addition: The baggy jeans or wide-leg khaki trousers)*
```

Fit card:

```
I just scored this Y2K butterfly baby tee on Depop for $18.00 and I am completely obsessed with it. I am definitely styling it for casual streetwear with baggy dark wash jeans, a cropped black denim jacket, and chunky white sneakers. Alternatively, I might switch the vibe to something a bit more edgy by pairing the tee with heavy black combat boots.
```

### impossible query stops early (Criterion 2 — the branch)

- Query: `designer ballgown size XXS under $5`
- Wardrobe: example

**Try 1**

- stopped early: yes — No listings matched. You could:
  - use broader keywords (e.g. 'jacket' instead of a specific style)
  - try a different size than 'XXS'
  - raise your price limit above $5
- selected_item: (none)
- search_results: 0


### fit card, hoodie (Criterion 4, 5)

- Query: `hoodie size L under $40`
- Wardrobe: example

**Try 1**

- stopped early: no
- selected_item: Vintage Graphic Hoodie — Faded Black ($26.0, depop)
- search_results: 1

Outfit suggestion:

```
**Outfit 1: The Ultimate Grunge Streetwear Look**
*   **New Item:** Vintage Graphic Hoodie (Faded Black)
*   **Bottoms:** Baggy straight-leg jeans, dark wash
*   **Shoes:** Black combat boots
*   **Accessories:** Black crossbody bag

*Why it works:* The faded black graphic hoodie matches the edgy, streetwear, and grunge aesthetic of the baggy dark-wash jeans and combat boots. It leans into an effortless, relaxed silhouette.

**Outfit 2: High-Contrast Casual**
*   **New Item:** Vintage Graphic Hoodie (Faded Black)
*   **Bottoms:** Wide-leg khaki trousers
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Brown leather belt (threaded through the trousers for contrast)

*Why it works:* Pairing the faded black grunge hoodie with clean, minimal khaki trousers creates a balanced high-low mix of earth tones and vintage streetwear, grounded by chunky white sneakers.
```

Fit card:

```
I am so obsessed with this vintage graphic hoodie that I just scored on depop for $26.00. The faded black wash has the absolute best lived-in grunge feel for throwing on with baggy dark jeans and combat boots. I am also planning to style it with clean khaki trousers and chunky white sneakers for an easy high-contrast streetwear look.
```

### fit card, empty wardrobe (Criterion 4, 5)

- Query: `denim jacket under $50`
- Wardrobe: empty

**Try 1**

- stopped early: no
- selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
- search_results: 7

Outfit suggestion:

```
Your wardrobe is currently empty, so these ideas use common wardrobe basics.

**Outfit 1: Casual Streetwear**
*   White crewneck t-shirt (not owned)
*   High-waisted black straight-leg jeans (not owned)
*   White canvas sneakers (not owned)

**Outfit 2: Double Denim**
*   Black fitted bodysuit (not owned)
*   Dark wash relaxed denim jeans (not owned)
*   Ankle boots (not owned)
```

Fit card:

```
I finally found the exact light wash, cropped denim jacket I was hunting for on Poshmark and I only paid $42.00 for it. I am picturing it thrown over a casual streetwear fit with a white crewneck t-shirt, high-waisted black straight-leg jeans, and white canvas sneakers. It would also look so good leaning into a double denim vibe paired with a black fitted bodysuit, dark wash relaxed denim jeans, and ankle boots.
```

### tee or hoodie in size L (Criterion 5)

- Query: `tee or hoodie in size L`
- Wardrobe: example

**Try 1**

- stopped early: no
- selected_item: Vintage Band Tee — Faded Grey ($19.0, depop)
- search_results: 4

Outfit suggestion:

```
**Outfit 1: Casual Grunge Streetwear**
*   **Top:** Vintage Band Tee (New item) layered under the **Black cropped zip hoodie**
*   **Bottoms:** Baggy straight-leg jeans (dark wash)
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

**Outfit 2: Edgy Contrast**
*   **Top:** Vintage Band Tee (New item)
*   **Outerwear:** Vintage black denim jacket (slightly cropped)
*   **Bottoms:** Wide-leg khaki trousers
*   **Shoes:** Black combat boots
```

Fit card:

```
I honestly cannot believe I scored this faded grey vintage band tee for only $19.00 on depop. The wash on it is so perfectly worn in and looks amazing layered under my cropped black zip hoodie with baggy jeans and chunky sneakers for a casual grunge streetwear vibe. I am definitely going to wear it next with khaki trousers and combat boots for that effortless edgy contrast.
```

### sneakers size 9 under $60 (Criterion 5)

- Query: `sneakers size 9 under $60`
- Wardrobe: example

**Try 1**

- stopped early: no
- selected_item: Low-Top Canvas Sneakers — Off-White ($20.0, poshmark)
- search_results: 1

Outfit suggestion:

```
Here is an effortless outfit combining the new low-top canvas sneakers with your existing wardrobe:

* **Top:** White ribbed tank top
* **Bottoms:** Baggy straight-leg jeans (dark wash)
* **Outerwear:** Vintage black denim jacket (worn over the tank)
* **Shoes:** Low-Top Canvas Sneakers (Off-White)
* **Accessories:** Black crossbody bag

**Why it works:** The off-white/cream canvas sneakers give a relaxed, classic contrast to the dark indigo denim, while the fitted white tank and black denim jacket tie the minimal streetwear aesthetic together.
```

Fit card:

```
I finally scored these low-top canvas sneakers on Poshmark for only $20.00 and I am already obsessed with them. I am pairing them with dark wash baggy jeans, a white ribbed tank, and my favorite vintage black denim jacket for the ultimate minimal streetwear vibe. The cream color of the shoes just ties the whole effortless look together.
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
| 1 | A matching query completes all three tools | 4 of 5 | MET (5/5) | All 5 runs of "matching query completes" reached `create_fit_card` and returned a fit card. |
| 2 | An impossible query stops before the second tool | 5 of 5 | MET (5/5) | All 5 runs stopped with an error message and no `outfit_suggestion`; `suggest_outfit` was never called. |
| 3 | The selected item is the same item reaching both downstream tools | 5 of 5 | MET (5/5) | `check_loop.py`: in all 5 runs, the ids of `selected_item`, `search_results[0]`, and the `new_item` received by `suggest_outfit` and `create_fit_card` were identical. |
| 4 | The fit card contains what the spec requires | 4 of 5 per query | MET (hoodie 5/5, empty wardrobe 5/5) | Counted sentences with the segmenting rule and string-searched price and platform in every card; each had 2 to 4 sentences and exactly one price and one platform mention. |
| 5 | Search results respect the size and price filters | every query passes | MET (5 of 5 queries) | For each query, results were non-empty and every listing's size and price satisfied the query's values; the 5 runs of each query agreed. |


**Diagnoses**
No criterion was missed, so there is nothing to diagnose against the five targets.
However my targets were low for criterion 4: it targeted 4 of 5, but both queries passed 5 of 5 (all tests had 2 to 4 sentences and one price and platform mention). I would tighten it to 5 of 5 per query.
While reviewing parse_query and _size_matches, I found a gap my scenarios did not cover: a spelled-out size like “size medium”. Running python app.py ask 'vintage graphic tee in size medium' --trace (see below). Location: tool (parse_query); mechanism: it passes the raw word after “size” to _size_matches, which compares whole tokens, so “medium” never equals “m”.

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
  - try a different size than 'medium'
```

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
move create_fit_card to MCP, all tools behaved the same


---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**
In `parse_query` (`agent.py`), a size spelled out after the word "size" is now normalized to the abbreviation the listings use: "small" → "S", "medium" → "M", "large" → "L", "extra large" / "x-large" → "XL". The regex tries these phrases before the generic one-token rule, and any size not in the table is passed through unchanged, so "size M", "size M/L", "size 9" and "size W30" behave as before.

**Which failure it was meant to fix:**
None of the five criteria was missed, so this is not a fix for a MISSED row. It targets a gap my scenarios did not cover.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all three tools (matching query completes) | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. An impossible query stops before the second tool(impossible query stops early) | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. The fit card contains what the spec requires (fit card, hoodie) | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. The fit card contains what the spec requires (fit card, empty wardrobe) | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Search results respect the size and price filters (matching query completes) | every query passes | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Search results respect the size and price filters (fit card, hoodie) | every query passes | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Search results respect the size and price filters (fit card, empty wardrobe) | every query passes | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Search results respect the size and price filters (tee or hoodie in size L) | every query passes | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Search results respect the size and price filters (sneakers size 9 under $60) | every query passes | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Search results respect the size and price filters (matching query completes with spelled-out size) | every query passes | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

- Criterion 3 is not in this table because it is checked by check_loop.py, which spies on the ids reaching each tool (five runs, output below); the other four are read from the run_eval.py run log.
- Rows that name the same scenario are judged from the same five runs.


**Real output from one try**, pasted as text, naming the file and function
that produced it:

**Produced by `check_downstream_tools.py` (spying on `agent.run_agent`):**

```
[1] parse_query
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Vintage Band Tee — Faded Grey, Graphic Tee — 2003 Tour Bootleg Style … +7 more
[3] select_item
      in:  10 results
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
      →    results found, picking the first
[4] suggest_outfit
      in:  dict with keys: item, wardrobe_items
      out: **Outfit 1: Y2K Streetwear Contrast** *   **New Item:** Y2K Baby Tee *   **Bottoms:** Baggy straight-leg jeans…
[5] create_fit_card (via MCP)
      in:  item: Y2K Baby Tee — Butterfly Print ($18.0, depop) | outfit: **Outfit 1: Y2K Streetwear Contrast** *   **New …
      out: I just scored this Y2K baby tee on depop for $18.00 and I am obsessed with the butterfly print. I wore it toda…
try 5: PASS  {'selected_item': 'lst_002', 'search_results[0]': 'lst_002', 'suggest_outfit': 'lst_002', 'create_fit_card': 'lst_002'}

5/5
```

**Produced by `python run_eval.py --label after`:**

### matching query completes (Criterion 1, 5)

- Query: `vintage graphic tee under $30`
- Wardrobe: example

**Try 1**

- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Outfit suggestion:

```
**Outfit 1: Y2K Streetwear Contrast**
*   **New item:** Y2K Butterfly Print Baby Tee
*   **Bottoms:** Baggy straight-leg jeans (dark wash)
*   **Shoes:** Chunky white sneakers
*   **Outerwear:** Black cropped zip hoodie (worn open or carried)
*   **Why it works:** The fitted, feminine baby tee balances the oversized, low-key vibe of the dark baggy jeans, leaning fully into the Y2K aesthetic. 

**Outfit 2: Casual Crossover**
*   **New item:** Y2K Butterfly Print Baby Tee
*   **Bottoms:** Wide-leg khaki trousers
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag
*   **Why it works:** Pairing the graphic baby tee with neutral, wide-leg trousers creates an easy mix of vintage-cute and minimal earth tones.
```

Fit card:

```
I scored this Y2K butterfly print baby tee on depop for $18.00 and I am already obsessed with it. I am planning to style it with baggy dark wash jeans and chunky sneakers for the ultimate Y2K streetwear contrast. It is also going to look so good dressed down with wide leg khaki trousers and a black crossbody bag for a casual crossover vibe.
```

### impossible query stops early (Criterion 2 — the branch)

- Query: `designer ballgown size XXS under $5`
- Wardrobe: example

**Try 1**

- stopped early: yes — No listings matched. You could:
  - use broader keywords (e.g. 'jacket' instead of a specific style)
  - try a different size than 'XXS'
  - raise your price limit above $5
- selected_item: (none)
- search_results: 0


### fit card, hoodie (Criterion 4, 5)

- Query: `hoodie size L under $40`
- Wardrobe: example

**Try 1**

- stopped early: no
- selected_item: Vintage Graphic Hoodie — Faded Black ($26.0, depop)
- search_results: 1

Outfit suggestion:

```
**Outfit 1: Casual Grunge Streetwear**
* **New Item:** Vintage Graphic Hoodie
* **Bottoms:** Baggy straight-leg jeans, dark wash
* **Shoes:** Chunky white sneakers
* **Accessories:** Black crossbody bag

**Outfit 2: Edgy Contrast Look**
* **New Item:** Vintage Graphic Hoodie
* **Outerwear:** Vintage black denim jacket (layered over the hoodie)
* **Bottoms:** Wide-leg khaki trousers
* **Shoes:** Black combat boots
```

Fit card:

```
Scored this vintage graphic hoodie on depop for only $26.00 and I am already obsessed with the perfectly worn-in faded black wash. I am definitely styling it for casual grunge streetwear with baggy dark wash jeans and chunky white sneakers. For a slightly more put-together contrast look, I will layer a vintage black denim jacket right over it with wide-leg khaki trousers and black combat boots.
```

### fit card, empty wardrobe (Criterion 4, 5)

- Query: `denim jacket under $50`
- Wardrobe: empty

**Try 1**

- stopped early: no
- selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
- search_results: 7

Outfit suggestion:

```
Your wardrobe is empty, so these ideas use common wardrobe basics.

**Outfit 1: Casual Streetwear**
*   Crop top or basic white tee (not owned)
*   High-waisted black leggings or biker shorts (not owned)
*   White sneakers (not owned)

**Outfit 2: Classic Denim on Denim**
*   Simple black turtleneck or fitted tank (not owned)
*   Straight-leg black or white trousers (not owned)
*   Ankle boots (not owned)
```

Fit card:

```
I cannot believe I finally scored this light wash cropped denim jacket on Poshmark for only $42.00. It is the absolute ultimate piece for throwing over a fitted black tank and straight leg trousers for that effortless coffee run vibe. My closet honestly needed this exact layer to pull every single basic outfit together.
```

### tee or hoodie in size L (Criterion 5)

- Query: `tee or hoodie in size L`
- Wardrobe: example

**Try 1**

- stopped early: no
- selected_item: Vintage Band Tee — Faded Grey ($19.0, depop)
- search_results: 4

Outfit suggestion:

```
**Outfit 1: Casual Grunge Streetwear**
* **Top:** Vintage Band Tee (New item)
* **Bottoms:** Baggy straight-leg jeans, dark wash
* **Outerwear:** Vintage black denim jacket
* **Shoes:** Chunky white sneakers
* **Accessories:** Black crossbody bag

**Outfit 2: Edgy Contrast**
* **Top:** Vintage Band Tee (New item)
* **Bottoms:** Wide-leg khaki trousers
* **Shoes:** Black combat boots
* **Accessories:** Brown leather belt and black crossbody bag
```

Fit card:

```
I cannot stop thinking about the wash on this vintage band tee that I just scored on depop for $19.00. I am definitely styling it with baggy dark wash jeans and a black denim jacket for a casual grunge streetwear look. It would also look so cool paired with khaki trousers and combat boots for a more edgy contrast.
```

### sneakers size 9 under $60 (Criterion 5)

- Query: `sneakers size 9 under $60`
- Wardrobe: example

**Try 1**

- stopped early: no
- selected_item: Low-Top Canvas Sneakers — Off-White ($20.0, poshmark)
- search_results: 1

Outfit suggestion:

```
**Outfit 1: Casual Streetwear**
* **New item:** Low-Top Canvas Sneakers (Off-White)
* **Owned pieces:** Baggy straight-leg jeans (dark wash), White ribbed tank top, Vintage black denim jacket, Black crossbody bag
* **Why it works:** The slim, minimal profile of the low-top canvas sneakers contrasts nicely with the volume of the baggy dark wash jeans and the oversized denim jacket, creating an effortless, classic streetwear look.

**Outfit 2: Relaxed Minimalist**
* **New item:** Low-Top Canvas Sneakers (Off-White)
* **Owned pieces:** Wide-leg khaki trousers, White ribbed tank top, Oversized grey crewneck sweatshirt, Brown leather belt
* **Why it works:** The off-white/cream tones of the sneakers tie in seamlessly with the earth tones of the khaki trousers and belt, while the slouchy grey crewneck keeps the outfit relaxed and balanced.
```

Fit card:

```
I finally scored these low-top canvas sneakers on poshmark for $20.00 and I am already obsessed with them. They are going to look so good with my baggy dark wash jeans and oversized black denim jacket for an effortless, classic streetwear look. I cannot wait to style them with my wide-leg khaki trousers and a slouchy grey crewneck for something a bit more relaxed and minimal.
```

### matching query completes with spelled-out size (Criterion 5)

- Query: `vintage graphic tee in size medium`
- Wardrobe: example

**Try 1**

- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Outfit suggestion:

```
**Outfit 1: Y2K Streetwear Contrast**
*   **New Item:** Y2K Butterfly Baby Tee
*   **Bottoms:** Baggy straight-leg jeans (dark wash)
*   **Outerwear:** Vintage black denim jacket
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

**Outfit 2: Casual Earth-Tone Mix**
*   **New Item:** Y2K Butterfly Baby Tee
*   **Bottoms:** Wide-leg khaki trousers
*   **Accessories:** Brown leather belt
*   **Shoes:** Chunky white sneakers
```

Fit card:

```
I scored this cute Y2K butterfly baby tee on depop for $18.00 and I am already obsessed. I am definitely styling it with wide-leg khaki trousers and a brown leather belt for an easy earth-tone look. Chunky white sneakers will tie the whole casual outfit together.
```


**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->
Yes, for the gap I found, and nothing else moved. All five criteria were already MET before the change, so no criterion went from MISSED to MET; the change fixes a case my scenarios did not cover.

- **Before:** `python app.py ask 'vintage graphic tee in size medium' --trace` returned "No listings matched", and the loop stopped before `suggest_outfit` with an error asking me to change the query. No listing has the token "medium", and `parse_query` passed the raw word through.
- **After:** the new scenario (matching query completes with spelled-out size) passed 5 of 5 in `run_eval.py --label after`: `size` was parsed as "M", `search_results` was non-empty, and every listing satisfied the size and price in the query.

---

## What's Still Broken
<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->
No criterion is currently missed. What remains are gaps outside the five criteria, and one target I think is too loose:

- **Criterion 4's target is low.** Both queries passed 5 of 5 against a target of 4 of 5. I would tighten it to 5 of 5 per query. I did not do this in this unit because tightening a number gives nothing to fix.
- **Multi-size and relative sizes are not supported.** "size L or M" and "size smaller than M" are not handled by `parse_query`. I stopped because that changes the tool's input type and the spec, which is more than the one change I scoped.
- **Sizes without the word "size" are not parsed.** "medium hoodie" leaves "medium" in the description. Fixing it needs a rule for when a size word is a size and when it is part of a description.


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
