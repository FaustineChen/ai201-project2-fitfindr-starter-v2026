# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. -->
Search is a plain keyword match, so some phrasings of a query that should match will still miss the listings' wording.
Two of the three tools also call the LLM, so an API error, timeout, or truncated response can end a run before the fit card is produced. 4 of 5 allows for that occasional failure

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->
An empty list from `search_listings` is a deterministic result, and the loop's branch on it is plain code. If it fails even once, it is a bug (such as calling `suggest_outfit`), so 5 of 5 is the right bar.

---

## 3. The selected item is the same item that reaches both downstream tools

<!-- YOU WRITE THIS ONE.

     How would you know that the item your search found is the same item the
     next tool received? Name something countable or observable.

     This is the criterion people find hardest, because state failure doesn't
     look like state failure — it looks like a tool problem. Something that
     compares session["selected_item"] against what actually reached
     suggest_outfit is the shape you're after. -->
In 5 of 5 runs with a matching query, `session["selected_item"]["id"]` equals `session["search_results"][0]["id"]`, and the `new_item` received by `suggest_outfit` and by `create_fit_card` has that same `id`.
Checked by asserting the id at each call.

**Why this target:**
Passing state through the session: either the loop writes the first search result into `selected_item` , or it does not. Any mismatch is a bug, so 5 of 5 is the right bar.
Listing ids are unique, so comparing `id` is a short, countable check of whether the same listing reached every tool.

---

## 4. The fit card contains what the spec requires

<!-- YOU WRITE THIS ONE.

     The fit card calls a model, so the same input can produce different words
     each time. That's not a bug — it's the nature of the tool. So what would
     make it acceptable?

     Think about what you'd actually be unhappy to see. A caption that never
     mentions the price? Two different items producing the same opening
     sentence? A card longer than a caption anyone would post? Any of those can
     be turned into a number. -->
In at least 4 of 5 runs (using different matching queries, including one with an empty wardrobe), the fit card is 2 to 4 sentences, mentions the item's price exactly once, and mentions the platform name exactly once.
A sentence is a segment ending in `.`, `!`, or `?` followed by whitespace or the end of the text, so `$38.00` does not split a sentence. Price and platform are checked by string search in the caption.

**Why this target:**
The prompt asks for these elements, but the model is not guaranteed to follow it. The model's output varies run to run, so 5 of 5 would make the target depend on that variance. 4 of 5 still catches a prompt that fails regularly.

---

## 5. Search results respect the size and price filters

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. Speed, the empty
     wardrobe path, what happens when the model can't be reached, whether the
     search respects a price ceiling — anything, as long as it names a number
     or an observable outcome. -->
For 5 of 5 test queries that state a size or max price, every listing in `session["search_results"]` satisfies the size and price that stated in the query, not the values found in `session["parsed"]`. This catches both a parse that drops the constraint and a search that fails to apply it.

**Why this target:**
Filtering is plain code with no model variance, so 5 of 5 is the right bar. This failure is easy to miss because the agent still completes all three tools and produces a plausible fit card. The data also makes size matching easy to get wrong: a plain substring test lets "s" match "us 9" and "l" match "xl", so the criterion checks the rule I wrote in the Tool Inventory.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
