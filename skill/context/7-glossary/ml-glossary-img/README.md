# Figures for ml-glossary.md

Added 27 October 2026, on Prayas's word (*"update with explanatory diagrams, charts, figures and visualisations"*, then *"a lot of svgs -- every difficult concept"*). 51 SVGs, one under each entry where a picture explains more than the words. The glossary's text was not changed; a diff of every non-image line against the reviewed version is identical. The reviewed version is in `[path withheld]`.

`make.py` builds every figure; `python3 make.py`, then `md2pdf ml-glossary.md` from the folder above. Each number drawn comes from one of four places, and the figure says which:

- **Measured** (`measure.mjs` → `measured.json`, run with csearch's local `bge-base-en-v1.5`, nothing sent anywhere): the tokens, the twelve-sentence map (two flattened directions keep 32% of the differences, stated on the figure) and the *ink for the printer* search.
- **Computed** in `make.py`: gradient descent on one valley, the line and the curve through ten seeded points, the softmax at three temperatures (its four scores are made up, and the figure says so), GPT-3's parameters as 33-million squares.
- **From the glossary's own text**: rai's 64 of 96 and 0 of 72, RAM's 178 against the parser's 162, MiniLM's half size and 99%, the 380 tokens, the minus marks.
- **Drawn by hand to show an idea**, each saying so on the figure: attention, calibration, seeds, drift, the two 90%-accurate models, the three runs, the threshold's position.

Colours: terracotta, blue, amber and green, checked as a set with the dataviz validator (amber and green sit close for red-weak readers, so every group is also labelled in words).
