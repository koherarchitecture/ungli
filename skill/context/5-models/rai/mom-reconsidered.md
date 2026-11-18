# mom reconsidered, without the clean requirement

🛑 **Decided 28 September 2026, 05:37, on his word:** *"I am continuing with minilm based rai, museum model plans are dropped"*. rai stays on MiniLM. Route B was closed by the Ettin test of 27 September (223 of 430 against 0.3.7's 360). Route C and a revived mom are not pursued. Section 3 below (a matched writer for the MoVD model) is dropped along with the MoVD model. Route A (continuing MiniLM's own training on rai-like text) was approved and tested on 28 September 2026 and did not help: the averaged readers counted 327, 318, 304 and 113 over four rounds against 0.3.7's 360 (grapevine 13z18). rai stays on 0.3.7's base.

*27 September 2026, 17:25. A proposal, not a plan: nothing here trains until Prayas says so, and `MOM-PLAN-20260925.md` (archived, binding for the old clean process) is not revived by this file. Asked for in his words: "figure how we can solve why mom was archived. claude generated training data is fine now. i am done with the "clean" thing". Sources: `koher/ARCHIVE-SEPTEMBER-2026/mom-clean-base/` (ARCHIVED.md, LESS-IS-MORE.md, OVERNIGHT-20260924.md, MOM-PLAN-20260925.md), `GRAPEVINE.md`, and one Exa research run the same afternoon (unchecked citations, marked).*

## Why mom was archived — two reasons, only one of them stated

**The stated reason (26 Sep, his word).** Once rai's rows kept Claude-written questions and answers, a clean base bought nothing MiniLM did not already give. Dropping the clean requirement dissolves this reason completely — and with it mom's original purpose. A mom revived now needs a new reason, below.

**The technical wall underneath.** mom never reached MiniLM:

- The best small base, `mom-big-4` round 2, counted **185** on the Claude-worded rows and **117** on rows with no Claude words (version 3), against 0.3.6 on MiniLM at 234–242.
- The wide teacher, `mom-large-1` (12×768), counted 37 and 51 in its first two rounds, its held-out loss rising (5.947 → 6.075); it was behind because of its lower peak rate, and 60 rounds would have taken about six days.
- The plan named the cause itself: a 12×384 model trained from scratch saturates below MiniLM, because MiniLM was not trained from scratch — it was distilled from a base-size teacher trained on 160GB (Wang et al. 2020). mom read its corpus about once (0.16–3B tokens); MiniLMv2's published recipe runs about 52 billion token positions (Exa; unchecked).

## What dropping "clean" solves, and what it does not

**Solved at once: the rows.** Claude-written rows are allowed again, so the drop from 185 to 117 that the Claude-free rows cost is gone. ⚠️ But GRAPEVINE 13z4 found that most of what the Claude-worded rows counted on rai's own forms was the forms' own words — the test sets share wording with those rows. Part of 185, and of 0.3.6's own count, is overlap with the test, not reading. A revived mom should be judged on the unseen set first.

**Solved at once: the teacher.** Any strong open model can be the teacher now. mom no longer has to build its own teacher from scratch on openly licensed text, which was the slow, costly part.

**Not solved by the decision: the scale gap.** A from-scratch small base on a few billion tokens will still sit below a distilled one. That is a fact about how these models learn, not about cleanliness.

## What mom could be for, now

1. **A better base for rai** — aim 250+ (his mark, 26 Sep 2026), above 0.3.6.
2. **A teacher for other models** — his word on 25 Sep, 19:17: *"we will keep mom large as a teacher for all kinds of other models"*. The rai family has thirteen names; a family base serves them all.
3. **A matched writer** — the MoVD model (`museumofvestigialdesire.net/movd-model-20260927.md`) wants a small decoder at rai's size. ⚠️ This touches Koher's own rule that its small models generate no text (26 Sep 2026); the MoVD writer would be MoVD's, not a Koher tool, and SDC's 27 Sep settlement allows a model to do language work where negotiated and configured. His to weigh.

