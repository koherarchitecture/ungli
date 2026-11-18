# *teetar aadhi bater*

**The name (29 October 2026, 14:22; he asked me to choose, *"CHOOSE A NAME FROm the new syntax family"*):** the tool is ***teetar aadhi bater*** and its model is **`aadha`**, so a tool that runs on aadha says the whole idiom, *aadha teetar aadhi bater*, half partridge and half quail, a thing that is neither. The animal dances when the writing is half noise and half story, the very creature the idiom laughs at; and it is SYNTAX's theme, a form taken from two places other than itself. Chosen by the rule: the candidate that names both the family's theme and the tool's function (repeat-reader run `14aad43a`; `naach` was second, naming the dance but not borrowed form).

*Started 29 October 2026, 13:44, on Prayas's word: "train such a model on spark - figure name for it from syntax family of names. this will be a syntax model and project", "train new model, dont use qwen", "small model like rai olr RAM". A SYNTAX model and project.*

**What it is.** A small reader that marks each sentence a student writes with one number (his words, 30 October 2026: *"more than the normal amount of abstraction, layered meaning, analogy etc are considered noise but are the desirable kind of noise"*, then at 12:46 *"abstract poetic nonsense is condered undesirable kind of noise. the 15 is the desirable noise. undesirable noise can be upto 2% only"*): **2 story**, plain writing and the everyday idiom, and imagined writing told plainly: fiction, dialogue and impossible events (his word, 30 October 2026, on that line drawn in `tests/hand-v12.jsonl`: *"1 is correct"*); **1 the good noise**, the desirable kind, more abstraction, layered meaning or analogy than everyday writing (grammar bent on purpose, as e e cummings bends it, was part of it from 12:00 to 14:20 on 30 October; that thread is discarded, `archive/cummings-thread/`); **0 unwanted noise**, gibberish (shuffled words, word piles, random letters) and nonsense with no meaning under it (abstract poetic nonsense, swapped-word nonsense, invented words). Code, not the model, works out the balance from the marks, in two checks: the share of the good noise sets the dance (full at 15%, still beyond 15% ± 12, and below 5% it looks sick), and more than 5% unwanted noise keeps the animal still whatever else the piece does (2% until 31 October, 08:19, his word: *"make them both 5"*); all four numbers are settings on the page. Where the everyday amount of abstraction ends is his to judge; the line drawn in `tests/hand-v9.jsonl`, `tests/hand-v10.jsonl` and `scripts/layered.py` is a proposal: a conventional idiom is story, a fresh image, an extended analogy or an abstraction made to act is the good noise. Earlier keys, kept as the record: until 30 October at 12:00, 1 was *grammar without sense* and figures of speech were taught as story; from 12:00 to 12:46, abstract poetic nonsense was the good noise. `scripts/rekey.py` turns the old rows and hand sets into the present marks (`tests/rekeyed/`).

**How it is made.** `microsoft/MiniLM-L12-H384-uncased` with a new three-way head, the argument notation's classifier recipe (three passes at 5e-5, batch 16, one starting head, seeds 7, 1 and 2, souped). The rows (`scripts/gen.py`) are labelled by how they were made, never by a model: real sentences from the open corpus vetted for rai's base (`koher/ARCHIVE-SEPTEMBER-2026/mom-clean-base/data/pretrain/`), the same sentences with their content words swapped for others of the same tag (spaCy `en_core_web_sm`), and shuffled, random or lettered noise; a third typed as people type; split by a hash of the sentence; every row through rai's vegan scan. English only in this first version.

**Measured against.** The code-only route (`scripts/bar.py`, a word list): 1,873 of 4,500 held-out rows and 14 of 32 on the hand set (`tests/hand-v1.jsonl`, written and keyed before training). The feasibility tests that led here are in `[path withheld]`.

