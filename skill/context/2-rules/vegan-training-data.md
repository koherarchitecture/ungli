# No model's training data needs non-vegan text

*Policy, 23 September 2026. Prayas: "make a rule for all models that none of their training data should require any non-vegan text."*

**The rule.** No text that any Koher model is trained, tuned or tested on names an animal product, and no model is designed so that its training would need such text. This covers every model, present and future: rai and the models built on it, the Coherence classifier, anything in `koher-engine-core`, and anything Koher trains for a sibling project. It covers everything that becomes training or test data: forms and their questions, fillers and templates, generated rows, held-out test answers, examples in model cards, and prompts used to generate data.

**What counts.** Food and drink from animals (milk, curd, ghee, paneer, butter, cheese, cream, eggs, meat, fish, honey and the like) and materials from animals (leather, wool, silk, pearl, ivory, gelatine, beeswax and the like), including when a word is used only as a place, a colour or a shape: a milk booth, a cream door, a stone shaped like an egg.

**Replacements are plain.** When an animal product is found, it is replaced at once with the everyday vegan thing a person would actually say: soy milk in tea, a flat oval stone, ink on paper, an off-white door. No obscure combinations picked to look varied. Removing one is a repair, not a question for Prayas.

**If a model's task cannot be trained without it**, the model is not built in that form.

**Enforced, not only written.** Each model's own checks must fail when the rule is broken. For rai this is `tests/test_vegan.py`, run by `scripts/check.sh`, which scans the forms, the data-writing scripts, the training data and every test set; proved on 23 September 2026 by planting one word and seeing the checks fail. A new model gets its own equivalent before its first training run.

**What already exists stays as it is** (Prayas, 23 September 2026: *"what is done is done"*). The rule runs forward. The published rai archives 0.3.2 and 0.3.4 are not withdrawn, and the Coherence classifier is not re-examined or retrained under it. Never propose either again.

**Scope** (Prayas, 25 October 2026: *"the vegan rule is for work I do and examples i give - ppls can do what they want"*). The rule binds his own work and the examples he gives: Koher's models, their data, and the examples in Koher's and SDC's documents. It never binds what other people train or build with Koher's methods and code, and no public text asks them to follow it. It is about animal products; a passage that describes harm to other life, such as crop advice that kills insects, names none and is not barred by it.

Ledger §206.
