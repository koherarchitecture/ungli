# mein sagar: the reader and its test

*4 November 2026, 12:02; moved from `../aadha-teetar-aadhi-bater/own/next-version-plan.md` the same day at 17:35. The training scripts stayed in aadha's folder until 20:34 that day, when they moved here on his word (`HANDOFF.md`, 20:34): `scripts/run-whole.sh`, `scripts/run-whole-all.sh`, `scripts/run-whole-o4.sh`, `own/whole-rows.py`, `own/whole-read.py`, and the test scripts named below, all now in this folder; paths written `../aadha-teetar-aadhi-bater/…` below are as they stood when written.*

Another interface for using aadha, on your words: "this will be deployed AS another interface for using aadha. figure name in family", "line by line version not needed - remove". Local only, in this folder, not deployed. The reader is an adapter on soup o9x3 with five seeds, reading a whole text up to 512 tokens. The limits are 100 to 350 words, and a text outside them gets no mark.

Test with 67 Museum pages held out (three seeds, 573 Museum parts trained). Read as good noise: 129 of 132 held Museum parts. Read as story: 99 of 100 student essays, 44 of 50 ETS essays, 68 of 72 runs of plain sentences, 4 of 4 stories. Of 11 testers' pieces, which have no label, 5 read as good noise. All the good-noise rows are one writer's, so this does not show whether it learnt the kind of writing or the writer. The version in the demo trains on all 338 pages, so the Museum has no test of its own there; on the same others it reads 99 of 100, 46 of 50, 71 of 72 and 4 of 4 as story.

The animal's answer, dance on good noise and still otherwise, is my placeholder and yours to change. The name is my pick from run e79ff7f3, all five candidates unsure.

*The animal's answer above was later replaced: the pot took the bird's place on his word at 12:25.*

## On the live base, without the columnists, 4 November 2026, 18:37

