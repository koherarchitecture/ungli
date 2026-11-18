# A 3B orchestrator and a system-wide router for ungli

*25 October 2026, 08:05. Internal working note beside `method-form.md`, written on Prayas's question: does ungli need a bigger model, about 3B, as an orchestrator for harder tasks like semantic search, and can each small model be linked to a system-wide router? What follows is my reading and a recommendation.* *Adopted on his word the same morning and released as ungli 1.5 (25 October 2026, 09:21), with METHOD.md edited on his word.*

## What ungli already has in place of an orchestrator

In the scaffold the orchestrator is code. `run` in `scaffold/layers.py` takes a list of layers written by people, puts the case through them in that order, stops the moment a layer answers nothing and hands the case on, and makes the top call from a table people wrote. Nothing in the order, the stopping or the hand-over is a model's. That is not an accident of the scaffold. It is METHOD.md's fifth reason for small models (*more control over the kind of logical steps performed, and over when each is performed*), and it is the public position *Knowing Why*: "The middle layer, the one that makes the actual decision, is not a model. It is code you can open, read, and challenge."

So the question is not whether ungli has an orchestrator. It has one. The question is whether that orchestrator should become a model.

## Why I think a 3B orchestrator should not be added

**It would take the step ungli keeps.** An orchestrator decides which operation runs next and when. That is exactly the control METHOD.md says small models give back, and exactly the part your 2 October rule keeps with you: the design layer (which decisions exist, what a list may hold, when a case goes to a person) is drawn by you and never handed over. A model choosing the order of layers is that design layer moved inside a model.

**Planning breaks the window, choosing does not.** If the 3B model writes a plan, sub-questions or rewritten queries, it is writing English inside the system, and the window rule refuses it. If it only returns the number of a layer from a list, it passes the window, but then it is a chooser, and a chooser over a short fixed list rarely needs 3B parameters. Either way, *orchestrator* in the usual sense, a model that plans, is outside the method.

**The harder task is usually an unnamed one.** METHOD.md's first step is to name the function of intelligence narrowly. A task that seems to need an orchestrator is often a task that has not been broken down yet, and the orchestrator would be doing step one and two for you, at run time, invisibly. Where a task cannot be broken down into operations a person can list, METHOD.md already says what that means: it is not a ungli job.

**The outside evidence leans the same way, as corroboration only.** The routing literature collected on 2 October (`[path withheld]`) finds that learned routers often fail to beat a simple baseline (Li et al., 2026, LLMRouterBench) and that a fixed assignment by kind of task recovers most of what routing gains (Lee, 2026, a single-author preprint with no holdout). Koher has also tried a model as router once: the Ideation Scaffold routed through Haiku zero-shot and was archived on 3 March 2026 with the note "Zero-shot is a prototype technique, not an architecture." These were not the reasons above; they agree with them.

## Semantic search does not need a 3B model

Semantic search sounds like the case for a bigger model, and your own measurements say otherwise. csearch is semantic search over all your writing with a 110M encoder (`bge-base-en-v1.5`) and cosine similarity, and no language model at all. On 23 September the encoder alone beat encoder plus re-ranker outright, 22 of 34 against 17, and 11 of 17 against 3 on abstractly phrased queries, so the re-ranker was removed.

In ungli's terms, semantic search is already a pointer. Its list is taken from the case (the passages of a corpus), and its answer is the number of the nearest passage, or nothing when the best score falls under a threshold set on hand-keyed cases. That passes the window exactly, and it needs an encoder, not a writer.

It would also fix a limit the README states: `pointer.py` reads only the first 380 or so tokens, and an answer past that is handed on as not found. A finder layer in front of it, the csearch encoder choosing which passage the pointer reads, lets the same 33M pointer answer *who will do it?* of a long document. That is a second layer of the same small kind, not a bigger model.

## The system-wide router: yes, as a table in code

Linking every small model to one router fits the method, provided the router is code. There are now three models built this way (rai's reader, RAM's reader and the chooser), so it is the second case that justifies generality, not anticipation. A router in ungli would be a registry written by people: each layer's name, where it runs, its list or how its list is taken from the case, and its measured threshold; and a table saying, for each kind of case, which layers run in which order and where a *don't know* goes. `run` already does this for one pipeline; the router is `run` with the table lifted out so several pipelines share the layers.

The one place a model could enter the router is when a case arrives without saying what kind it is: is this text a form answer for rai or an office note for RAM? That is a chooser over a short list of pipelines, returning a number or nothing, with *nothing* going to a person. Whether that needs 3B, or a fine-tuned 33M classifier, or no model at all because the sender already says what they are sending, is something to measure on hand-keyed cases before choosing, the way every ungli threshold is set.

## Recommendation

Do not add a 3B orchestrator. Keep orchestration in code, and build the system-wide router as a table people write. Add semantic search as a finder layer using the encoder csearch already runs, in front of the pointer. If unlabelled cases turn out to be common, add a chooser that picks the pipeline by number, and size it by measurement, starting small.

This is a recommendation, not a decision: whether ungli should ever admit a planning model is a change to the method, and the method is yours.

## A link to the animal proposal, proposed

The harmony number is already built the way this note recommends. In `splitdomaincognition/projects/animal/code/harmonious/` an open sound classifier names the source of each sound, a people guard written in code refuses an hour where people make more than a tenth of the sound, and `number.py` combines the comparisons by rules written in advance. No model decides the order or the hand-over. If ungli gains a router, the animal work is its first worked example from outside the office.

*Corrected the same day, on his word (*"it is funny you dont think any custom models are needed for semantic search"*): the semantic search section above missed that a general encoder does not know a domain's own words. ungli now adds a domain guide where needed, a small model trained for one domain that points at an entry in a glossary its people wrote; see METHOD.md and ROADMAP.md 1.9.0.*
