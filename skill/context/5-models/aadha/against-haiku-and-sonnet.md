# aadha against Haiku and Sonnet

*30 October 2026. aadha is the small model inside teetar aadhi bater; the version measured is soup i3, live since 16:54 that day.*

## The question

A chatbot can be asked to mark sentences. So why train a small model of my own for teetar aadhi bater? I put the question to a measure: the same sentences, marked by aadha and by two hosted models, Claude Haiku and Claude Sonnet.

## What the task is

aadha gives each sentence one of three marks.

- **Story**: plain writing, who did what and when. An everyday idiom is story. So is made-up writing told plainly, dialogue and impossible events included.
- **The good noise**: writing with more abstraction, layered meaning or analogy than everyday writing.
- **Unwanted noise**: gibberish, and nonsense with no meaning under it.

The animal on the page dances when about 15% of a piece is the good noise. More than 2% unwanted noise stops it, and under 5% good noise it looks sick.

## How it was measured

603 sentences, each with the mark I gave it before any model saw it: the hand-written test sets, a set of probes (second-language English, Hinglish, text typed without capitals or full stops, very short and very long sentences), and the ten test pieces. None of it is student writing.

Haiku and Sonnet were given the three marks in the words above and nothing else: no examples, no training. They answered with numbers only. aadha was given the sentences.

## The results

| | aadha | Haiku | Sonnet |
|---|---|---|---|
| all 603 sentences | **576** | 441 | 456 |
| story (328) | 324 | 325 | 316 |
| the good noise (72) | 62 | **72** | 67 |
| unwanted noise (203) | **190** | 44 | 73 |
| abstract poetic nonsense, within unwanted (149) | **141** | 4 | 30 |
| the ten test pieces, coming out as built* | 10 | 10 | 10 |

\* Three good-noise lines in the test pieces were replaced the same day with lines aadha reads correctly, so that row leans towards aadha; the hosted models came out as built on all ten anyway.

## Where aadha does better

**It holds the line I drew.** The difference is almost entirely one boundary: nonsense that sounds like poetry. Told in words that it is unwanted, Haiku still called it the good noise 101 times and Sonnet 120. *A blue arithmetic slept inside the echo of the stairs* and *Mirrors argued gently with the grammar of the floor* are the good noise to both Haiku and Sonnet, and unwanted noise to aadha. A large model finds a meaning in almost any sentence; aadha was trained on my marks, so it keeps nonsense out.

**It keeps stock idioms as story.** Sonnet read 12 story lines as noise, most of them everyday figures of speech: *The office was a furnace by two in the afternoon*, *The queue at the passport office moved like a snail*, *That form is a maze of boxes and signatures*. For aadha these are story, as I asked.

**It costs the same however many people use it.** aadha runs on my own server. A hosted model is paid per call, so its cost grows with every student.

**Students' writing stays where they put it.** A sentence goes into aadha and a number comes out; nothing is sent to a provider. The consent screen promises that what students write is kept under their login, and a provider in the middle would be a different promise.

**It cannot say anything but a mark.** aadha has no words to give. A chatbot can be told to answer with a number, but that is an instruction I would have to keep in force, not a property of the model.

**It gives the same mark every time.** The same sentence gets the same mark today and next month, which matters when testers' corrections are the record I am building.

## Where it does not

**The hosted models catch more of the good noise.** Haiku caught all 72 lines and Sonnet 67, against aadha's 62. aadha misses dry, wry claims made in plain words, such as *My thumb has signed more papers than my hand ever agreed to* and *Without the card I was a student only in my own opinion*, which both hosted models catch. Testers have since shown three more kinds aadha gets wrong: layered lines typed without capitals or full stops, very short plain sentences, and story with spelling mistakes.

## What the totals hide

Most of the 149 nonsense lines (126 of them) are in test sets written when that kind of nonsense was still the *wanted* noise, before I changed the marks on 30 October. On the sets written under the present marks alone (182 sentences), the gap narrows:

| | aadha | Haiku | Sonnet |
|---|---|---|---|
| sets keyed under the present marks (182) | **176** | 162 | 175 |
| nonsense within them (23) | **23** | 4 | 19 |

There, aadha and Sonnet are level, and both are ahead of Haiku. aadha's lead over Sonnet is a lead in kind more than in count: it is right where the line is mine, and wrong where the meaning is subtle.

## What was not tested

- Whether examples in the prompt would move Haiku and Sonnet. They were given only the definitions.
- Students' own writing. Every sentence here was written for testing.
- Larger models than Sonnet.

## Where the numbers are

`tests/hosted/hosted.py` sends the sentences; each model's marks are in `tests/hosted/`, and `tests/hosted/compare.txt` has the tables.
