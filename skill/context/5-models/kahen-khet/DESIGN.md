# *khet ki sune khalihan ki*: design

*Revised 3 November 2026, on his word "revise everything", to the point he gave kahen that morning. First written at 08:39 from his voice note ("a tool to communicate ... why they think a idea makes sense ... between them and their teachers using the component system designed in ada") and his instruction for a syntax tool with a small model. A proposal: every choice below is his to change, and what is my reading is marked as mine.*

## The point, in his words

*"the line is in the student's voice, it is tandem (two people and two roles both), a student getting through to a teacher and a teacher getting through to a student both are counted - no scoring, no winning or losing"*, after *"the good noise / bad noise thing is aadha's point"*.

Then his answers to three questions, the same day. Who holds which role, and who makes each mark: *"choice"*. What counts as getting through on a line: *"human explicit confirmation"*. Whether the tool is students only: *"student was example. keep other scopes open"*.

The earlier statement on the gap also stands, since he has not withdrawn it: *"the gap in meaning between the two group's components has to be recovered by the model. if there was no gap what would be the point? the gap is usually perceived to be a learning gap but sometimes it can be a point"*, and *"the gap can be the point jnot is - so the model has to figure if it is. interpretation help"*, and *"the point can be extracted from user input"*.

## What it is

Someone writes a line about why something makes sense. It may be a student with a teacher, a clerk with an officer, a patient with a doctor: the student was his example, and every such scope stays open. The two people each break that line into components, and each writes down what they gave and what they took. Neither sees the other's work until both have closed. Then the page shows what each person has explicitly confirmed got through.

Both directions are counted, as two counts. They are never added, compared or turned into a score, and the page has no winner, no loser and no standard reading of its own. A line nobody has confirmed simply is not counted, and the page does not say it failed. Where something is not confirmed, the gap may be a learning gap, or it may be the point, and the small model, `kahen`, helps work out which. It gives marks and word numbers, and never a word of its own.

## The name

