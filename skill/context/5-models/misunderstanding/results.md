# Misunderstanding tools: feasibility run

Run on the Spark, 3 to 4 November 2026; written 4 November 2026. Throwaway probes only: nothing was kept and no model reaches anyone. This does not count as Prayas agreeing to any source, and no label here is his key. Scripts are in `scripts/`.

Method: MiniLM (`microsoft/MiniLM-L12-H384-uncased`), 3 passes, 5e-5, batch 16, seed 7, at most 8000 training rows, against always-commonest and a word count, plus 16 rows I wrote in each tool's real setting (8 each way).

| tool | what its label says | train / test | commonest | word count | model | F1 (0 / 1) | my 16 rows |
|---|---|---|---|---|---|---|---|
| `akal` | an indirect answer means yes or no (Circa) | 8000 / 5456 | 0.539 | 0.678 | 0.829 | 0.813 / 0.843 | 11 of 16 |
| `arth` | two sentences mean the same (PAWS) | 8000 / 8000 | 0.558 | 0.509 | 0.872 | 0.883 / 0.858 | 6 of 16 |
| `saari` | the passage answers the question (SQuAD 2) | 8000 / 11873 | 0.499 | 0.507 | 0.628 | 0.493 / 0.706 | 11 of 16 |
| `rassi` | the writer meant it as sarcasm (iSarcasmEval) | 3467 / 1400 | 0.857 | 0.746 | 0.808 | 0.890 / 0.242 | 8 of 16 |
| `sawal` | the asker says the reply missed the question (Stack Exchange) | 416 / 78 | 0.500 | 0.526 | 0.500 | 0.000 / 0.667 | 10 of 16 |
| `oonth` | the asker's complaint, by a second pattern (Stack Exchange) | 92 / 14 | 0.500 | 0.643 | 0.500 | 0.667 / 0.000 | 8 of 16 |

Limits: the 16 rows are mine and few; 11 of 16 comes up about 1 time in 10 by coin toss, so it cannot show that a label travels, while 6 of 16 is still a warning for a model at 0.872 on its source. Label truth for `sawal` (about 25 of 30) and `oonth` (about 8 of 30) is my reading of a sample. `saari`'s probe used a general sequence classifier on 8000 of 130,319 rows, so it may understate what that source can do.

Licences: Circa CC BY 4.0. Stack Exchange CC BY-SA 3.0 on the April 2024 dumps. PAWS is marked `other` and has to be read. SQuAD 2 and iSarcasmEval were not checked.

Likelihoods are my estimates from the table above, not measurements. `akal` a little better than even; `saari` about 1 in 3; `sawal` about 1 in 5, and only with a larger source, which is untested; `arth` and `rassi` about 1 in 10; `oonth` next to none on this source.
