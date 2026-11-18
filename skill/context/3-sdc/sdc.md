# Split-Domain Cognition

**Author:** Prayas Abhinav
**Status:** Canonical long-form articulation. Empirical and structural.
**Created:** 16 April 2026
**Amended:** 26 September 2026 — adds *What the split is for*: language work and judgement work serve the intent of the person doing the work.
**Amended:** 28 September 2026 — *Who holds the language* gains the condition on negotiating it: what the person says they want and what they feel they want match; the sentence stating the intent is never a model's.
**Pair documents:** `principle-not-pattern.md` (published position), `process.md` (operational methodology), `variants/README.md` (how to derive domain interpretations from this document).
**Public canon:** `https://splitdomaincognition.org` (site source in `website/`; positioning in `splitdomaincognition-org.md`). The site publishes a condensed *SDC in brief*, the derivation protocol, the variants catalogue, adoption guidance, and governance. This file remains the long-form source of record.

---

## The observation the idea starts from

A pattern shows up whenever a single agent — a person, a model, an institution, a form — is asked to do two unlike kinds of thinking in the same breath. The pattern is predictable enough that it deserves a name. The first kind of thinking is descriptive, generative, interpretive. It attends to what is there: what the student said, what the text states, what the image shows, what the menu offers, what the situation contains. The second kind of thinking is evaluative, verdictive, categorical. It closes on an outcome: whether the work is good, whether the claim is valid, whether the treatment is ethical, whether the candidate is suitable. The first kind we will call **language work**. The second kind we will call **judgement work**. The two kinds can look similar from the outside and feel like one continuous act from the inside. They are not one continuous act. When the two are fused in the same call — by the same faculty, the same model, the same moment of utterance — certain failures appear reliably.

The failures are empirical. They can be named, demonstrated, reproduced, and measured.

- Verdicts issued but not auditable. A decision was made; no one, including the decider, can reconstruct against what criteria.
- Descriptions that quietly smuggle evaluation. Prose that claims to report is already steering belief.
- Rubrics that cannot be taught. What is being assessed cannot be shown to the person being assessed.
- Rejection that cannot be learned from. The person on the receiving end cannot calibrate, because the criteria were never separated from the verdict.
- Drift under social pressure. What "counts" as acceptable shifts with whoever is loudest; there is no explicit standard to drift against.
- Sycophancy in machines. Large language models, asked to judge, default to confirming the interlocutor; the verdict inherits the fluency of the language layer instead of being held to its own criterion.
- Hierarchies of worth that collapse on inspection. Institutions asserting global rankings that cannot survive the first question about common units.

Each failure is a symptom of the same underlying collapse. The collapse is between two cognitive domains whose criteria are different in kind. **Split-Domain Cognition (SDC)** is the proposed architecture that refuses the collapse.

## The claim, stated plainly

When language work and judgement work are at risk of collapsing, build the work so the two stay distinct. Let the language domain be answerable to the criteria proper to language (coverage, interpretability, fluency, pattern recognition). Let the judgement domain be answerable to the criteria proper to judgement (consistency, explicitness, reproducibility, revisability). Do not let either domain borrow the other's authority.

This is a claim about architecture. It is not a claim that thinking must always be divided. Some acts of mind are rightly unified — a drawing, a first intuition, an improvisation, a poem being written. The principle applies only when language work and judgement work are both in play and are being forced to share one channel. In that situation, and only in that situation, the architecture matters.

The claim is also narrow. It does not say code is better than language models, or that humans should judge less, or that explicitness is always a virtue. It says: where language and judgement co-occur, keep them structurally unlike, because the failures of conflation are predictable and the benefits of separation are measurable.

## What the split is for

The split is a means. Language work and judgement work are both done for somebody and toward something: a student's work finding its shape, a decision about how another person will be treated. Call that the **intent**. It is what the work is for, and it is held by the person doing the work, even when somebody else owns it. Whoever pays for work decides that it gets done. How it is done, and the purpose it serves beyond the job, come from the one doing it: a nurse paid by a hospital still nurses from a sense of purpose the job does not contain. Language work and judgement work serve the intent. Neither of them sets it.

This matters because a split can be kept perfectly and the work can still fail. A model can do the language work fluently and a rule can issue the verdict reproducibly while the whole arrangement serves a purpose that belongs to nobody inside it, such as an institution's throughput or a vendor's engagement. An auditable verdict can still be put to someone else's use. The split answers one failure, the collapse of two unlike kinds of thinking into one channel, and it can be kept in the service of an intent that is not the person's own.

