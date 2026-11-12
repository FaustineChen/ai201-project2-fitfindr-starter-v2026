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
In at least 4 of 5 runs (using two matching queries, including one with an empty wardrobe), the fit card is 2 to 4 sentences, mentions the item's price exactly once, and mentions the platform name exactly once.
A sentence is a segment ending in `.`, `!`, or `?` followed by whitespace or the end of the text, so `$38.00` does not split a sentence. Price and platform are checked by string search in the caption.

**Why this target:**
The prompt asks for these elements, but the model is not guaranteed to follow it. The model's output varies run to run, so 5 of 5 would make the target depend on that variance. 4 of 5 still catches a prompt that fails regularly. Each query is judged on its own five runs.

---

## 5. Search results respect the size and price filters

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. Speed, the empty
     wardrobe path, what happens when the model can't be reached, whether the
     search respects a price ceiling — anything, as long as it names a number
     or an observable outcome. -->
For 5 of 5 test queries that state a size or max price, `session["search_results"]` is non-empty and every listing in it satisfies the size and price that stated in the query, not the values found in `session["parsed"]`. This catches both a parse that drops the constraint and a search that fails to apply it.

**Change: ** add non-empty search research

**Why this target:**
Filtering is plain code with no model variance, so 5 of 5 is the right bar. This failure is easy to miss because the agent still completes all three tools and produces a plausible fit card.
The data also makes size matching easy to get wrong: a plain substring test lets "s" match "us 9" and "l" match "xl", so the criterion checks the rule I wrote in the Tool Inventory.
An empty list would satisfy ‘every listing’ vacuously, so non-empty is required; search has no model variance, so each query is judged once and its five runs must agree.


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

## Capstone criteria

---

### 1. A temporary model failure recovers

When the stub fails the first 1, 2, or 3 attempts of a model call (503, dropped
connection, or empty reply) and then answers normally, `POST /ask` returns a
session with `error` equal to `None` and a fit card. This must hold in 3 of 3
trials, one trial for each number of failures.

**Why this target:**
The failure is injected, so there is no model variance, and 3 of 3 is the right bar.

### 2. A persistent model failure ends with a readable error, in time

When every model attempt fails, `POST /ask` returns a non-empty `error` sentence with no `Traceback` text and no HTTP 500. This must hold in 3 of 3 trials (503, dropped connection, empty reply).

**Why this target:**
A user who sees a stack trace cannot act on it, but a short sentence tells them to try again. The stub fails the same way every time, so there is no variance and 3 of 3 is the right bar. 

### 3. Retries never exceed the limit

When every model attempt fails, the attempts field in the log is exactly 4 (1 try plus 3 retries), in 3 of 3 trials.

**Why this target:**
The limit is a constant in `config.py`, so the real risk is an off-by-one in the retry loop: 3 attempts would give up too early and 5 would retry too much. "Exactly 4" catches both, while "at most 4" would not. The 429 path has its own `MAX_RETRIES = 5` and is not counted.

### 4. A hung call or an empty reply is treated as a failure

When the stub hangs forever, the model call is cut off and treated as failed within 22s (the 20 s timeout plus 2s thread and scheduling overhead). When the stub returns an empty string, it is retried and never passed on as a result. Neither case crashes a later tool, and the empty-reply case never produces a blank fit card. This must hold in 3 of 3 trials per case.

**Why this target:**
Before this change there was no timeout at all, so a hung call blocked the one-request-at-a-time lock and every later request waited behind it. An empty reply used to pass through as `""`, and this system's fit card would have been blank while the run still looked successful, which is the failure this criterion is meant to catch.

### 5. Every request writes one valid log entry, including failures

For a mixed batch of at least 12 requests (successes, a missing `query` returning 400, a temporary failure, and a persistent failure), the log file has exactly one line per request. Each line parses as JSON and has these fields: `timestamp`, `query`, `status`, `error`, `duration_ms`, `attempts`. In 3 of 3 batches, 100% of lines are valid, with no missing fields and no missing requests.

**Why this target:**
A log that only records successes would pass a weaker test and be useless for diagnosis. The target is 100% because a missing or half-written line cannot be recovered afterwards, and the cost of one is a gap in the evidence for every other criterion.