On his yes. `gagar` retrained as an adapter on `o4x3`, the base aadha serves, in about seven minutes on the Spark (`scripts/run-whole-o4.sh`, in aadha's folder). His 31 columnists' pages are out, on his words "NOT THE COLUMNIST PAGES, NOT MINE"; his 2 hidden pages stay. Checked: 0 of the 31 columnists' pages have a paragraph in the training rows, against 303 of his 307 as the control. The adapter is `../aadha-teetar-aadhi-bater/runs/ad-o4x3/whole-all/soup`, 1.8 MB, and the copy of the model that was in this folder is gone.

| Read as | Text | `o9s5` | `o4x3`, 67 pages held out | `o4x3`, what ships |
|---|---|---|---|---|
| The good noise | Held Museum parts | 129 of 132 | 129 of 132 | none left to test |
| Story | Student essays | 99 of 100 | 99 of 100 | 99 of 100 |
| Story | ETS essays | 44 of 50 | 47 of 50 | 47 of 50 |
| Story | Runs of plain sentences | 68 of 72 | 70 of 72 | 72 of 72 |
| Story | Example stories | 4 of 4 | 4 of 4 | 4 of 4 |

**Other writers, a test only, on his yes.** Neither trained on, and with no label, since whether they are good noise is his to say:

| Text, from Project Gutenberg | Parts | Read as the good noise, held-out | Read as the good noise, what ships |
|---|---|---|---|
| Emerson, *Essays: First Series* | 269 | 254 | 251 |
| Russell, *The Problems of Philosophy* | 163 | 78 | 70 |

So the reader did not simply learn one writer: most of Emerson reads as the good noise though it never saw him. Russell splits about in half. What this leaves open is what it did learn. It may be philosophical meaning, or an older, abstract, essayist's manner, which Emerson has and Russell's plainer analysis has less of. Age alone is tested below.

Of 11 testers' pieces, 5 read as the good noise, as before.

**Old prose with no philosophy in it, a test only, on his yes (4 November 2026, 18:46).** `../aadha-teetar-aadhi-bater/own/old-prose-read.py`, on the same cut. Read as the good noise:

| Text, from Project Gutenberg | Parts | Held-out version | What ships |
|---|---|---|---|
| Darwin, *The Voyage of the Beagle* (1839) | 732 | 11 (2%) | 7 (1%) |
| Dana, *Two Years Before the Mast* (1840) | 568 | 46 (8%) | 27 (5%) |
| Emerson, *Essays: First Series* (1841) | 269 | 254 (94%) | 251 (93%) |
| Russell, *The Problems of Philosophy* (1912) | 163 | 78 (48%) | 70 (43%) |

Three books from within two years of each other split by what they do, not by when they were written, so old-fashioned prose alone does not make the good noise. Those three also rule out little else: a reader could still be keyed to abstract, reflective, aphoristic prose as a manner, with or without an argument in it, and Russell's plainer, step-by-step philosophy reading only about half would fit that. Nothing here separates that manner from the meaning, and every text on the good-noise side of training is still one writer's.

## Tested on Museum text it never saw, 4 November 2026, 20:00

His word: "I want to check sagar with movd text". Nothing was compressed or rewritten: `../aadha-teetar-aadhi-bater/own/movd-check.py` reads overlapping windows of up to 350 words of his own sentences in his own order, with the reader trained without these 61 pages. The live reader has seen all his pages, so it cannot be tested on them.

| Test | Read as the good noise |
|---|---|
| Unseen pages, every window | 180 of 182 |
| Unseen pages over 350 words, every window good noise | 45 of 46 pages |
| *Audience*, 578 words, which the line reader put at 1% | 3 of 3 windows |
| The same windows, sentences shuffled | 180 of 182 |
| Sentences dealt from two different pages | 27 of 27 |
| The same windows, every word shuffled | 0 of 182; all read unwanted noise |
| Student and ETS essays, in order and shuffled | 4 of 150 and 4 of 150 |
| Columnists' pages, in the Museum, not his | 53 of 55 |

How much text it needs (`own/movd-length.py`), his sentences in his order:

| At least | Museum | Essays |
|---|---|---|
| One sentence | 11.7% | 1.5% |
| 15 words | 20.1% | 1.2% |
| 30 words | 39.3% | 1.1% |
| 50 words | 63.6% | 1.3% |
| 75 words | 79.2% | 2.2% |
| 100 words | 84.9% | 1.3% |
| 150 words | 87.4% | 1.6% |
| 250 words | 95.4% | 1.9% |
| 350 words | 98.6% | 73 Museum windows; essays too few to count, 0 of 2 |

What this shows: the answer does build up across a text, as his "text-wide" said, and essays stay flat however long they get. What it does not show: the order of the sentences plays no part, so it is not following an argument. It is adding up a kind of sentence. It reads that kind in other writers too (columnists, Emerson 93%, Russell 43%). Abstract prose with nothing behind it has not been tried, so whether it can tell meaning from the manner of meaning is still open.

## Tested on 140 books from Project Gutenberg, 4 November 2026, 20:39 to 20:52

His word, 20:04: "ask it to test rigously with gutenbergt text". Test only, never training. The books were chosen by a rule written before any was read (`sources/gutenberg/RULE.md`, with the predictions made beforehand; the list is `books.json`, md5 `2aee30bb…`): Gutenberg's own subject headings and category shelves, ten headings of fourteen books, seven authors a heading with two works each, 71 authors in all, no book swapped afterwards. Each book, licence stripped and front and back matter dropped by a rule, was cut as a Museum page is cut (parts of 100 to 350 words), at most 150 parts a book spaced through it, and read by the reader that never saw the 61 held pages (`runs/ad-o4x3/whole/merged`) as written, with its sentences shuffled and with its words shuffled, and by the live reader as written. Script `own/gutenberg-read.py`, run on the Spark in 771 s; results `sources/gutenberg/results.json`; every table, by book as well, in `sources/gutenberg/report.md` (`own/gutenberg-report.py`). The headings are the catalogue's sorting, not his judgement; no reading below is a label.

| Heading | Books | Parts | Read as the good noise, in order | Mean of the books (95%, resampling books) | Spread across books | Sentences shuffled | Words shuffled | Live reader |
|---|---|---|---|---|---|---|---|---|
| essays | 14 | 1,753 | 71% | 69% (59 to 78) | 26 to 93 | 70% | 0% | 65% |
| philosophy | 14 | 1,928 | 45% | 46% (36 to 56) | 14 to 94 | 45% | 0% | 38% |
| religion (sermons, theology) | 14 | 1,392 | 34% | 31% (20 to 42) | 0 to 69 | 35% | 0% | 28% |
| speeches | 14 | 1,090 | 29% | 31% (19 to 43) | 0 to 73 | 30% | 0% | 22% |
| letters | 14 | 1,830 | 16% | 16% (8 to 25) | 0 to 65 | 15% | 0% | 10% |
| manuals and textbooks | 14 | 1,567 | 10% | 9% (4 to 14) | 0 to 27 | 11% | 0% | 8% |
| science | 14 | 1,796 | 9% | 10% (4 to 17) | 0 to 42 | 9% | 0% | 8% |
| fiction | 14 | 1,664 | 8% | 8% (5 to 11) | 0 to 24 | 8% | 0% | 7% |
| history | 14 | 1,574 | 7% | 5% (1 to 10) | 0 to 21 | 7% | 0% | 4% |
| travel | 14 | 2,040 | 2% | 2% (1 to 4) | 0 to 11 | 2% | 0% | 2% |

Every word-shuffled part read as unwanted noise. The reading rises with length on the high headings as it did on the Museum (essays 11% at one sentence, 42% at 100 words, 77% at 350; philosophy 4%, 23%, 53%) and stays flat on travel (1% to 2%) and fiction (1% to 7%). The writer's birth century and the catalogue's translation flag show no steady relation to the reading inside a heading. Nine books hold a sentence of the story-side training runs, at most eight (Emerson's *First Series*), and read no differently from their neighbours.

**Order plays no part, in any kind of writing.** Shuffling the sentences moved no heading by more than one point; per part, the probability of the good noise is the same to three decimals in order and shuffled, and shuffling lowered it on 46% to 55% of parts, a coin toss; 1% to 6% of parts changed mark, the ones at the threshold. The reader carries no trace of order.

**What it reads is a register, not argument and not grandness.** Against the predictions written first: essays came as expected; philosophy (46%) and religion (31%) came in under the 60% and 50% I had written, with a wide spread inside each: Santayana 94% and 82%, Hume's *Enquiry* 60%, Holbach 69% and 53%, against Moore's *Principia Ethica* 27% and *Philosophical Studies* 14%, Russell 48%, the Paulist sermons 25%, Haeckel 0% to 10%. Science came in under my 10% line: Darwin's *Origin of Species* read 2%, Faraday 1% and 7%, Somerville 0% to 1%, with Bacon 25% to 27% and Tyndall's Belfast address 42% the exceptions. The oratory proper read low (Demosthenes 7% and 9%, Webster 15% and 32%, Roosevelt 0% and 27%, Wilson at war 27%), while two manuals on how to speak read high (Pittenger's *Oratory Sacred and Secular* 71%). So a sustained argument about nature (the *Origin*) and a grand manner (Demosthenes, Webster) both read as story, and reflective prose about conduct, mind, belief, art and life reads as the good noise in whoever writes it, across three centuries and in translation. The surprise I had not written: the live reader, trained on all his pages, reads other writers 5 to 7 points lower than the held-out reader on the four high headings.

What this cannot say: whether that register is what he means by "a rational or philosophical meaning, more than a report has room for". The *Origin* has rational meaning and reads 2%; whether it is the good noise by his definition is his to say. `sources/gutenberg/blind-sheet.md` holds ten windows, one each from Darwin, Moore, Demosthenes, Webster, the Paulist sermons, Santayana, Pittenger, Holbach, Abelard and Tyndall, numbered in a shuffled order with no mark shown (the marks are in `blind-key.json`, not to be opened first), for him to key if he chooses; by his rule of 2 November a components file comes first.

## `whole-order`: shuffled pages taught as story, 4 November 2026, 21:21 to 21:40

His answers at 21:19: a Museum text with its sentences shuffled is story ("No: it becomes story", "with sentences shuffled meaning is not progressive right"), and yes to the run. `own/order-rows.py` wrote the 573 training parts of his pages in order twice as the good noise and the same parts shuffled once as story, with the story side unchanged and the held pages out. Three seeds and a soup, on the Spark, with the same recipe as `whole` (LoRA r=8, three epochs, 2e-4). Nothing went live and `whole-all` is untouched. Its average training loss was 0.69 against about 0.40 for the plain arm. The rule was written before the run, in `DONE-MAC-hermes-gagar-fix.md`.

| Test | The rule | `whole` | `whole-order` | Holds |
|---|---|---|---|---|
| Held windows, in order | at least 175 of 182 | 180 | 180 | yes |
| Held windows, sentences shuffled | under 91 of 182 | 180 | 151 | no |
| Sentences dealt from two pages | under 14 of 27 | 27 | 26 | no |
| Essays, in order | at most 6 of 150 | 4 | 5 | yes |
| Essays, shuffled | at most 6 of 150 | 4 | 2 | yes |
| Gutenberg headings, in order | within 10 points | – | science +22, philosophy +14, religion +13, speeches +13, letters +11 | no |

Every word shuffled still reads 0 of 182. On the held test parts it reads 131 of 132 in order and 110 of 132 shuffled as the good noise, Emerson 81% and Russell 64%.

**Measured after the run, on its own training rows** (`own/order-train-read.py`): of the 573 shuffled parts it trained on, it read 135 as story and 438 as the good noise, and 1,110 of the 1,146 in-order rows as the good noise. So it did not learn order and fail to carry it over; on this recipe it barely learnt it at all. One recipe does not show the adapter cannot.

| Gutenberg, read as the good noise | `whole` in order | `whole-order` in order | `whole` shuffled | `whole-order` shuffled |
|---|---|---|---|---|
| essays | 71% | 65% | 70% | 52% |
| philosophy | 45% | 59% | 45% | 47% |
| religion | 34% | 47% | 35% | 28% |
| speeches | 29% | 42% | 30% | 29% |
| letters | 16% | 26% | 15% | 17% |
| manuals | 10% | 18% | 11% | 9% |
| science | 9% | 31% | 9% | 20% |
| fiction | 8% | 12% | 8% | 6% |
| history | 7% | 15% | 7% | 6% |
| travel | 2% | 12% | 2% | 4% |

Order now plays a part on other writers, 6 to 19 points between in order and shuffled where it played none. But in-order prose rose in nine headings of ten, including travel and science: the *Origin of Species* went from 2% to 27%. That fits what the handoff warned of, a reader that picks up text holding together and not what it means. It does not prove it: that would need a text that holds together and says nothing, and none is in the test.

## Ten pages compressed to 350 words, and components defined on them, 4 November 2026, 21:30 to 21:52

His words at 21:30: "Museum texts have already been used in training. So to define components which I can check, you can make 350 word compressed versions"; at 21:32: "on the 350 word compressed versions, you will define components - I will check". `own/museum-compress.py` cut *Audience* and nine held pages drawn with seed 4 (`sources/museum/compressed.jsonl`). Between 96% and 100% of the words in each version are his, in his order (305 of 318 at the lowest, *Negotiation*). A cut keeps the words and can still lose the steps: *Negotiation* went from 763 words to 318 and lost its bridge, and the sentences that led to its ending.

All three trained readers read all ten as the good noise, in order and shuffled, 60 readings of 60, none over 512 tokens (`own/museum-compressed-read.py`, `sources/museum/read.json`). The definition, my marks and his slots are in `sources/museum/components-proposed.md`, waiting for his check. A fresh Opus reader given only the definition (`own/components-test.py`, two runs, four calls) put his pages in order at 1 in 20 of 20, and nothing else at 1 in 52 other texts. Shuffled pages went to unwanted noise 17 times in 20, against his rule, and 5 of 20 essays went to common coin, so two thresholds I wrote before running were not met. No key has come from any of this and nothing trains on it.