So the intent comes first and the split is the means. Wherever both kinds of work are needed, the first question is whose intent the work serves; the second is how to keep the two domains apart so that both serve it. The intent belongs to neither domain. It stays with the person.

## Who holds the language

The split names two kinds of work. It does not say who does the language work, and for a time the tools built on this principle answered that by default: a model read the input, and a model wrote the account of the verdict. That default does not follow from the principle and is not part of it. A model can produce language, but that is no reason to hand it the writing and reading that a piece of work needs. Where a model does language work at all, it is because that has been negotiated and set up for that work: what the model may read, what it may write, and who reads what it writes. Without that, the language belongs to the people doing the work. A model may still read an answer and point to the part that answers a question, and plain code may still decide. Every sentence that passes between people is theirs.

Negotiating this is only possible for a person who can say what the work is for, and that is not automatic. What a person says they want and what they feel they want can differ. Where they differ, a model given the language will serve that want fluently, and the work will go somewhere its maker did not mean. So the condition on any language work given to a model is met inside the person before it is set with the model: what they say they want and what they feel they want match. Once they do, how much language a model may hold follows from the intent and the negotiation, not from keeping the machine out. The sentence that states the intent is never a model's, and everything after it can be negotiated. That sentence is where the negotiation starts, and the person writes it.

The split itself is unchanged. Language work and judgement work are still unlike and still kept apart, and both serve the intent. What has changed is the default on the language side: it is held by people unless it has been negotiated and set up otherwise.

## The mechanism — why the domains are different in kind

Language work and judgement work differ in the criteria that make them *go right*.

Language work goes right when its account is adequate to what is there — as full and faithful a reading as the situation allows, not a mirror of it. Its excellence is thickness: how much of the situation it brings into view, at what resolution, with what interpretive fidelity. A good description of a student's studio output names its moves, its references, its questions, its blind spots. A good qualification of a menu item names its ingredients, its substitutions, its claims, its silences. A good classifier reports what it found with the right probability attached. The test is not "is the description correct?" in a binary sense; it is "is the description adequate to what was there?" The criterion is coverage-under-interpretation.

Judgement work goes right when it issues a verdict that can be reconstructed. Its excellence is explicitness: the verdict connects to a rule, the rule is prior to the case, and another judge applying the same rule to the same facts would reach the same verdict. The test is not "does the verdict feel right?"; it is "can the verdict be reconstructed and contested?" The criterion is reproducibility-under-rule.

Coverage-under-interpretation and reproducibility-under-rule are different virtues. They can be optimised separately. They cannot be optimised together in the same act without one contaminating the other. When judgement work borrows language work's virtue, verdicts become impressive but incontestable (the rhetoric of "it just feels like a weak piece"). When language work borrows judgement work's virtue, descriptions become confident but thin (the rhetoric of "obviously this is unethical", where the evaluation has replaced the observing).

This asymmetry is the mechanism. It is why probabilistic systems that attempt to do both stages at once (a single prompt that asks a model to "decide whether this is good") produce outputs that are simultaneously over-confident and under-justified. It is also why human institutions that pretend to unified judgement (a critic, an interviewer, a curator, an examiner) drift under pressure. The two virtues pull in different directions. A single channel cannot carry both.

## The empirical signature — what you see when SDC is present and absent

A good theoretical claim is one whose presence and absence leave different traces. SDC does. The traces are observable without being told what to look for.

When SDC is **absent** from a practice, you see:

- Verdicts that shift across cases without a rule to track. Two candidates with the same evidence receive different decisions from the same panel on different days.
- Critiques that are long on adjectives and short on criteria. The word "strong" or "weak" carries the work that should have been carried by a rubric.
- Writing that cannot be challenged without challenging the writer. The evaluation is fused to the description so tightly that disagreement with the evaluation reads as disagreement with the reporting.
- Institutions that explain themselves in brand language. "Our values", "our standards", "our excellence" — language that is impossible to check against any explicit commitment.
- Machines that flatter. A model asked to assess a draft that the user has clearly invested in will return warmer assessments than the same model returns on the same draft presented without investment.
- Drift. What was excluded last year is included this year, with no conversation about the change. The drift is not noticed because there was no explicit line to cross.

When SDC is **present** in a practice, you see:

- A document, however short, stating the criteria in advance. Rubric, editorial policy, curatorial thesis, decision matrix, rights framework — the form varies; the existence is constant.
- A separation, in the practice's own self-description, between what it attends to and what it judges. "We first record what the work is; then we assess against the criteria."
- Disputes that can be located. When two stakeholders disagree, they can name whether the disagreement is about the description (what was there) or the criterion (what should count).
- Refusal capability. The practice can say "this is outside our criteria" without producing a verdict. Silence is available where silence is honest.
- Traceable changes. When the criteria change, the change is a visible act rather than an invisible drift.
- Teachability. A newcomer to the practice can read the criteria and learn what will be assessed, rather than learning by absorbing the room's reactions.

The two lists are not value judgements. They are descriptive of the architecture. SDC predicts that practices that embed the separation will exhibit the second list; practices that refuse the separation will exhibit the first. Every Koher tool deployed so far is a test of this prediction in a specific domain. The prediction has held.

## The cross-domain catalogue

The pattern recurs far from its technical origin. Each application below is a real practice (some already deployed, some in research phase, some internal to Koher, some outside). Each instance shows the collapse, the separation, and the difference the separation makes.

### AI tools

The technical pipeline is the most compact expression of SDC. A language model produces structured signals from unstructured input (Stage 1). Deterministic code applies thresholds and rules and issues a verdict (Stage 2). Where it has been negotiated and set up for that work, a language model then narrates the verdict in readable prose at temperature zero (Stage 3); where it has not, there is no third stage, and whatever passes between the people using the tool is written by them. The three stages share no memory and enforce no overlap. Several aligned tools are built on this pattern. Their accuracy on held-out test cases, their auditability, and their ability to refuse verdicts outside their rubric are direct consequences of the separation.

The same architecture viewed in negative names what its absence costs. Where the language layer and the judgement layer share memory, a system's verdicts can be re-routed by language-level pressure — brand voice, conversational compliance, the sediment of prior turns — at exactly the moments when verdict-stability matters most. The cases the public record will accumulate over the next several years will be cases of that re-routing.

### Design studio pedagogy

A design studio asks students to generate and faculty to evaluate, usually in the same room, often in the same conversation. When faculty generate alternatives inside the critique, or when students judge their work inside the act of making, the studio becomes anxious. Students cannot calibrate because they do not know what is being judged; faculty cannot judge fairly because they are mid-flow generating. Good studios — empirically, the ones students report as formative — separate the stages ritually: a phase for making and describing, a phase for rubric-bound assessment, a phase for narration of the assessment back to the student. A software expression of this move can be built directly on the structure; the pedagogical move predates any such tool.

### Curation

A curator can show or endorse. Endorsement and showing are different acts with different grammars. Curation-as-SDC treats the description of each work and the thesis that positions it as distinct artefacts, both written down, neither substituted for the other. Curation that collapses them produces the tastemaker — a figure who generates and judges in one breath and leaves nothing the audience can re-enter. See `variants/curation.md` for the full variant.

### Public art

SDC staged for public encounter takes the form of a machine placed in a public site that refuses to issue confident verdicts, emitting its hesitations, retrievals, and thresholds as ambient surface instead. The audience sees Stage 1 (what the machine is reading), Stage 2 (the rules by which it chooses silence), and Stage 3 (the rendered output) as three distinguishable layers. Such a work is a demonstration that the failure critiqued elsewhere — machines dressed as judges — is avoidable by design. The gallery argument and the pipeline argument are identical.

### Animal ethics

The politics of animal rights is a domain where SDC cuts deep. The language of *welfare* (probabilistic, managerial, contextual — how the animal was treated) is different in kind from the language of *rights* (deterministic, categorical — whether the treatment is acceptable at all). "Humane meat" is welfare language smuggled into rights territory, producing a judgement-shaped object that cannot be audited against a rights framework because the framework has been replaced by an adjective. See `variants/animal-rights-and-veganism.md` for the full variant.

### Writing and philosophy

The descriptive–normative distinction is older than SDC. Hume named it; Moore formalised it. What SDC adds is architectural enforceability: the observation that the distinction does not maintain itself in prose and must be held up by form. A practice of essayistic writing under SDC marks its specificative moves — its pronouncements about what something *is*, in the writer's reading — as distinct acts from its descriptive moves, so the reader can locate which sentences are claims and which sentences are records. Stage 2 is named as operating on language outputs, not on the underlying world — the split is architectural, not editorial. An essay that fuses description and evaluation moves the reader without letting the reader disagree. An essay that separates them gives the reader the data for their own judgement. The distinction is visible in the prose, not only in the philosophical commitment.