**`kahen` · *khet ki sune khalihan ki*.** The saying is *kahen khet ki, sune khalihan ki*: one says field, the other hears threshing floor. Hindi dictionaries give its meaning as something said and something else understood (Hindwi gives *kahe khet ki*; a Hindi exam bank prints *kahen*, the five-letter form the family's shape needs). It has the family's shape: a five-letter model word, the public name being the rest of the saying, and the full saying printed only in the sentence that says what the tool runs on. The field and the threshing floor are on one farm, at two stages of one crop.

It names the function exactly and reaches the family's theme (a form taken from somewhere other than yourself) only in part. Other candidates, all *unsure* in repeat-reader run `0cb919ce`: `chota` · *munh badi baat*, `thali` · *ka baingan*, `andhe` · *ke haath bater*, and `kahan` · *raja bhoj kahan gangu teli*, whose butt is a caste occupation.

## The tandem

Tandem, as he defines it, is two people and two roles both. On every line there is something each person gave and something each took, so the sheet has four fields, and it runs in both directions on the same line.

| | gave | took |
|---|---|---|
| **first to second** | what the first person meant to get across in this line | what the second took from it |
| **second to first** | what the second had tried to get across, which this line answers | what the first took from the second, as this line shows it |

**The roles are a choice.** His word. Who holds which role, and who makes each mark, is chosen by the two people at the start of each sheet, and the page offers that choice in the empty state. It assumes neither.

**Getting through is a human's explicit confirmation.** His words: *"human explicit confirmation"*. So a direction counts only when a person has said so, and no model and no code ever supplies it, infers it or suggests it. An unanswered direction is not a *no*.

## The three checks

The three steps he named, with the keys replaced by getting through.

**1. Identify the components.** Each person writes a components file: three components, each one's name and what it is. Neither sees the other's until both are locked. If the teacher wrote the one file, the tool would only test whether the student had learned the teacher's definitions. Once both have marked words, code counts how often the student's component 2 fell on the same words as the teacher's components 1, 2 and 3, and shows that as a three-by-three table, so different cuts of the same line show whatever the names say.

**2. Break down into components.** On each line, each person marks the words that are each component, exactly as they stand, or `none`.

**3. Translate the mix into what was given and taken.** Each person writes what they gave and what they took, in their own words, and whoever the pair chose confirms whether it got through.

Code then reports each line by one rule, stated so anybody can contest it: the parts count as the same when, for every component, the words shared are at least half of the words either person marked. That half is a setting on the page.

| counted | how |
|---|---|
| got through, first to second | lines explicitly confirmed |
| got through, second to first | lines explicitly confirmed |
| broke the line down alike | lines whose parts count as the same |

These three stand side by side as counts of lines, with no total and no percentage of anything. Two people can break a line down alike with nothing confirmed, or confirm by different cuts, and the page shows those lines together.

## Where the lines come from

The line is in one person's voice, written by them, about why something makes sense, and pasted in so that code cuts it into lines, as aadha's page does. In his statement that voice is the student's, and he has said the student was an example. In v0.1's data it is the person a level lower, which is my reading; whose voice it takes in a real pair stays open.

**Choosing the pair and the discipline.** A pair says what kind of pair it is, typing its own if it is not listed, and a student and teacher choose a discipline the same way. The choice labels the sheet and picks the worked example they see before writing their own files. It is not given to the model, so a reading cannot lean on what a discipline or a level is assumed to think.

## The small model

**What was measured before the point changed, 3 November 2026.** A tiny reader (frozen MiniLM embeddings, a linear head, `scripts/follow.py`) can follow one person's keys from few lines: 76% on his 138 confirmed lines against 52% for the commonest key and 50% shuffled, and 79% on [name withheld]'s 38 prose lines against 45% and 33%. Following a person is not recovering a gap: on the one real pair, his keys against [name withheld]'s marks (`scripts/gap.py`), a head asked which of 38 lines part got 26, against 27 for always saying *same*. So from the sentence alone it recovered nothing, and every job below reads both people's parts and words. Those were aadha's keys, so these numbers are the record and no bar for what follows.

Two jobs are trained. A third, grouping, starts with no training. Whether something got through is not a model's job at all: it is a person's explicit confirmation, and it is an input here. An earlier version of this design trained a reader for it, and I removed that on his answer.

**Is the gap the point?** Given a line where a direction is unconfirmed or the parts differ, it returns *the point* or *not the point*. It no longer says whose, since one person's point against the other's reads as winning. *Not the point* says only that, and does not say learning gap: a gap can also be a slip or a missing choice. This is the place nearest SDC's line that verdicts stay with a person or with code a person can read. It holds because the mark is a typed value from a fixed list, shown as a reading beside the people's, and decides nothing. Whether that is enough is for him to say.

**What is the point?** It returns the first and last word numbers of a stretch of what the two people entered, on `deepset/minilm-uncased-squad2`, so it writes nothing. The page prints those words verbatim, says whose words they are as a fact of where they came from, and shows nothing below a threshold.

**Same gap elsewhere.** Given a line with a gap, it returns the numbers of other lines that part the same way, with the frozen encoder alone and no training. It groups lines and never names the group.

## The data for v0.1

Synthetic, on his words "Can this data be synthesized? I will improve", "Make enough for v 0..1" and "train v 0.1 on spark". Everything in `synth/lines/` is made up: Opus writes each line and code checks it, then a second Opus call reads it, and a line that fails is dropped. Sixteen pairs of 50 lines each. Eight are a student and teacher, by discipline: interaction design, computer science, mechanical engineering, medicine, law, commerce, history, physics. Eight are others: staff nurse and ward sister, patient and doctor, loan applicant and bank manager, city resident and municipal ward officer, client and advocate, mason and site engineer, software engineer and project manager, domestic worker and employer. All of them urban, on his word: *"only urban categories"*. Code holds this too: a line with a word such as *village*, *farmer* or *crop* is dropped, whichever pair it came from. The choice of pairs and the size are mine.

**Labels.** "S through" and "T through" stand for a confirmation the imagined people gave or did not. The point marks rest on my working rule in `synth/make.py` until `keys/components.md` is his. v0.1 trains on those on his word, and on those terms only; the next version rests on his keys.

**What was fixed on the way here.** An earlier 2,385 lines on aadha's keys are kept in `synth/aadha-keys/`. On those, the words of "said" alone predicted the point at 87% on held-out pairs against 54% for the commonest answer, because *because* and an empty "said" marked one answer. So here code sets, for every line, which marks it carries and whether *because* appears, evenly, before Opus writes a word. Bulk variants change only amounts, dates, names and the like, and add the lowercase form people type: swapping nouns took the sense out of about half the lines at every setting tried (27 to 34 of 60 marked, against 0 of 20 originals).

**Limits.** These are a model's imagination of two people, so the tests that count are whole held-out pairs now and real pairs later. The marks are mine however many rows carry them, and variants add no judgement.

## Measuring it

Each bar is set before training, and each check can fail. These measure the model, never the people, and none of these numbers reaches a page.

- **Is the gap the point?** On whole held-out pairs (law, physics, staff nurse and ward sister, client and advocate; history and mason to tune), against the commonest answer, a word count over the same input, and shuffled labels. The two errors are counted apart. *Don't know* is counted too, since a cut that says it on nearly every line would hide a reader that cannot do this.
- **What is the point?** Word overlap against a code-only route, and how often it returns words where there is no point, since a tool that always finds a point is inventing one.
- **His keys.** Then his 100 keyed lines (`keys/gap-keys.txt`), from the held-out pairs, under his own definition. That is v0.1's first real test.
- **v0.1, measured 3 November 2026, 14:15, on the Spark** (three-seed soup, 1,236 gap rows and 1,380 span rows, whole pairs held out, labels from my working rule, scores in `reader/runs/v01/`). *Is the gap the point?* got 108 of 179 held-out lines, the same as the 107 that always saying *the point* would get, against 92 for a word count and 77 for shuffled labels. So it did not clear its bar, though the word tell that inflated the earlier lines is gone. At a cut of 0.9 it answered 98 lines, 64 right; the no-wrong cut on tuning answered nothing. *What is the point?* overlapped 0.28 with the point, against 0.39 for the code-only route, and returned words on 39 of 92 lines with no point. It also failed its bar. Neither is ready to show anyone, and neither score says anything yet about his judgement, since no line has his key.
- **If it fails.** The sheets still compare without the model, and confirmations still count, but nothing then helps work out whether a gap is the point. By his sentence that would not be the tool he asked for.

## The page

Plain, in SYNTAX's look (`frontend-design-prayas-plain`). The line is drawn once with each person's parts as a band of colour on their own side, and the two directions beside it:

```
 first    ▔▔▔▔▔ 1 ▔▔▔▔  ▔▔▔▔▔▔ 2 ▔▔▔▔▔  ▔▔ 3 ▔▔       confirmed it got through
          The prototype works because people stop asking where to tap.
 second   ▁▁▁▁▁▁▁▁ 3 ▁▁▁▁▁▁  ▁▁▁ 1 ▁▁▁  ▁▁▁ 2 ▁▁▁

          got through, first to second  12   ·   got through, second to first  9   ·   broke it down alike  17
```

(The bands, the line and the counts are made up to show the layout.) The three-by-three table sits above the lines. No total, percentage, trend or comparison of the two counts appears anywhere, and no words such as *ahead*, *behind*, *gap closed* or *better*. Lines that part the same way sit together, with each person's own reading of the gap and, after those, the model's mark. The page does not call a gap a misunderstanding, a mistake or something to fix.

## What the hierarchy changes

This tool sits on a power gradient, so its safeguards are in its shape, since a norm enforces nothing:

- **Sealed by code.** The server refuses to show either person anything of the other's until both have closed. A closed sheet cannot be reopened after the reveal.
- **Nothing to win.** No score exists in the data model, so none can be shown or exported. Two people are always identifiable to each other, so each agrees to that at the start. Larger groups stay open, and any group reading would be code's plain commonest answer.
- **No marks, no assessment.** It is not to be used where one person grades the other on the result, and the page says so. With his own students, that means students he does not grade, with a consent sheet as in `grounding/SCHEME.md`, since [institution withheld] has no ethics committee.
- **Both can change it without him.** The choice of roles, components files, the overlap setting and the kinds of pair are controls on the page, there in the empty state.
- **Nothing of theirs leaves.** Local models, self-hostable, no analytics, and the pair's record deleted by the pair. Released openly, it names no institution.

**What it cannot see.** Someone lower down often confirms rather than disagree, so a confirmation can be what they expect the other wants. Sealing the sheets reduces this and does not remove it. The page has to say that a confirmation does not prove understanding, and that a gap that closes after the reveal is not evidence that something was learned, since a point can be given up under pressure as easily as a mistake can be corrected.

**One person's words.** The pair study found that a tool sitting between two people must never put one person's words to the other as theirs. Every word on the page is labelled with whose it is, in code.

## In SYNTAX

A proposal, since which syntaxes come next is his: a syntax named **tandem reading**, by its primary name, of which this tool is an instance.

| element type | need | |
|---|---|---|
| line | essential | one person's words |
| components | essential | the three named cuts each person makes |
| parts | essential | the words that are each component |
| gave | essential | what each person meant to get across |
| took | essential | what each person took from the other |
| confirmation | essential | a person saying that it got through |
| pair | optional | helps: which worked example they see |

`left_out`: who is right, any score, who won, tone, anything outside the line and whether the two people's interests are the same. `kahen` is flagged `"thing": true`: it holds no reading of its own.

## Build order

1. The v0.1 lines, then bulk variants (`synth/`).
2. v0.1 on the Spark, on his word (`reader/`).
3. He writes `keys/components.md` and keys `keys/gap-keys.txt`, blind.
4. The page, rendered at 1920 and 760, and a first real pair, for its parts and marks. Whether to ask [name withheld] or another pair is his.
5. Later, if those hold: a pointer and a chooser for text nobody has keyed, taking a person's own definition as input.

## What might connect

For him to judge. *Tandem* already stands in his canon as the tandem-and-witness rule, in *People Hold the Conversation*: is this the same tandem, and is there a witness here? The archived pair study (`koher/koher-papers/nid-shifting-paradigms/archive/pair-study/`) left one finding unsolved: with context given, private questions never took up the other person's point. His note of March 2026 (`koher/conversations/recordings/2026-03-09-voice-notes-parameterisation-gap.md:44`) has the same dispositions needing two languages depending on who speaks. *Describe, Do Not Grade*: does the other person's sealed sheet count as a real outside? His About page for aadha, quoting *Silence* on "the negative space of the expression": is what did not get through the same negative space?

Leads from one Consensus search, not yet through the citation chain and so cited nowhere as fact: Jablin 1979 on semantic-information distance between superior and subordinate; Bisel et al. 2012 on the hierarchical mum effect.

## What is his

1. **The name.** `kahen` is my pick and he has been calling the tool that; it is not yet recorded as chosen.
2. **When a gap is the point,** in `keys/components.md`. Until then those labels rest on my working rule.
3. **Whether *the point / not the point* may stay at all,** given no scoring and no winning or losing. I have kept it without *whose*, because his statement on the gap stands.
4. **The sixteen pairs, and whose voice the line takes** beyond his student example. v0.1 uses the person a level lower.
5. **What counts as user input for extracting the point:** I have read it as everything either person entered.
6. **A first real pair:** [name withheld] or another.
7. **Whose project it is:** SYNTAX's ownership is open, so neither Koher's nor SDC's rules are applied here.
