# keyer

*Made 8 November 2026 on Prayas's word: "make a all-projects keying tool in which I keep pressing key and the sample keeps getting changed".*

One place to key for every project. It shows one item at a time, picked at random from what is not yet keyed, with nothing beside it: no source, no model's mark. He presses a key, it is saved, the next item appears. It runs on this machine only, sends nothing anywhere, and needs nothing installed beyond Python 3 (both machines have it).

## Run it

```
python3 [path withheld]
```

It opens http://127.0.0.1:8797 in the browser. Ctrl-C in the terminal stops it. `keyer.py <deck>` opens the page on that deck (http://127.0.0.1:8797/#<deck>), and if keyer is already running it only opens the page.

## Keys

- The deck's keys (for the Decay words: `+` or `=` for plus, `-` for minus), or click the buttons.
- If the deck has components, also the number of the component, before or after the key, or click its button. The item saves when both are marked.
- Backspace takes back the last key made in keyer. Esc clears a key not yet saved.

## Decks

`decks.json` lists them. Each names: `items` (a JSON list of objects, path relative to `personal_projects`), `field` (the one shown and keyed), `keys` (the file his keys are appended to, one JSON line each: the item, `key`, `date`, `via: "keyer"`, and `component` when given), `keys_allowed` (keyboard key → value), `components` (optional) and `rule` (one line shown under the item). The latest key for an item wins, so a sheet read in with `--read` and keys made here can share one file.

- `decay-words`: the 401 words for The Decay of Meaning (only words that carry a feeling, since 8 November 2026), 2026 edition (`prayas-games-archive/decay-of-meaning/2026-keys/`), keyed + or − only, with no component step: on his word of 8 November 2026 the components are read by Claude from his keys and written, newest first, into that folder's `components.md`, which C opens beside the item.

- `decay-rekey`: the same words' contradictions, keyed again at the end. Opens only when `decay-words` is all keyed (`after`), and shows each word's contradiction under it (`why`). Keys go to `rekeys.jsonl`.

Two optional fields in a deck: `why`, a field of each item shown under it, and `after`, a deck that must be all keyed before this one opens.

- `beam-thread`: 240 simulated moments on Beam's own mazes (`koher/tools-scratch/29-beam/keys/`, remade with `node keys/make_thread_deck.js`), each showing where the two have walked, the thread they have laid and one choice the model might make, keyed + or −. Code's read of the moment, in words, shows with the picture before he keys and is stored with the key (`reveal`). The earlier `beam-mazes` deck was removed on 9 November 2026 on his word, with none of its items keyed; its files stay in that folder.

Two more optional fields: `image`, a field holding an inline SVG shown in place of the item's name, and `route`, a field listing for every cell of that picture the next cell on the way out (or `[mouth, landing]` for a step into a tunnel), which is what a click draws, with the number of steps and tunnels on the way. `route_read`, a field listing a line of text for each number of steps, adds that line.

- `student-tool`: 32 items from `tools/coding-bench/` (16 StudentEval prompts, each answered by two coding tools with their names removed), keyed + or −. Which tool made each item stays in that folder's `deck/map.json`, and `bench.py report` joins the keys back. Do not rebuild the deck once keying has begun: keys are joined by item text. The components are read from his keys into that folder's `deck/components.md`, as for the Decay words.

- `chooser-poems` (10 November 2026): a compose deck, not one item at a time. It has `compose` (the number of words on each line, here 6, 3, 6) and `sets` (a JSON list of sets, each a list of indexes into `items`); each poem is made from the next set, shown in a shuffled order fixed for that set (alphabetically for poems 1 to 6; his word on 10 November 2026: *"shuffled"*) with no suggestions, all 1000 on screen at once (the font is sized to fit the window), and is saved to `tools/chooser/poems.jsonl` with its set's number and `"order": "shuffled"`. Punctuation marks (the deck's `marks` file, here `tools/chooser/marks.json`) stand at the head of the list and can be placed in a slot in place of a word, any number of times, and turn red and underlined once in the poem, as words do (his word: *"they can be used again but it needs to show"*); typing a mark shows it first (his word, 10 November 2026: *"allow punctuation marks to be added in place of a word"*). Type to narrow the list, Tab moves the selection through the words shown (Shift-Tab back), Enter places the selected word (bold and underlined), or click one (the words are ink blue on a paper ground, set in installed fonts so nothing is fetched; a word turns bold under the pointer and red and underlined once it is in the poem); Enter saves the full poem; Backspace in the empty box takes back the last word, or, with no word placed, opens the last saved poem to rewrite (a saved poem is never deleted: his word, 10 November 2026, *"save all edits"*, after Backspace had deleted poem 18, restored the same day from a copy); Esc clears the poem. The *Poems* button at the top opens every saved poem, newest first, with its date and set (Esc closes it), and the line under the page shows the poem just saved. Each poem in that panel has an *Edit* button (his word, 10 November 2026: *"Allow me to rewrite / edit already composed poems"*): it opens the poem with its own set of 1000; clicking a word in the poem clears that slot for a new word (Backspace clears the last word), Enter saves the poem back in place and keeps it on screen (his word, 10 November 2026: *"enter to save should stay at saved edit of poem"*), and Esc leaves it as it was (the poem stays saved; only the screen empties). ↑ and ↓ (or the *↑ earlier poem* and *↓ later poem* buttons at the top right) step to the poem before or after without changing any, and from a new, empty poem ↑ opens the last one; with changes they save the poem first (the earlier version kept under `earlier`) and then move, unless a slot is empty, when they stop and say so (his word that evening, after the arrows had refused to leave poem 13: *"I cant go to 12th poem"*) (his question, 10 November 2026: *"how do I go back to poem 5 withoout editing any in between?"*). The saved line keeps its number, set, date and marks, and gains `edited` (the date and time of the latest rewrite) and `earlier`, the poem's edit history: every previous version, oldest first, each as `{"poem", "written"}`, where `written` is when that version was saved (the poem's `date` for the first). The *Poems* panel shows each poem's earlier versions under it, newest first (his word, 10 November 2026: *"edit history for each poem saved"*). What the poems train is in `tools/chooser/README.md`.

- `coherence-v2-rests` and `coherence-v2-words` (11 November 2026): Coherence v2's two keying tasks, task 1 *why believe this?* (37 cards, keyed by the number of the sentence that says why the top sentence is true, or 0) and task 2 *words and their emoji* (136 words, keyed by the number of the emoji that fits, or 0), from `koher/tools-scratch/57-coherence-moodboard/keys/` (made by `make_decks.py`). Their shared `group` shows them as one job, with a strip at the top for moving between them. The command `coherence-keying` (his word, 11 November 2026: *"make coherence keying open with a command"*) opens keyer at the first of the two with items still to key, so task 2 opens by itself once task 1 is done; if keyer is already running it only opens the page. It is linked into `[path withheld]` on the Mac; on the ThinkPad it needs `ln -s [path withheld] [path withheld]`.

The command `poem-keying` (his word, 11 November 2026: *"open poem keying in its existing state with a command"*) opens keyer on `chooser-poems` as it stands: every saved poem, and the next set ready for the next poem. If keyer is already running it only opens the page. It is linked into `[path withheld]` on the Mac; on the ThinkPad it needs `ln -s [path withheld] [path withheld]`.

Not yet a deck: aadha's sentence keying (`syntax/…/scripts/keys.py`), because each sentence there also takes the words that are each component, which needs marking spans inside the sentence. Add it when that marking is built here.