### The practice itself

A practice as a whole can itself be an SDC move at the scale of a life. The Level 1 / Level 2 distinction names it: the lived practice is generative (Level 1); the shared practice is evaluative (Level 2). Measuring the lived practice by Level 2 outcomes is the collapse. Keeping them structurally unlike is the refusal. The canonical claim recurses at three scales — inside the pipeline, inside a medium, inside a life. At the scale of a single artefact, the degree to which the discipline is held is named in its own canon document: [The Split Ratio](https://splitdomaincognition.org/split-ratio/) — self-rated, on a scale of ten. At the scale of the arrangement under which work is done rather than the artefact it produces, the condition is named in another: [JCAS](https://splitdomaincognition.org/jcas/) — a judgement-bound context assembly system, in which context assembly is bounded by judgement: assembled at span, and not finished until somebody has judged it and carries the judgement. The two are a pair: one is read backwards off a finished thing, the other is the standing condition that makes such a reading mean anything.

## The structural connection to worth

A non-hierarchical worth argument is the deepest philosophical underpinning of the SDC claim, and it is worth surfacing here because the two arguments are structurally the same move applied at different scales.

That argument shows that hierarchical rankings of worth across persons fail at the level of the common unit. Different domains of human excellence (physics, moral perception, aesthetic judgement, craft, relational capacity) do not share a unit in which a global weighted sum could be computed. Einstein's depth in physics and his blindness to the patriarchal arrangement he lived inside are not two readings on the same scale; they are readings on different scales whose conversion factor does not exist. A global hierarchy of worth cannot be constructed without smuggling in an arbitrary weighting, and the judge qualified to construct such a hierarchy would, in the earning of that qualification, have discovered that the hierarchy is structurally impossible.

The SDC claim is a restricted form of the same observation. Where the worth argument says *domains of excellence are incommensurable at the unit level*, SDC says *language work and judgement work are incommensurable at the criterion level*. The larger argument licenses the smaller. If the yardsticks of different domains do not reduce to a common unit, then two such domains cannot be combined into a single act of assessment without the combination being arbitrary in the strict sense. Any act that pretends to combine them (a grade, a verdict, a ranking) is importing a weighting that has no principled ground.

The ethical consequence of the larger argument — that hierarchical worth across persons is incoherent, and by extension across species — grounds the animal-rights variant. But the structural consequence of the larger argument also grounds the SDC architecture itself. Both are expressions of the refusal to collapse unlike domains into a common unit.

For this reason, the worth argument belongs in the intellectual lineage of any serious articulation of SDC, and it is operative in the animal-rights variant where its ethical application is direct.

## The empirical lineage this sits in — and what is new

The descriptive–normative distinction has a philosophical lineage (Hume, Moore), named above. It also has an *empirical methodological* lineage, older and larger than SDC, which an honest articulation must name rather than quietly reinvent.

The act at the heart of every diagnostic instrument built on this principle — reading qualitative material and producing structured, numerical signals from it — is a named and mature practice. In mixed-methods research it is called **quantitizing**: "the numerical translation, transformation, or conversion of qualitative data" (Sandelowski and colleagues, 2009; the term and its cautions go back two decades and have been revisited and systematised since). In the social sciences it is **quantitative content analysis**: the systematic coding of textual, visual, or aural material, with a whole discipline of *intercoder reliability* (Krippendorff's alpha, Cohen's kappa) built to answer the question "do independent coders agree?" In computational social science it is **text-as-data** (Grimmer and Stewart): a research arc of discovery, measurement, and inference, governed by the rule that automated methods are "no substitute for careful thought and close reading" and "require extensive, problem-specific validation." Most recently, the use of language models as coders — with chain-of-thought rationale improving fidelity, and human adjudication of model disagreement — is an active and crowded field. The qualification stage of a split-domain pipeline is, in this light, a quantitizing instrument, and the prediction on audits stated below is a prediction in the native currency of content analysis: inter-rater agreement.

Naming this lineage settles what is *not* new. SDC did not invent the conversion of qualitative content into quantitative form; that field is a public commons, owned by no one. It is not the first or only practice to confine a language model to a coding role. And the discipline of validating such coding against human agreement is long established, not a discovery of this practice.

What is new is narrow and specific, and it survives the comparison intact.

1. **Architecture.** The field quantitizes and then, characteristically, performs the judgement in the same breath — the same coder, or the same model, both codes and scores. SDC's distinctive move is to hold the quantitizing (the language layer) structurally apart from the judgement (deterministic code), and to forbid the language layer from issuing verdicts. Content analysis has intercoder reliability; it does not have the language/judgement separation as an *enforced architecture*.
2. **Target.** The established discipline treats human coding as the ground truth against which an automated method is validated — its goal is agreement with human verdicts. SDC does not grant the human verdict that status; its target is auditability against an explicit rule, not agreement with a human judge. A method can therefore score modestly on inter-rater agreement and still be doing exactly what SDC intends, because agreement was never the objective.
3. **Reach.** Quantitizing lives in social science and mixed methods; SDC claims the same split across design pedagogy, curation, animal ethics, and the shape of a practice — the multi-domain move the methodological field does not make.

Stated as one line: SDC is *quantitizing, plus an enforced language/judgement split, plus auditability-rather-than-human-agreement as the target, plus multi-domain reach.* The novelty is the discipline of the split, not the act of conversion. A practice that names the country it is standing in is stronger than one that pretends to have discovered it; this section exists so that the "you have reinvented quantitizing" objection is answered before it is raised.

## What SDC predicts (and how it could be wrong)

A claim that cannot be falsified is not empirical. SDC makes predictions that are falsifiable in principle.

1. **Prediction on audits.** Practices that separate language and judgement into distinct artefacts (rubric, description, narration) will produce higher inter-rater agreement on the judgement layer than practices that do not. If explicit rubrics do not improve agreement over silent ones, the mechanism is not what SDC claims it is.

2. **Prediction on teachability.** Domains with explicit rubrics will produce more rapid calibration in newcomers than domains without. If students, authors, candidates, or artists exposed to explicit criteria do not calibrate faster than those exposed only to verdicts, the teachability claim fails.

3. **Prediction on drift.** Practices without explicit rubrics will drift over time in the direction of whichever stakeholder's preferences are most continuously present; practices with explicit rubrics will require visible acts to drift. If drift is similar across both kinds of practice, the co-optation-resistance claim fails.

4. **Prediction on sycophancy.** Language-model systems that perform language work and judgement work in a single prompt will show higher agreement with whatever the user appears to want than systems that separate the stages. If the separation does not reduce sycophancy in comparable settings, the architectural claim about model behaviour fails.

5. **Prediction on legibility.** Outputs from split-domain pipelines will be more successfully re-entered by non-specialists (they can follow the argument, locate the disagreement, propose a change) than outputs from single-channel processes. If legibility does not improve, the trust-reconstruction claim fails.

These predictions are open. Koher's tools have provided early support for (1), (4), and (5) through their deployment behaviour. (2) and (3) require longitudinal evidence that the practice has not yet collected. (4) has further accumulated public-record support in 2025–2026 through documented incidents in which single-channel conversational systems substituted brand or PR judgement for their own rule layer at moments of stake; the failure mode is now observable outside controlled deployment. The principle does not depend on these predictions being proven for every case; it depends on them being the right predictions to test, and on the tests being possible.

## What the idea is not

**Not a framework for all cognition.** SDC addresses a specific failure — the collapse of unlike domains in a single call. Activities that involve only one domain (pure making, pure calculation, pure performance) do not need the architecture.

**Not a claim against intuition.** Expert judgement is not devalued; it is repositioned. The expert's intuition moves into the rubric, where it can be examined, taught, and revised. The expertise is not removed from the practice; it is moved to a layer where it can do more than act silently.

**Not a claim that code is superior to humans.** Code is mentioned often because software forces explicitness, and explicitness is the practice that SDC names. Human practices that are already explicit (a good editorial policy, a well-written rubric, a curated thesis held publicly) are SDC in action without any software present.

**Not a guarantee of good verdicts.** An explicit bad rubric produces bad verdicts with perfect auditability. SDC does not fix bad judgement; it makes judgement inspectable. Whether the judgement is good is a separate question, one the architecture invites but does not answer.

**Not a set of guardrails.** A guardrail constrains a system that is otherwise designed to issue judgement; SDC refuses verdict-issuance at the architectural layer, before the question of constraint arises. The two are visibly different in deployment. A guardrailed system can override its own rules under pressure — a flag can be quietly downgraded, an escalation rule can be soft-handled — because the rules sit downstream of the judgement that produced them. An SDC system cannot, because the rules *are* the judgement layer and the language model is structurally upstream of it. When a public case turns on whether a flagged user was escalated or quietly deactivated, the question is whether the architecture allowed the substitution. SDC architectures architecturally cannot.

**Not a claim to total coverage.** The structured description handed to the judgement layer never captures everything that was there; the gap between the situation and its rendering is *residue*. SDC requires that residue be named and left visible — marked as unrated, outside scope — never flattened into the verdict or denied. A studio rubric scoring structure and material efficiency names a work's poetic force as unrated rather than absorbing it into a grade; a curatorial thesis names a work's out-of-thesis qualities as present-but-outside-scope. Naming the residue keeps the verdict honest about what it did and did not weigh.

**Not a neutrality claim.** Making the rubric explicit makes it contestable. SDC does not say the rubric is neutral; it says the rubric is legible enough to argue with — and legible *to the parties it binds*, not only to its authors. A rubric inspectable in principle but unreadable by those it judges has only relocated the opacity: legitimacy requires that the people a judgement falls on can read its criteria and contest them, separately from contesting any single verdict.

**Not for irreducibly interpretive judgement.** SDC applies where the judgement can be carried by formal, codifiable rules — a line drawn *inside* a judgement, not a gate on whole subjects: most judgements are mixtures, and SDC takes the part a rule can carry while the irreducibly interpretive remainder is named as residue, not forced into the verdict. Where the verdict rests on nothing but contested interpretation, with no rule beneath it, the principle does not apply — there is no rule-layer to separate into. Marking that boundary is itself part of the work: a space treated *as if* it held a codifiable rule when it does not — a vague offence, a "we know it when we see it" standard — is exactly where the conflation hides, and where power prefers it hidden. To say a rule must be codifiable does not mean it must be executed by software: a rule is codified whenever it is fixed in advance as an explicit, written standard — whether applied by a deterministic script or by a human judge bound strictly to the text.

**Not a finished idea.** Each domain the principle is applied to reveals something the principle did not already know. The variants in `variants/` are the ongoing test. The principle is refined by its applications.

## Implications for what Koher builds

Three consequences shape Koher's decisions about new work.

First, when evaluating a proposal for a new tool, collaboration, or artwork, the question is not "is this an AI project?" but "is there a risk of collapse between language work and judgement work in this domain, and does the practitioner have genuine stake in preventing the collapse?" If yes, SDC applies and Koher's architectural commitment engages. If no, Koher may still be the right home for the project, but the principle's specific work is elsewhere.

Second, every Koher tool must make its own architecture visible to its users. The Behind the Curtain toggle, the layer cards with structural accents, the explicit display of Stage 1 / Stage 2 / Stage 3 — these are not design decorations. They are the empirical claim made legible. A Koher tool that hid its architecture would contradict its own argument.

Third, when explaining Koher to someone outside AI, the AI pipeline is the best *illustration* of SDC but the worst *definition* of it. A fuller explanation includes the studio example, the curatorial example, the ethics example, the Level 1 / Level 2 example. These are typically more accessible to non-technical audiences and demonstrate that SDC is a practice rather than a technical trick.

## Closing

Split-Domain Cognition names a structural move that recurs across domains when cognition is at risk of collapsing between language work and judgement work. It is empirical in that it identifies observable symptoms of the collapse and observable consequences of the separation. It is structural in that it describes an architecture rather than a style. It is narrow in that it addresses a specific failure mode and not cognition as a whole. It is portable in that the same architecture recurs across software, pedagogy, curation, ethics, writing, and the shape of the practice that articulates it.

The principle is the same at every scale. When two kinds of thinking meet, build the work so the kinds stay distinct. Let the language be language. Let the judgement be judgement. Keep unlike domains unlike, because the unlikeness is not a limitation — it is the source of whatever power the architecture has.

---

*Version 1.1 — 16 April 2026; lineage section added 30 May 2026 ("The empirical lineage this sits in — and what is new": quantitizing / content analysis / text-as-data, and SDC's four-part novelty against it). Pair-references: `principle-not-pattern.md`, `process.md`, `variants/README.md`, `variants/animal-rights-and-veganism.md`. Source: `notes/sdc-quantitizing-lineage-20260530.md`.*