## Three routes, cheapest first

**A. Adapt MiniLM itself (hours).** Keep rai's base; continue its masked-word training on rai-register text (domain-adaptive, then task-adaptive pretraining: Gururangan et al. 2020, eight of eight tasks improved, gains ranging from under a point to about twelve — not measured on extractive reading or at 33M; Exa, unchecked). Then point as now. This is the smallest change and follows the grapevine's rule of one change at a time. "mom" becomes MiniLM made rai's own.

**B. Swap the base for a newer small encoder (a day of tests).** Candidates at rai's size, from Exa (unchecked): **Ettin encoder 32M** (JHU 2025; 10×384, 2T tokens, MIT; a different tokenizer from MiniLM; its authors report it slightly below MiniLM on GLUE and above it on some retrieval) and the MiniLM-shaped retrieval models E5-small-v2 and BGE-small (33M). Test each on rai's three sets as they are, then A on the winner. **Ettin's decisive feature is that it ships a matched decoder, `ettin-decoder-32m`, trained on the same data** — one family covering rai and the MoVD writer.

**C. Distil a new mom from a strong teacher (days).** A 12×384 student trained against a large open teacher (BERT-large or RoBERTa-large) with MiniLMv2's attention-relation distillation, on 0.1–2B tokens of general plus rai-like text, then pointed. Exa's estimate, derived and unmeasured: roughly 2–10 GPU-hours per billion tokens on the Spark. This is mom's original route with the constraint removed: mom-large-1 as teacher is no longer needed, because the teacher can be any open model already trained.

## Suggested order

B's tests first (cheap, and they decide A's starting point), then A on the winner, and C only if A falls short of 250 on the unseen set. One change at a time, three pointing seeds, two rounds, per the grapevine. The GPU work runs detached on the Spark.

## Open, and his

- Whether mom is for rai, for the family, for the MoVD writer, or all three.
- Whether a base with a different tokenizer (Ettin) is acceptable, since rai's released model and ka pahad would change underneath.
- Whether the old gates in MOM-PLAN are rewritten for the unclean route, or a new plan replaces it.
- Whether the MoVD writer is allowed to share a family with Koher's non-speaking models.

## Test started, 27 Sep 2026, 20:36 — his word: *"t6est if ettin reader + squad + minilm helps. else ettin only for writer"*

Route B's first test, on the Mac (MPS), detached: `scripts/ettin-test.sh`, log `runs/ettin-test.log`. One change against 0.3.7, the base: `jhu-clsp/ettin-encoder-32m` taught SQuAD 2.0 (126,704 vegan-filtered rows, `scripts/squad_rows.py`, 2 passes at 3e-5; about two hours), then 0.3.7's rows and recipe exactly (2 passes at 2e-5, batch 32, seeds 7, 1, 2, souped), no token types. **The bar, 0.3.7 re-scored the same evening on the six current test sets at its own threshold 8.92: 360 of 430** — v1 157/180, artwork 20/24, unseen 66/96, ka pahad 52/60, typing 21/24 and 44/46, no false presents. Read the unseen set first (GRAPEVINE 12a, 13z4). ⚠️ Grapevine 13m: SQuAD did not help mom's base; here it is the fair pairing, since MiniLM reaches rai through a SQuAD-trained checkpoint. If Ettin falls short, it is kept for the writer only.

## Result, 28 Sep 2026, 00:44 — Ettin does not help the reader

The Ettin soup counted **223 of 430** (threshold 12.96) against 0.3.7's **360** (8.92); seeds 189, 237, 243, the best still 117 short. Unseen 34 against 66, typing 8/24 against 21/24 (a cased vocabulary against lowercase typing). No false presents in either. By his instruction, Ettin is kept **for the writer only**, and route B is closed for rai; route A (MiniLM made rai's own) is the reader's next step if he wants one. GRAPEVINE 13z17. The first attempt (20:36) died at 20:40 on a SQuAD row of about 1,000 spaces and was found at 22:49 (GRAPEVINE-OPS O9); the run reported here started 22:50.
