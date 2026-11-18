---
title: "syntax.workshop: the models"
---

*24 October 2026. Prayas Abhinav. Also kept as a Claude doc: https://claude.ai/artifact/CyXScXJbiuwb1Pnitvab5H*

## What the models are for

syntax.workshop ships four small models (M1 to M4); a fifth (M5) was measured and not shipped. None of them writes English or corrects grammar. Each one only points at a step the writer may want to read again.

Every model keeps the same rules:

- **It runs on the phone.** The models download once (about 150 MB in all, int8) and run in the browser. Nothing is sent anywhere.
- **It reads English only.** It is given English sentences the writer typed (and, for M1, the steps), never a feeling.
- **It answers with a number or nothing.** A step number, a word number or a label number, or *null*. The sentence the writer sees is fixed text, written in advance; no model's words reach the screen.
- **No wrong point for students** (your words, 23 October 2026: *"For students - no mistakes"*). Each threshold is the one that made no wrong point on the tuning half, counted once on a held-out half. So the checks say less, and what they say has not been wrong on the cases measured.
- **Each check can be switched off** per argument, in the ⋯ menu. They are all on unless the writer turns one off.

## The list

| Model | What it answers | Built from | Size (int8) | Held-out result, no wrong point allowed |
| --- | --- | --- | --- | --- |
| **M1 carries** | Which step does this English sentence carry? | multilingual-e5-small, retrained on Hindi, Marathi, Gujarati and code-mixed pairs | 45.4 MB | Gujarati 111 of 136, Marathi 99 of 122, Hindi (through mixed) 87 of 126, mixed 82 of 119; none wrong |
| **M2 how sure** | Does this sentence sound hedged, boosted or plain? | MiniLM-L12 with a three-way head, trained | 34.3 MB | 180 of 180 right, none wrong |
| **M3 stand-in** | Which word here stands in for your chosen English word? | minilm-uncased-squad2 (a pointer), after WordNet | 34.1 MB + 1.6 MB WordNet | 38 of 94 answered with WordNet first, none wrong |
| **M4 move** | Which move does this sentence make? | MiniLM-L12 with a six-way head, trained | 34.3 MB | 131 of 270 answered, none wrong |
| **M5 sense** | Which dictionary sense does this word have here? | M1's encoder | not shipped | No round beat always choosing the first sense |

What each model reads and answers with is in its own section below.

## What each one does

### M1 carries

M1 matches English to steps. It turns each step and each English sentence into a vector and finds the step the sentence is closest to. It answers only when that step is close enough, clearly ahead of the next best, and the sentence has no number its step lacks (a guard in code, added after one Gujarati case mixed up two times).

It runs on the *Check an earlier chapter* screen. The writer pastes English written before, perhaps already polished by AI, and the screen shows: "These steps were not found anywhere in the chapter" and "These sentences match none of your steps". That shows where a polished chapter has dropped a step or added a claim the writer never made.

It is the only model that reads the writer's own language. It runs only where both counts showed no wrong point; elsewhere the screen says the check has not been measured for that language.

### M2 how sure

M2 reads one English sentence and labels it hedged, boosted or plain. Code then compares that label with the feeling the writer gave the step: only the feeling's certainty mark (sure, unsure or neither), never the feeling word itself.

On the English side it points when they disagree: "The English sounds more or less sure than you marked for this step." An *unsure* step written in confident English, or a *sure* step full of *perhaps*, is the case it catches.

### M3 stand-in

M3 runs only after a code check has found that a term's chosen English word is missing from a step's English. It asks, of each sentence, "Which words mean {your word}?" and points at one word, or none. WordNet's synonyms are tried first; M3 is asked only where WordNet finds nothing.

The screen shows: "Another word seems to stand in for your term here: … Your word: …". That catches a polished draft swapping *trace* for *evidence*.

### M4 move

M4 reads the first sentence of each step's English, with the sentence before it, and names its move: question, claim, reason, but, example or so. Code compares that with the mark the writer gave the step.

When they differ, it points: "This sentence seems to do something other than its step's mark says." A step marked *reason* whose English reads as a new claim is the case it catches.

### M5 sense (not shipped)

M5 was to pick which dictionary sense a Hindi word has in its step. No round beat always choosing the first sense, so it was not shipped. The dictionary is still there: the writer sees every entry in the dictionary's own order and picks one, or none.

## Checks that use no model

These run in plain code. They cost nothing to download and their rules can be read.

| Check | What it does | What the screen says |
| --- | --- | --- |
| **No English yet** | Lists steps whose English box is empty | "This step has no English under it yet." |
| **Chosen word missing** | For each term in a step, checks that its chosen English word (or its plural) is in the step's English | Names the missing word; M3 runs only after this |
| **Number dropped** | Finds a number in the step that its English lacks | "Your step has this number and its English does not:" |
| **More abstract than usual** | Counts abstract words in a sentence against the writer's own sentences (needs 30 of them first) | "This sentence is more abstract than your own English usually is:" |
| **No example in a long run** | Compares a run of claims and reasons with the writer's own runs (needs 10 first) | "This run of claims and reasons is longer than your own runs usually are, with no example among them" |
| **WordNet** | Synonyms of a chosen word, looked up before M3 is asked | Feeds M3's pointer |
| **Dictionary** | Wiktionary entries (Hindi 36,098 words, Marathi 5,351, Gujarati 6,941) in their own order | The writer picks an entry or none |

The two that compare with the writer's own arguments say nothing until there are enough of them. They compare a person with their own past writing, never with a norm.

## Still open

- **No human test set yet.** Every result above is on generated cases and open corpora, not on students' own writing. The human sets in the build spec still decide whether each model passes.
- **English words inside a step can pull M1 off.** On one earlier draw of Hinglish conversations, the mixed threshold made one wrong point in about 400 cases. A clean count is not a promise.
- **M1's weights and the AGPL release.** M1 was trained on IITB and Samanantar, both CC BY-NC, so whether its weights can go out with the code is not settled.
- **The interface text** in Marathi and Gujarati still needs a Marathi and a Gujarati reader, and the Hindi needs your check.