**Run.** `scripts/run-spark.sh` on the Spark (`[path withheld]`, the vLLM environment's Python, `HF_HOME` inside the project); results in `runs/*-results.json`.

**Served.** Soup b is aadha (his choice, 29 October 2026) and is served from `koher/tools-dev/koher-engine-core/aadha/` as its own keyed app, apart from the `koher-engine` app Coherence calls: `aadha` on `blevn`, https://aadha.syntax.prayasabhinav.net, deployed and checked live on 29 October 2026 at 18:19. Nothing calls it yet. The balance settings are on the page and are options of `scripts/balance.py`. **Since 3 November 2026, 22:30, on his word, the app serves soup o4x3 with the adapter reflect2, as 0.6.0+o4x3.reflect2**, in place of 0.5.3+i11.reflect1. o4x3 was taught from Claude's reading (`own/`, his exception of that day), not from his keys; the page reaches the app and offers reflect as before.

## First run, 29 October 2026, 15:02

| | held-out rows (4,500) | hand set (32, keyed before training) |
|---|---|---|
| code only (`scripts/bar.py`) | 1,873 | 14 |
| `aadha`, soup of seeds 7, 1, 2 | 4,399 | 28 |
| seeds alone | 4,384 · 4,389 · 4,382 | 28 · 27 · 29 |

The soup's misses on the hand set: Jabberwocky's invented words read as meaning (1.00), two mild swapped sentences read as meaning, one shuffled sentence read as meaning (0.68). No threshold with no wrong answer exists on the tuning half, because some swapped rows still make sense and carry the wrong label; the counts above are the reader's first choice with no threshold. Lesson 13z54 in the training grapevine. Weights: `runs/soup/` (128 MB); results: `runs/*-results.json`.

## Second run: arms a and b, 29 October 2026, 15:50 to 17:20

Two arms trained on stricter rows, with the first run's soup re-measured on the same fixed sets afterwards (`scripts/after-arms.sh`): **a** stricter swaps (`data-a/`), **b** stricter swaps plus invented words (`data-b/`). The fixed held-out rows are not the first run's, so the first run's 4,399 above and its 4,082 below measure different sets. Counts are the reader's first choice with no threshold; as before, no threshold gives no wrong answer on the tuning half, so the at-threshold columns answer nothing.

| | held-out rows (4,500, fixed) | hand set (32) | hand set 2 (26) |
|---|---|---|---|
| first run's soup | 4,082 | 28 | 19 |
| a | 3,984 | 28 | 19 |
| b | 4,427 | 27 | 21 |

Right by kind on the held-out rows: meaning 1,486 · 1,491 · 1,488; noise 1,456 · 1,460 · 1,466; swapped 976 · 975 · 973; invented 164 · 58 · 500 (first run, a, b). Nearly all of b's lead is the invented-word rows. Which soup becomes `aadha` is his to choose. Weights and results: `runs/a/`, `runs/b/`, `runs/soup-results-fixed.json`.

## The testing copy for students, 29 October 2026

Built on his word: *"make the "teetar aadhi bater" tool ready to deploy - develop full features. make it gated access for 50 students, limited test routine, full logging everythihng for grounding"*. Version 0.1.1 (`VERSION`): from 30 October 2026, 11:42, the link preview and the page's description say *Powered by the aadha model, helping you make aadha teetar, aadhi bater content*, under the title *teetar aadhi bater* (his words).

- **The page** (`web/public/index.html`) is the animal page with the sheet rebuilt: a student writes a piece and presses Read it; code cuts it into sentences, aadha marks each, and the animal dances to the balance worked out in code from the marks and the settings, which the student can change. Each sentence shows aadha's mark and a choice to say it is wrong; a note can be kept with each reading. `web/animal.html` stays as the demo with hand-marked pieces.
- **The server** (`web/server.mjs`, Node, no dependencies) holds the logins, the consent, the limits and the record, and calls aadha at `AADHA_URL` with `AADHA_API_KEY` (on blevn, over CapRover's own network). Who takes part, the routine and what is kept: `grounding/SCHEME.md`.
- **Logins**: 50 students, a teacher and a demo login, issued; passwords in `[a private file]`.
- **Checked 29 October 2026, on the Mac against the live aadha**: no login and a wrong password 401; a reading before consent 403; a reading of the half-and-half piece marked `[2, 1, 2, 1, 2, 0]` and danced 1.00, and 0.00 with the full dance moved to 30%; a fourth reading in a day 429; corrections, notes and settings kept against their reading, refused on someone else's; the export 403 for a student and the whole record, in order, for the teacher; withdraw left one line. Rendered in Chrome at 1920 and 760 with no page errors.
- **Deployed 29 October 2026, 19:50 IST**, on his word (*"deploy teetar-aadhi-bater -- make it ready for grounding"*): the app `teetar-aadhi-bater` on blevn, https://teetar-aadhi-bater.syntax.prayasabhinav.net, made by `web/create-app.py` (persistent volume `teetar-aadhi-bater-data` at `/app/data`, aadha's key its only environment variable, access log off, HTTPS forced) and deployed by `bash web/deploy.sh`. **Checked live**: no login and a wrong password 401; a student login gets the page with 12 readings, 3 today, and no consent; the demo login's reading went through the live aadha (`[2, 1, 2, 1, 2, 0]`), its correction and note were kept and exported marked demo; a student's export 403. The demo login was then withdrawn, so the record starts with that one line. One slip per student (address, login, password) is in `grounding/login-slips.txt`, kept out of git; the record is pulled with `bash grounding/pull.sh`.

## Arms c and d: noise as abstract poetic nonsense, 29 October 2026

His words: *"noise does not mean gibberish, make it very abstract poetic nonsense"*, then, testing `grounding/test-texts.txt`, *"if the resultas are not as expected. fix and retrain"* and *"improve it more"*. `scripts/poetic.py` adds code-generated poetic nonsense to arm b's rows as grammar without sense (label 1): arm c with ten sentence shapes, arm d with twenty-four and more words. The test texts are keyed as `tests/hand-v3.jsonl`, and a fresh set written before arm d trained as `tests/hand-v4.jsonl`; no word of either set's noise lines is in the generator's lists, and the generator refuses to run if one is.

| | held-out b (4,500) | held-out c (5,250) | hand 1 (32) | hand 2 (26) | test texts (65) | fresh set (40) | test pieces dancing as expected (8) |
|---|---|---|---|---|---|---|---|
| soup b | 4,427 | 4,690 | 27 | 21 | 47 | 34 | 2 |
| soup c | 4,417 | 5,167 | 30 | 22 | 61 | 37 | 6 |
| soup d | 4,416 | 5,166 | 31 | 23 | 61 | 38 | 5 |

**Soup c is aadha from 29 October 2026, 22:55**, not d: d's new errors read real story as noise, which counts a student's own story against them (training grapevine 13z55, 13z56). aadha reports the arm (`"weights": "soup c"`) and the tool keeps it with every reading. Still wrong on the test pieces: 1 and 7. The next lever is the line between figures of speech and nonsense.

## Arms e, f and g, and soup g live, 30 October 2026

On his words *"if piece 1 is wrong - fix it. dont give up"* and *"improve it more"*: arm e added 1,500 story rows on the border (figures of speech that mean something, plain errands); arm f filled the poetic shapes with the corpus's own words (`scripts/broad.py`); arm g added every sentence of `grounding/test-texts.txt` to arm f's training rows, twenty times each (`scripts/exemplars.py`), his choice of the fallback, so from then those texts are training rows, not a test. Each arm had a blind hand set keyed before it was built (`tests/hand-v5.jsonl` to `hand-v8.jsonl`); the test pieces for the 15% balance (`grounding/test-texts-15-percent.txt`) were never in training.

| | held-out b | v5 | v6 | v7 | v8 | first eight pieces | 15% pieces | story read as noise, blind |
|---|---|---|---|---|---|---|---|---|
| soup e | 4,423 | 36 | 39 | 37 | 38 | 6 | 10 | 1 |
| soup f | 4,420 | 39 | 40 | 40 | | 6 | 9 | 3 |
| soup g | 4,426 | 37 | 40 | 39 | 40 | 8 (trained on) | 9 | 2 |

**Soup g is aadha from 30 October 2026, 10:29**, his choice over e after v8 showed g's one error on the 15% pieces (*One of them was due back on the fifteenth.*, read as noise, so the all-story Library piece sways at 0.50) was a single line, not a pattern. Checked live: the first eight pieces 8 of 8, the 15% pieces 9 of 10, no key 401. Training grapevine 13z57 to 13z59.

## Arms h, i and i2, and soup i2 live, 30 October 2026

Arm h widened the noise that is wanted to layered meaning, abstraction and analogy (`scripts/layered.py`); arm i is arm h's rows under the present marks (`scripts/rekey.py`), and soup i was live until 15:32. Arm j, grammar bent in the manner of e e cummings, was stopped and the thread discarded at 14:05 (`archive/cummings-thread/`). At 14:15 his word was *"discard mall cummings-style training data from "arm i" and make it work for a "imaginative-writing, general writing tool""*. A blind set of imaginative and general writing, `tests/hand-v12.jsonl`, was keyed first; on it soup i read all 22 story lines (fiction, dialogue, impossible events told plainly, plain prose, idiom) as story and all 8 unwanted lines as unwanted, but caught 5 of 12 lines of the good noise. That fiction and impossible events told plainly are story is his word (*"1 is correct"*, 14:30).

The bent rows turned out to be 7,176 of arm i's 12,000 good-noise rows, not the fifth layered.py's odds suggest, because its other shapes ran out of new sentences. Arm i2 (`scripts/widen.py`) takes them out and adds 4,200 metaphors made without *like* from new tables; hand-v10's six bent lines left the measure. Trained on the Spark 14:20 to 15:29, same recipe.

| set (present marks) | soup i | soup i2 |
|---|---|---|
| `tests/probe-i.jsonl`, written after i2's rows (second-language English, Hinglish, typed, short and long, 4 good noise) | 20/24, good noise 0/4 | 24/24 |
| hand-v12 (its misses shaped i2's tables, so no longer blind) | 35/42, good noise 5/12 | 41/42, good noise 11/12 |
| hand-v9 | 30/40, good noise 5/15 | 32/40, good noise 9/15, two idioms read as good noise |
| hand-v10 (34 lines) | 28/34, good noise 8/14 | 30/34, good noise 10/14 |
| hand-v1 to v8, in total | 309 | 305 |
| held-b, held-c | 4,437 / 5,187 | 4,433 / 5,183 |

Before training the only rule said was that i2 would go live if it measured better. The finer rule was set after the numbers were read, so it is a proposal for him to judge, not a test it passed: more right on the sets keyed under the present marks (probe, v9, v10, v12, +23 lines), against 4 fewer on hand-v1 to v8, which were keyed under earlier marks. Soup i2 went live on `aadha` at 15:32 (`/health` reports *soup i2*). What it still gets wrong: everyday idioms sometimes read as good noise (*a piece of cake*, *music to my ears*), abstract poetic nonsense sometimes reads as story (four lines on v5 and v7 against soup i's two), and good noise said as a plain claim (*A timetable is a map of everyone else's priorities*) still reads as story. Soup i comes back with `bash deploy/make-caprover-tar.sh i` in `koher-engine-core/aadha` and one deploy.

## Arm i3, and soup i3 live, 30 October 2026, 16:54

His words at 15:35: *"so does it need to be better? can we train one more round?"* `tests/hand-v13.jsonl` was keyed first (15:36): on it soup i2 read all 10 idioms as story and all 10 unwanted lines as unwanted, but caught 2 of 8 lines of the good noise said as a plain claim. Arm i3 (`scripts/sharpen.py`) is i2's rows plus 5,000 code-made claims (*A CV is just a ledger of tiny surrenders*, mark 1) and about 1,400 stock idioms in a metaphor's place (*The second semester has been a pain in the neck*, mark 2). Trained on the Spark 15:37 to 16:48.

| set | soup i2 | soup i3 |
|---|---|---|
| hand-v13 (blind for i3) | 35/42, claims 2/8 | 40/42, claims 7/8 |
| probe | 24/24 | 24/24 |
| hand-v9 | 32/40, idioms 8/10, good noise 9/15 | 38/40, idioms 10/10, good noise 13/15 |
| hand-v10 | 30/34 | 33/34 |
| hand-v12 | 41/42 | 41/42 |
| hand-v1 to v8, in total | 305 | 307 |
| held-b, held-c | 4,433 / 5,183 | 4,439 / 5,189 (the best of any arm) |

Better or equal on every set under the present marks and better in total on the older ones, so soup i3 went live on `aadha` at 16:54 (`/health` reports *soup i3*). No story line on hand-v9 to v13 or the probe set is read as noise. Still missed: *Traffic is patience sold by the kilometre* (read as unwanted), *Our old flat still lives in my hands whenever I unlock any door*, *My notebook keeps the version of me that I keep forgetting to become*, *Exams measure the shadow of what we know*, *The old fort guards nothing now except our selfies with it*, *The town wore its history the way a widower wears his wife's wristwatch* (all read as story).

## aadha i3 against Haiku and Sonnet, 30 October 2026, 17:45

His word: *"test with haiku and sonnet"*, after asking why this is worth doing when a chatbot could do it. `tests/hosted/hosted.py` sends every keyed sentence (603: hand-v1 to v13 under the present marks, the probes, i3's three blind spots, the ten test pieces; all written for testing, no student text) to each model through Claude Code on the subscription, the way lakir was compared, with the three marks as the About page states them and no examples. Results: `tests/hosted/compare.txt`.

| | aadha i3 | Haiku | Sonnet |
|---|---|---|---|
| story | 324/328 | 325/328 | 316/328 |
| good noise | 62/72 | 72/72 | 67/72 |
| unwanted noise | 190/203 | 44/203 | 73/203 |
| abstract poetic nonsense (within unwanted) | 141/149 | 4/149 | 30/149 |
| test pieces as built | 10/10 | 10/10 | 10/10 |

The hosted models catch the good noise better, i3's three blind spots included, and read story as well (Sonnet read 12 story lines as noise). The gap is one line of his definition: abstract poetic nonsense is unwanted. Given that definition in words, Haiku called it the good noise 101 times and Sonnet 120; aadha, trained on his keys, holds it. Untested: whether examples in the prompt would move them; most of the 149 poetic lines are in hand-v3 to v8, written when that nonsense was still the wanted noise.

## What changed, kept on the page, from 0.2.0 (30 October 2026)

His word: *"mantain changelog opening in modal on page, attribute insights to testers"*. `grounding/changelog-text.md` is the list; `python3 web/make-about.py` builds it into `web/public/changelog.html` with the About page, and "What changed" in the page's footer opens it in the same modal as the About sections. 🔴 Every change that reaches testers, to the page or to the live soup, gets a line there before it is deployed, and an insight that came from a tester is credited to *a tester*, never by name (his word, 30 October 2026, 22:03: *"ambiguate names in changelog"*), and nobody is quoted who did not consent to quotation. `VERSION` is 0.2.0, which the record stamps on every line from then on.

## Arm i4, 30 October 2026: measured, not live

Built by `scripts/casual.py` on the plan's answers (`next-version-plan.md`): i3's rows plus casual good noise (3,000), similes (2,000), wry claims (600), misspelt story (5,000), short story (3,000), story fragments (3,000) and the testers' 136 new sentences keyed in `grounding/tester-keys.jsonl` (twenty times each). Trained on the Spark 20:43 to about 22:10. Measured on the Mac against soup i3 under the rule agreed before training (more right on the present-mark sets; no more story read as noise; at least 22 of the 23 nonsense lines; no more than 10 rows lost on each held-out set):

| | soup i3 | soup i4 | rule |
|---|---|---|---|
| present-mark sets (v9, v10, v12, v13, v14, probe), 239 lines | 224 | 226 | met |
| story read as noise there | 0 | 1 (*ok so the assignment is due monday right*) | **not met** |
| nonsense lines kept, of 23 | 23 | 23 | met |
| held-b / held-c | 4,439 / 5,189 | 4,424 / 5,174 (−15 each) | **not met** |
| hand-v14, keyed first | 48/57 | 53/57 | |
| i3's three blind spots | 0/3 | 2/3 | |

What i4 learnt: casual layered lines and wry claims (seven of hand-v14's misses now right, two of the three blind spots). What it lost: unwanted noise read as story (on the held-out sets, 20 swapped-word and 7 shuffled lines each; on hand-v14, *under jumped spoon* and a nonsense fragment), the cost of teaching that short, broken and misspelt text is story; and three good-noise lines on v10, v12 and the probes. So soup i3 stays live. The next round needs a counterweight: short gibberish, nonsense fragments and swapped-word nonsense in the same casual forms, marked unwanted. Weights kept in `runs/i4/soup/`.

## Arm i5, 31 October 2026, 00:01: measured, not live; arm i6 started

Arm i5 (`scripts/counter.py`, his word *"build - fix problems pls"*) is i4's rows plus the counterweights of lesson 13z62: short gibberish, nonsense fragments, casual nonsense (all unwanted) and chatty story. Against soup i3 under the same rule: present-mark sets 231 of 239 (i3 224), hand-v14 55 of 57, i3's blind spots 2 of 3, nonsense 23 of 23; but one story line read as noise (*We were packed like sardines on the last bus.*, as the good noise) and the held-out sets 19 rows down each (4,420 / 5,170), mostly swapped-word nonsense (24) and shuffled noise (6) read as story, and two invented-word lines (*the darm ganomps*) read as story. The counterweights did not reach the held-out losses; what is common to i4 and i5 and new against i3 is the misspelt story, which teaches that a sentence of wrong-looking words is story. So soup i3 stays live, and arm i6 is i5 without the misspelt rows (`data-i6/`), to test that, started on the Spark at 00:05. If i6 passes, misspellings need another way in (a single misspelling per sentence, or none in training and a note on the page); if it does not, the held-out losses come from elsewhere.

## Arm i6, 31 October 2026, 01:40: three parts of the rule met, one missed by five rows

i5 without its 5,000 misspelt rows. Against soup i3: present-mark sets 231 of 239 (i3 224), no story read as noise (the sardines idiom is story again), nonsense 23 of 23, hand-v14 55 of 57, i3's blind spots 2 of 3. Held-out sets 4,424 / 5,174, 15 rows below i3 on each, against a limit of 10: on held-b, 21 swapped-word lines and 4 shuffled ones read as story, against 8 story lines and 3 noise lines gained. Taking the misspelt rows out removed the sardines error and four of the nineteen held-out losses, so they were part of the cause, not all of it. Soup i3 stays live by the rule. Whether those held-out swapped-word lines (machine-made in arm b, sentences with their words swapped for others of the same tag) should keep i6 off the page when it is better on every set written for the present marks is his call, not the rule's. Weights in `runs/i6/soup/`.

## Arm i7, and soup i7 live, 31 October 2026, 06:15

i6's rows plus the twin lesson 13z62 asked for, found by looking at what i6 lost (`scripts/shortnoise.py`): the swapped-word lines i6 read as story were short (12.6 words on average against 17.7) and more often typed in lower case, so i7 adds swapped-word nonsense cut to 8 to 14 words (4,000) and shuffled nonsense cut the same way (2,000), half typed in lower case. Trained on the Spark 03:05 to about 04:35. Against soup i3, under the rule agreed before i4: present-mark sets 230 of 239 (i3 224), no story read as noise, nonsense 23 of 23, held-out sets 4,433 / 5,183 (−6 each, within the limit of 10). **All four met, so soup i7 went live on `aadha` at 06:15** (`/health` reports *soup i7*). Its three seeds scored 4,423, 4,436 and 4,440 on held-b, so the spread between seeds (17) is wider than the gap to i3. Checked on i7 the same morning: the invitations' example lines read as the good noise; the About page's four examples read as written; all ten test pieces and the three samples come out as built; one line of the page's example bank (*One of them was due back on the fifteenth.*, in "Library fine") reads as unwanted, so that story was taken out of `web/public/examples.json`. Gains over i3: hand-v14 55 of 57 (48), i3's blind spots 2 of 3 (0). Weights in `runs/i7/soup/`.

## Version numbers, from 31 October 2026

`ROADMAP.md` holds the logic (his word: *"put on a semver roadmap and develop a version number logic"*): one number for what a tester meets, `MAJOR.MINOR.PATCH+soup`, the live soup as build metadata; MINOR for a new live soup, a new thing on the page, or (below 1.0) a change to the marks; PATCH for wording, fixes and the example bank; 1.0.0 his to call. `web/deploy.sh` refuses a `VERSION` with no heading of its own in `grounding/changelog-text.md` and rebuilds the page changelog on every deploy. `VERSION` is 0.3.0+i7.
