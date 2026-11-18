# ML Models Glossary

> 🔴 **The "Koher fit" recommendation for CLIP/SigLIP below was tested and did not hold (flagged 2 September 2026).** This file advises SigLIP 2 as the Stage 1 vision backbone and says it is *"preferred over CLIP for all new deployments"*. On 27 July 2026 a frozen SigLIP scoring images zero-shot against a vocabulary was measured at **79/104 = 75%** against a VLM's **97/104 = 93%** on the same 24 artefacts — it read a photograph of dense body text as *"a sparse and minimal composition"* at 0.88 confidence — and three repairs (stricter margin, deterministic cross-check, reworded poles) all failed. The encoder resizes to 224×224 and matches label strings; at that size a page of type is not type. ⚠️ **The narrow finding is against zero-shot label-matching for judging abstract properties, not against the encoder for every task** — a trained head on its embeddings, and its native joint text–image cosine, are untested rather than refuted. Do not read this banner as "SigLIP is bad". Read `tools-dev/koher-engine-core/VISION-OPEN-QUESTION.md` before choosing a vision backbone for anything.


A field reference for the koher-diagnostic agent. Use this document to recommend specific models, architectures, and deployment strategies when designing AI tool solutions for prospects.

All pricing reflects February 2026 rates. All costs in USD unless stated otherwise.

---

## Section 1: Text Classification Models (Stage 1 Candidates)

Stage 1 of the Koher architecture classifies input text against learned dimensions (e.g., "coherence between claim and evidence"). The classifier outputs severity levels per dimension. These models are the candidates for that role.

---

### DeBERTa-v3-base (Current Koher Choice)

| Attribute | Value |
|-----------|-------|
| Architecture | Disentangled attention + enhanced mask decoder, ELECTRA-style pre-training |
| Parameters | 86M backbone (128K vocabulary, ~184M total with embeddings) |
| Max sequence length | 512 tokens |
| Inference | CPU viable (moderate latency), GPU recommended for production |
| Fine-tuning GPU | Single consumer GPU (8–16 GB VRAM). ~3 epochs, lr=2e-5 |
| Typical accuracy | 90.6% on MNLI. 98.38% on Koher's 5-dimension design coherence task |
| Deploy cost | CPU: ~$0 (self-hosted). GPU: $0.50–1.00/hr on cloud |

**Why Koher chose it.** DeBERTa-v3-base hits the sweet spot: it outperforms BERT and RoBERTa on classification benchmarks while remaining small enough to fine-tune on a single consumer GPU and run inference on CPU. The disentangled attention mechanism captures nuanced semantic relationships — critical for design coherence dimensions where the difference between "good" and "adequate" is subtle. ELECTRA-style pre-training gives it stronger sample efficiency, meaning fewer training examples are needed per dimension.

**Koher fit.** The default recommendation for any text classification Stage 1 with short-to-medium inputs (<512 tokens). Start here unless there is a specific reason not to.

---

### DeBERTa-v3-large

| Attribute | Value |
|-----------|-------|
| Parameters | 178M backbone (~304M total) |
| Max sequence length | 512 tokens |
| Fine-tuning GPU | 24–48 GB VRAM (A10G, A100, RTX 4090) |
| Typical accuracy | ~86% mean accuracy on emotion classification. +8% recall over base on complex multi-category tasks |
| Deploy cost | GPU: $1.00–3.00/hr on cloud |

**When to upgrade from base.** Use DeBERTa-v3-large when:
- The classification task has many fine-grained categories (>10 dimensions)
- The domain involves ambiguous category boundaries (legal interpretation, medical diagnosis nuance)
- Base model accuracy plateaus below the client's threshold despite more training data
- The prospect has budget for GPU inference

**Koher fit.** Strong upgrade path. Recommend when base model accuracy is insufficient and the prospect's domain involves complex semantic structures. Not the default — the base model should be tried first.

---

### BERT-base / BERT-large

| Attribute | Value |
|-----------|-------|
| Parameters | 110M (base) / 340M (large) |
| Max sequence length | 512 tokens |
| Architecture | Masked language modelling, absolute positional encoding |
| Inference | CPU viable (base), GPU recommended (large) |
| Fine-tuning GPU | 8 GB (base), 24 GB (large) |
| Typical accuracy | 84–88% on standard classification benchmarks |

**When BERT is sufficient.** Use when:
- The classification task is straightforward (binary or 3–4 categories)
- Plenty of training data (>5,000 examples per class)
- Maximum compatibility is needed (BERT has the widest tooling support)
- The prospect's infrastructure already runs BERT

**Koher fit.** Acceptable baseline but DeBERTa-v3-base outperforms it on nearly every classification benchmark with comparable compute. Recommend BERT only if the prospect has existing BERT infrastructure they cannot change, or if the task is simple enough that model choice barely matters.

---

### RoBERTa-base / RoBERTa-large

| Attribute | Value |
|-----------|-------|
| Parameters | 125M (base) / 355M (large) |
| Max sequence length | 512 tokens |
| Architecture | Optimised BERT training — dynamic masking, larger mini-batches, no NSP |
| Inference | CPU viable (base), GPU recommended (large) |
| Fine-tuning GPU | 8 GB (base), 24 GB (large) |
| Typical accuracy | 1–3% improvement over BERT on most classification tasks |

**When to prefer over BERT.** Always, if starting fresh. RoBERTa's optimised training procedure produces better representations without architectural changes. The only reason to use BERT over RoBERTa is legacy compatibility.

**Koher fit.** Reasonable Stage 1 choice but still outperformed by DeBERTa-v3. Recommend when the prospect needs an established, well-understood model with slightly better performance than BERT.

---

### ALBERT

| Attribute | Value |
|-----------|-------|
| Parameters | ~12M (base) / ~18M (large) / ~60M (xxlarge) — 9x fewer than BERT-base, 18x fewer than BERT-large |
| Max sequence length | 512 tokens |
| Architecture | Factorised embedding matrix (80% parameter reduction), cross-layer parameter sharing (70% reduction), Sentence Order Prediction |
| Inference | CPU-friendly due to small size |
| Fine-tuning GPU | Single consumer GPU (4–8 GB) |
| Typical accuracy | ALBERT-xxlarge matches or exceeds BERT-large on GLUE, RACE, SQuAD |

**When to use.** Parameter-constrained environments: edge devices, mobile deployment, or when the prospect's infrastructure has strict memory limits. ALBERT trades speed for size — inference can be slower than BERT-base despite fewer parameters because of the cross-layer sharing overhead.

**Koher fit.** Niche. Use only when deployment constraints demand minimal model size (on-device, edge). For standard cloud or server deployments, DeBERTa-v3-base is better in every way.

---

### DistilBERT

| Attribute | Value |
|-----------|-------|
| Parameters | 66M (40% fewer layers than BERT-base) |
| Max sequence length | 512 tokens |
| Architecture | Knowledge distillation from BERT-base |
| Inference | 60% faster than BERT-base. CPU-optimised |
| Fine-tuning GPU | 4–8 GB |
| Typical accuracy | 86% on annotation tasks (vs BERT's 55% in some evaluations). Retains ~97% of BERT's language understanding |

**When to use.** Speed-critical deployments where latency matters more than maximum accuracy. Real-time classification in user-facing applications. Edge/mobile deployment where both speed and size matter.

**Koher fit.** Good for cost-sensitive deployments or when the prospect needs sub-50ms inference. Accept the 2–5% accuracy trade-off compared to DeBERTa-v3-base. Suitable for prototyping or when the classification task is not the bottleneck.

---

### XLNet

| Attribute | Value |
|-----------|-------|
| Parameters | 110M (base) / 340M (large) |
| Max sequence length | Theoretically unlimited (segment recurrence), practically 512–1024 tokens |
| Architecture | Permutation-based training, segment-level recurrence, relative positional encoding |
| Inference | GPU recommended. Slower than BERT due to permutation overhead |
| Fine-tuning GPU | 16 GB (base), 32+ GB (large) |
| Typical accuracy | 77–80% on bias detection. Competitive with RoBERTa on most tasks |

**When it helps.** Tasks requiring understanding of long-range dependencies within text (>256 tokens). Autoregressive modelling advantages appear in generation-adjacent tasks. In practice, DeBERTa and RoBERTa have largely superseded XLNet for pure classification.

**Koher fit.** Rarely the best choice for Stage 1. The permutation-based approach adds complexity without clear classification advantages over DeBERTa. Consider only if the prospect has existing XLNet infrastructure.

---

### ELECTRA

| Attribute | Value |
|-----------|-------|
| Parameters | 14M (small) / 110M (base) / 335M (large) |
| Max sequence length | 512 tokens |
| Architecture | Replaced token detection (discriminative pre-training) |
| Inference | CPU viable. Faster convergence during fine-tuning |
| Fine-tuning GPU | 4 GB (small), 8 GB (base), 24 GB (large) |
| Typical accuracy | Exceeds 80% on bias detection (every metric). Strong sample efficiency |

**Efficiency advantage.** ELECTRA-small matches BERT-base performance with 14M parameters. The discriminative pre-training task (detect which tokens were replaced by a generator) is more sample-efficient than masked language modelling. This means faster fine-tuning and better results with less data.

**Koher fit.** Strong alternative when training data is limited. DeBERTa-v3 actually uses ELECTRA-style pre-training, which is one reason it performs so well. If DeBERTa-v3 is unavailable or unsupported, ELECTRA-base is the next best choice.

---

### Longformer

| Attribute | Value |
|-----------|-------|
| Parameters | 149M (base) / 435M (large) |
| Max sequence length | 4,096 tokens (configurable up to 16,384) |
| Architecture | Linear attention with sliding window + global attention tokens |
| Inference | GPU required for long sequences |
| Fine-tuning GPU | 24–48 GB for sequences >2048 tokens |
| Typical accuracy | 84.7% macro-F1 on scholarly document classification, 85%+ on legal documents |

**When to use.** Documents that exceed 512 tokens: legal briefs, medical records, academic papers, contract analysis, lengthy grant proposals. The sliding window attention is linear in complexity rather than quadratic, making long documents tractable.

**Koher fit.** Essential for legal and medical domains where complete document context matters. Recommend when the prospect's inputs regularly exceed 512 tokens. Note: for documents that can be summarised or chunked, DeBERTa-v3-base with a preprocessing step may be more cost-effective.

---

### BigBird

| Attribute | Value |
|-----------|-------|
| Parameters | 128M (base) / 425M (large) |
| Max sequence length | 4,096 tokens |
| Architecture | Sparse attention — global tokens + sliding window + random attention |
| Inference | GPU required |
| Fine-tuning GPU | 24–48 GB |
| Typical accuracy | 84.3% on document classification (PubMed, arXiv) |

**When to use.** Similar use cases to Longformer. BigBird's random attention component can capture dependencies that Longformer's fixed pattern misses. Slight accuracy edge on certain biomedical datasets.

**Koher fit.** Alternative to Longformer for long documents. Choose based on domain: BigBird has strong biomedical results; Longformer has broader legal/multilingual results. Either works for Stage 1 with long inputs.

---

### ModernBERT

| Attribute | Value |
|-----------|-------|
| Parameters | 139M (base, 22 layers) / 395M (large, 28 layers) |
| Max sequence length | 8,192 tokens (16x BERT's 512) |
| Architecture | RoPE positional embeddings, GeGLU activations, Flash Attention, sequence packing, alternating attention patterns |
| Inference | 2–4x faster than previous encoders. 80% less memory than DeBERTa-v3 |
| Training data | 2 trillion tokens (web, code, scientific articles) |
| Fine-tuning GPU | 8–16 GB (base), 24 GB (large) |
| Typical accuracy | Outperforms BERT-Large and RoBERTa-Large on classification benchmarks. 3% improvement over BERT on challenging datasets |

**The 2025 contender.** ModernBERT is the strongest new entrant in the encoder model space. Its 8K context window handles documents that would require Longformer, while being significantly faster and more memory-efficient.

**Important caveat.** When controlled for training data (same dataset, same volume), DeBERTa-v3 retains superior sample efficiency and benchmark performance. ModernBERT's reported improvements partly derive from its 2T-token training corpus rather than purely architectural advantages.

**Koher fit.** Strong candidate for new deployments, particularly when:
- Inputs are 512–8,192 tokens (too long for DeBERTa, too short for Longformer)
- Inference speed and memory efficiency are priorities
- The prospect values modern, actively maintained models

For inputs under 512 tokens where maximum classification accuracy matters, DeBERTa-v3-base remains the safer choice due to proven sample efficiency.

---

### Domain-Specific Variants

#### BioBERT
- **Pre-trained on:** PubMed abstracts + PMC full-text articles (4.5B words biomedical text)
- **Strengths:** Biomedical NER (+0.62% F1 over BERT), relation extraction (+2.80% F1), biomedical QA
- **Koher fit:** Use for healthcare/medical prospects. Fine-tune BioBERT for medical coherence dimensions rather than starting from generic BERT

#### ClinicalBERT / BioClinicalBERT
- **Pre-trained on:** Clinical notes from MIMIC-III
- **Strengths:** Clinical NLP, perioperative care prediction (+20–38% AUROC over word embeddings)
- **Koher fit:** Use specifically for clinical documentation analysis. Stronger than BioBERT for clinical notes, weaker for research literature

#### MedicalBERT (2025)
- **Performance:** Outperforms BioBERT, SciBERT, and ClinicalBERT on most benchmarks. +5.67% over general BERT on average
- **Koher fit:** The strongest medical-domain encoder as of 2025. Recommend for new medical domain deployments

#### LegalBERT
- **Pre-trained on:** Legal corpora (case law, legislation, contracts)
- **Strengths:** Legal text understanding, contract clause classification, case outcome prediction
- **Koher fit:** Essential for legal domain prospects. Contract analysis, regulatory compliance, legal brief coherence — all benefit from legal pre-training

#### FinBERT
- **Pre-trained on:** Financial text (earnings calls, SEC filings, financial news)
- **Strengths:** Financial sentiment analysis, risk assessment, financial document classification
- **Koher fit:** Use for financial services prospects. Particularly valuable for thesis coherence in investment analysis

#### SciBERT
- **Pre-trained on:** 1.14M scientific papers from Semantic Scholar
- **Strengths:** Scientific text understanding, citation analysis, research paper classification
- **Koher fit:** Use for academic/research prospects. Grant proposal coherence, research paper quality assessment

**General guidance on domain variants:** Domain pre-training matters most when:
1. The domain has specialised vocabulary (medical terminology, legal citations)
2. Training data is limited (domain pre-training compensates)
3. The classification dimensions are domain-specific

If you have abundant training data (>2,000 examples per dimension) and the dimensions are generic (e.g., "argument coherence"), DeBERTa-v3-base fine-tuned on domain data often matches or exceeds domain-specific BERT variants.

---

### Multilingual Models

#### mBERT (Multilingual BERT)
| Attribute | Value |
|-----------|-------|
| Parameters | 110M |
| Languages | 104 languages including Hindi, Marathi, Gujarati |
| Typical accuracy | 92% on multilingual propaganda detection |
| Strengths | Computational efficiency, broad language coverage, solid baseline |

#### XLM-RoBERTa
| Attribute | Value |
|-----------|-------|
| Parameters | 125M (base) / 355M (large) |
| Languages | 100+ languages |
| Typical accuracy | 89–91% on multilingual tasks. Large variant outperforms base consistently |
| Strengths | Effective for low-resource languages, strong cross-lingual transfer |

**For Indian language support:** Both models support Hindi, Marathi, and Gujarati. XLM-RoBERTa-large is the stronger choice for high-accuracy requirements. mBERT is more computationally efficient for resource-constrained deployments.

**Koher fit.** Use XLM-RoBERTa-large when the prospect's documents are in Indian languages or mixed-language (Hindi-English code-switching in legal/medical contexts). For English-only domains, DeBERTa-v3-base remains superior.

---

## Section 2: Language Models for Generation (Stage 3 Candidates)

Stage 3 of the Koher architecture takes severity levels from the classifier (Stage 1) and deterministic rules (Stage 2), then generates a plain-language diagnostic narration. The model must follow structured prompts, respect the severity data it receives, and produce clear, actionable text.

---

### Claude Haiku 4.5 (Current Koher Choice)

| Attribute | Value |
|-----------|-------|
| Provider | Anthropic |
| Context window | 200K tokens |
| Pricing | $1 input / $5 output per million tokens |
| Latency | Fast — designed for high-volume, low-latency tasks |
| API | Anthropic API, AWS Bedrock, GCP Vertex AI |

**Why Koher chose it.** Stage 3 narration is a constrained generation task: the model receives structured severity data and must produce a coherent diagnosis. This does not require frontier reasoning — it requires reliable instruction-following, clear prose, and consistent formatting. Haiku 4.5 delivers all three at the lowest cost in the Claude family.

**Cost breakdown for typical Koher analysis:**
- Input: ~2,000 tokens (severity data + prompt template) = $0.002
- Output: ~500 tokens (diagnostic narration) = $0.0025
- **Per-analysis cost: ~$0.005 (half a cent)**
- Monthly at 1,000 analyses: $5
- Monthly at 10,000 analyses: $50

**Koher fit.** The default Stage 3 recommendation. Upgrade only when narration quality is insufficient.

---

### Claude Sonnet 4.5

| Attribute | Value |
|-----------|-------|
| Provider | Anthropic |
| Context window | 200K tokens (up to 1M with extended context) |
| Pricing | $3 input / $15 output per million tokens |
| Extended pricing | $6 input / $22.50 output (>200K input tokens) |
| Latency | Moderate — balanced speed and quality |
| API | Anthropic API, AWS Bedrock, GCP Vertex AI |

**When to upgrade from Haiku.** Use Sonnet when:
- The narration requires nuanced reasoning about complex severity interactions
- The prospect's domain demands higher-quality prose (e.g., client-facing legal opinions)
- The diagnostic must synthesise information across many dimensions (>10)
- Extended context is needed (documents > 200K tokens in the prompt)

**Cost at Sonnet tier:**
- Per-analysis: ~$0.01 (double Haiku)
- Monthly at 1,000 analyses: $10
- Monthly at 10,000 analyses: $100

**Koher fit.** Good upgrade for premium tiers or complex domains. 3x the cost of Haiku.

---

### Claude Opus 4 / Opus 4.5 / Opus 4.6

| Model | Pricing (input/output per 1M tokens) | Context |
|-------|---------------------------------------|---------|
| Opus 4 | $15 / $75 | 200K |
| Opus 4.5 | $5 / $25 | 200K |
| Opus 4.6 | $5 / $25 | 200K |

**When maximum quality matters.** Opus models represent frontier reasoning capability. For Stage 3 narration, this is overkill in most cases. Use when:
- The diagnostic narration must reason about novel situations not covered by prompts
- The prospect requires the highest possible quality (e.g., medical diagnostic explanations)
- The narration involves complex multi-step reasoning about dimension interactions

**Cost at Opus 4.5/4.6 tier:**
- Per-analysis: ~$0.015
- Monthly at 1,000 analyses: $15
- Monthly at 10,000 analyses: $150

**Koher fit.** Reserve for prospects who require absolute best narration quality and are willing to pay 3–5x the Haiku cost. Opus 4.5/4.6 at $5/$25 is now more accessible than the original Opus 4 pricing.

---

### Gemini 2.0 Flash

| Attribute | Value |
|-----------|-------|
| Provider | Google |
| Context window | 1M tokens |
| Pricing | $0.10 input / $0.40 output per million tokens |
| Latency | Very fast |
| API | Google AI Studio, Vertex AI |

**The cheap and fast alternative.** Gemini 2.0 Flash is 10x cheaper than Haiku on input and 12.5x cheaper on output. For simple narration tasks, it is a viable cost-reduction option.

**Cost breakdown:**
- Per-analysis: ~$0.0004 (less than a tenth of a cent)
- Monthly at 10,000 analyses: $4

**Koher fit.** Consider when cost is the primary constraint and narration quality requirements are modest. The 1M token context window is useful if the Stage 3 prompt includes extensive reference material. Test quality against Haiku before committing — Gemini's instruction-following for structured narration tasks should be validated.

---

### Gemini 2.5 Flash

| Attribute | Value |
|-----------|-------|
| Provider | Google |
| Context window | 1M tokens |
| Pricing | $0.30 input / $2.50 output per million tokens |
| API | Google AI Studio, Vertex AI |

**Mid-tier Google option.** Better reasoning than 2.0 Flash at moderate cost. Sits between Gemini 2.0 Flash and Claude Haiku on both price and capability.

**Koher fit.** Alternative to Haiku when the prospect prefers Google's ecosystem or needs the 1M context window at lower cost than Sonnet.

---

### Gemini 2.5 Pro

| Attribute | Value |
|-----------|-------|
| Provider | Google |
| Context window | 1M tokens |
| Pricing | $1.25 input / $10 output (≤200K), $2.50 input / $15 output (>200K) |
| Max output | ~65K tokens |
| API | Google AI Studio, Vertex AI |

**Google's flagship.** Strong multimodal capabilities (text, image, video, audio). Competitive with Claude Sonnet on reasoning tasks.

**Koher fit.** Consider when the prospect needs multimodal Stage 3 input (e.g., images alongside text severity data) or strong Google Cloud integration. More expensive than Haiku, comparable to Sonnet.

---

### Llama 3.3 70B

| Attribute | Value |
|-----------|-------|
| Parameters | 70B |
| Context window | 128K tokens |
| Pricing (API) | $0.20–0.89 input / $0.32–7.90 output per million tokens (varies by provider) |
| Self-hosting | Requires 2x A100 80GB or equivalent |
| Licence | Meta Community Licence (permissive for most commercial uses) |

**The open-source option.** Self-hosting eliminates per-token costs at the expense of infrastructure management. Breakeven vs Haiku API depends on volume (see Section 6).

**Koher fit.** Recommend for self-hosted deployments when:
- The prospect has existing GPU infrastructure
- Data sovereignty requirements prevent API calls to external providers
- Volume exceeds 100,000 analyses/month (self-hosting breakeven)

---

### Llama 4 Scout 17B / Maverick 17B

| Model | Parameters | Experts | Context | API Pricing (input/output) |
|-------|-----------|---------|---------|--------------------------|
| Scout | 17B | 16 | 328K | $0.08 / $0.30 |
| Maverick | 17B | 128 | 1M | $0.15 / $0.60 |

**Natively multimodal.** Llama 4 models handle text and images. MoE architecture means active parameters per inference are much lower than the total count.

**Koher fit.** Scout is an excellent low-cost API option — cheaper than Haiku with a longer context window. Test narration quality against Haiku. Maverick's 1M context window suits document-heavy domains.

---

### Mistral Small 3.1

| Attribute | Value |
|-----------|-------|
| Parameters | 24B (dense, multimodal — 12B text + 400M vision) |
| Context window | 128K tokens |
| Licence | Apache 2.0 |
| Strengths | Efficient, outperforms Llama 3.1 8B on reasoning benchmarks |

**Koher fit.** Good self-hosted option for smaller GPU setups (single A10G or RTX 4090). Apache 2.0 licence removes commercial restrictions.

---

### Mistral Large 3

| Attribute | Value |
|-----------|-------|
| Parameters | 675B (MoE) |
| Context window | 128K tokens |
| Pricing | $0.50 input / $1.50 output per million tokens |
| API | Mistral platform, various providers |

**European alternative with strong multilingual performance.** Excellent for European language domains and regulatory contexts where EU-based model provenance matters.

**Koher fit.** Competitive with Haiku on price ($0.50/$1.50 vs $1/$5). Test narration quality — Mistral Large 3 may be superior for multilingual narrations.

---

### Qwen 2.5 / Qwen 3

| Attribute | Value |
|-----------|-------|
| Languages | 100+ languages including strong Indian language support |
| Context window | Up to 131K tokens |
| Training data | Up to 18 trillion tokens |
| Pricing | $1.20–3.00 input / $4.80–15.00 output per million tokens (varies by model tier) |
| API | Alibaba Cloud, various providers |

**Multilingual strength.** Qwen models have strong coverage across Asian languages including Hindi and related Indic languages.

**Koher fit.** Consider when the Stage 3 narration must be in Hindi, Gujarati, or other Indian languages. The multilingual pre-training gives better natural language generation in these languages compared to English-centric models.

---

### Phi-4

| Attribute | Value |
|-----------|-------|
| Parameters | 14B (dense) |
| Context window | 16K tokens |
| Architecture | Optimised for reasoning on limited compute |
| Self-hosting | Single consumer GPU (RTX 3090/4090, 24 GB) |
| Strengths | Matches DeepSeek-R1 on AIME 2025. Outperforms models 5x its size on reasoning |

**The small-but-capable option.** Phi-4's reasoning performance relative to its size is remarkable. The 16K context window is a limitation.

**Koher fit.** Excellent for self-hosted Stage 3 on consumer hardware when context requirements are modest (<16K tokens). The small size means fast inference and low infrastructure cost.

---

### DeepSeek-V3 / V3.1 / V3.2

| Attribute | Value |
|-----------|-------|
| Parameters | 671–685B total (37B active per token, MoE) |
| Context window | 128–131K tokens |
| Pricing (DeepSeek API) | $0.14–0.28 input / $0.28–0.42 output per million tokens |
| Off-peak discount | 50% off (16:30–00:30 GMT) |
| Performance | Comparable to Claude Sonnet 3.5 |

**Cost-effective reasoning.** DeepSeek V3 delivers Sonnet-class performance at a fraction of the cost. The off-peak discount makes it exceptionally cheap for batch processing.

**Koher fit.** Strong Stage 3 candidate for cost-sensitive deployments. The low pricing makes it viable even for high-volume production. Caveat: evaluate data sovereignty requirements — DeepSeek's API is China-based.

---

### DeepSeek-R1

| Attribute | Value |
|-----------|-------|
| Parameters | 671B (MoE) |
| Context window | 128K tokens |
| Pricing | $0.12 input / $0.20 output per million tokens |
| Off-peak discount | 75% off |
| Performance | Comparable to OpenAI o1 on reasoning tasks |

**Reasoning-focused.** R1 excels at multi-step reasoning. For Stage 3 narration that requires complex diagnostic reasoning (not just prose generation), R1 is remarkably cheap.

**Koher fit.** Consider when the diagnostic narration involves complex reasoning chains — e.g., explaining why multiple dimensions interact to produce a particular severity pattern. At $0.12/$0.20, this is cheaper than any Claude model.

---

### Gemma 3

| Attribute | Value |
|-----------|-------|
| Parameters | 1B / 4B / 12B / 27B |
| Context window | 128K tokens |
| Pricing (API) | $0.03 input / $0.10 output per million tokens (12B) |
| Licence | Open weights |
| Strengths | Multimodal (vision), 4B model matches Gemma 2 27B on MATH/MMLU-Lite |

**Lightweight open model.** Gemma 3 12B is extremely cheap via API and runs on a single consumer GPU. The 4B variant runs on mobile hardware.

**Koher fit.** Budget-friendly Stage 3 option. The 12B model at $0.03/$0.10 is the cheapest API option covered here. Test narration quality — smaller models may produce less nuanced diagnostic language.

---

### Command R+ (Cohere)

| Attribute | Value |
|-----------|-------|
| Context window | 128K tokens |
| Pricing | $2.50 input / $10.00 output per million tokens |
| Strengths | Retrieval-augmented generation, enterprise chatbots, complex document analysis |
| API | Cohere API, AWS Bedrock |

**Retrieval-focused.** Command R+ is optimised for tasks that combine retrieval with generation — useful when Stage 3 needs to reference source documents alongside severity data.

**Koher fit.** Niche. Consider when the Stage 3 narration must cite specific passages from the analysed document. More expensive than Haiku without clear narration quality advantages for standard diagnostic output.

---

### Stage 3 Model Comparison Summary

| Model | Input / Output (per 1M tokens) | Context | Best For |
|-------|-------------------------------|---------|----------|
| Gemma 3 12B | $0.03 / $0.10 | 128K | Budget minimum |
| Gemini 2.0 Flash | $0.10 / $0.40 | 1M | Ultra-cheap with long context |
| DeepSeek-R1 | $0.12 / $0.20 | 128K | Reasoning at low cost |
| Llama 4 Scout | $0.08 / $0.30 | 328K | Cheap multimodal |
| DeepSeek-V3 | $0.14 / $0.28 | 131K | Sonnet-class at low cost |
| Gemini 2.5 Flash | $0.30 / $2.50 | 1M | Mid-tier with huge context |
| Mistral Large 3 | $0.50 / $1.50 | 128K | Multilingual, European |
| **Claude Haiku 4.5** | **$1 / $5** | **200K** | **Default Koher choice** |
| Gemini 2.5 Pro | $1.25 / $10 | 1M | Google flagship, multimodal |
| Command R+ | $2.50 / $10 | 128K | Retrieval-augmented |
| Claude Sonnet 4.5 | $3 / $15 | 200K–1M | Premium narration |
| Claude Opus 4.5/4.6 | $5 / $25 | 200K | Maximum quality |

---

## Section 3: Vision and Multimodal Models (Non-Text Domains)

When prospects deal with images, video, or mixed media (real estate photos, medical imaging, design portfolios, scanned documents), Stage 1 needs vision capabilities.

---

### CLIP / SigLIP 2

| Model | Architecture | Strengths |
|-------|-------------|-----------|
| CLIP | Contrastive vision-language pre-training | Zero-shot image classification, image-text matching, foundational model for many downstream tasks |
| SigLIP 2 | Sigmoid loss + decoder-based pretraining | Superior zero-shot classification, multilingual support, better localisation, OCR via NaFlex variant |

**CLIP** is the baseline: pre-trained on 400M image-text pairs, it maps images and text to a shared embedding space. Zero-shot classification works by comparing image embeddings against text descriptions of categories.

**SigLIP 2** (Google DeepMind, 2025) is the upgrade: better zero-shot performance, multilingual encoding, finer-grained localisation (object detection, segmentation), and the NaFlex variant preserves native aspect ratios for OCR/document tasks.

**Koher fit.** Use CLIP/SigLIP 2 as the Stage 1 vision backbone when the classification dimensions apply to images. For example: "visual coherence of a design portfolio" or "consistency between property photos and listing descriptions." SigLIP 2 is preferred over CLIP for all new deployments.

---

### Florence-2

| Attribute | Value |
|-----------|-------|
| Developer | Microsoft |
| Architecture | Vision-language model with region-level reasoning |
| Capabilities | Object detection, image captioning, segmentation, OCR, region-specific understanding |
| Parameters | Relatively compact (lightweight compared to large VLMs) |

**Koher fit.** Strong choice when Stage 1 needs to understand specific regions of an image (e.g., "is this part of the architectural drawing consistent with the specifications?"). The region-level reasoning sets it apart from CLIP's holistic image understanding.

---

### SAM 2 (Segment Anything Model 2)

| Attribute | Value |
|-----------|-------|
| Developer | Meta |
| Architecture | Unified image-video model with memory-based temporal propagation |
| Capabilities | Real-time promptable segmentation for images and video. 3 points to segment an object across an entire video |
| Training data | SA-V dataset: 51,000 videos, 600,000 masklets |

**Koher fit.** Use when the prospect needs to isolate specific objects before classification. Example: segment a product from its background before assessing design coherence. Not a classifier itself — a preprocessing tool for structured visual analysis.

---

### Multimodal API Options for Stage 3

When Stage 3 narration must reference visual inputs alongside severity data:

| Provider | Model | Vision capability | Pricing |
|----------|-------|-------------------|---------|
| Anthropic | Claude Sonnet 4.5 / Opus | Image understanding in prompts | $3–5 input / $15–25 output |
| Google | Gemini 2.5 Pro | Text + image + video + audio | $1.25 input / $10 output |
| Google | Gemini 2.0 Flash | Text + image | $0.10 input / $0.40 output |
| Meta | Llama 4 Maverick | Natively multimodal | $0.15 input / $0.60 output |

---

### YOLO v8 / v9 / v10 / v11

| Model | Key Innovation | mAP50-95 | Inference Speed | Best For |
|-------|---------------|----------|----------------|----------|
| YOLOv8 | C2f module | 59.2% | 10–20ms/frame | Small object detection, aerial imagery |
| YOLOv9 | PGI + GELAN | 69.6% | Higher latency | Highest recall, best overall detection |
| YOLOv10 | NMS-free | 58.5% | Fastest | Speed-critical, some detection inconsistencies |
| YOLO11 | 22% fewer params than v8m | 60.9% | Fast | Best speed/accuracy balance |

**Koher fit.** Use YOLO when Stage 1 needs to detect and classify objects within images (e.g., identifying design elements in architectural drawings, detecting defects in product photos). YOLO11 is the default recommendation. YOLOv8 for small object detection. YOLOv9 when recall is critical.

---

### Medical Imaging Models

#### BiomedCLIP
- **Training data:** PMC-15M (15M biomedical image-text pairs from 4.4M scientific articles)
- **Capabilities:** Zero-shot image classification, few-shot learning, medical VQA, cross-modal retrieval
- **Performance:** Outperforms general CLIP and radiology-specific models on pneumonia detection (88.8% recall)
- **Koher fit:** Use for healthcare prospects with medical imaging inputs. Foundation model for medical Stage 1

#### MedSAM / MedCLIP-SAMv2
- **Architecture:** BiomedCLIP + SAM integration
- **Capabilities:** Text-prompted medical image segmentation across multiple modalities (ultrasound, MRI, X-ray, CT)
- **Performance:** +13% Dice coefficient improvement over previous versions
- **Koher fit:** Use when Stage 1 needs to segment medical images before classification (e.g., "is this tumour boundary consistent with the radiologist's report?")

---

### Document Understanding Models

For scanned documents, forms, legal papers — where text must be extracted from images before classification.

#### LayoutLM / LayoutLMv2 / LayoutLMv3
- **Architecture:** Integrates text content with layout position embeddings
- **Strengths:** Key-value pair extraction, form field identification, document structure understanding
- **Best for:** Structured documents (forms, invoices, legal contracts with consistent formatting)

#### Donut
- **Architecture:** End-to-end OCR-free document understanding
- **Strengths:** Handles mixed printed and handwritten text, simplified pipeline (no separate OCR step)
- **Best for:** Documents with variable formatting, handwritten annotations

#### TrOCR + LayoutLM Combination
- **Architecture:** Separate OCR followed by layout-aware extraction
- **Best for:** Complex documents requiring both high-quality OCR and structural understanding

**Koher fit.** For prospects dealing with scanned documents (legal firms with paper contracts, medical practices with handwritten records):
- Simple forms: Donut (end-to-end, fewer moving parts)
- Complex structured documents: LayoutLMv3
- Mixed handwritten/printed: TrOCR + LayoutLM pipeline

These models are Stage 0 (preprocessing) — they extract structured text that then feeds into Stage 1 classification.

---

## Section 4: Embedding Models (Retrieval Components)

When the architecture includes a retrieval step before classification — e.g., "find the most relevant contract clauses before assessing coherence" — these embedding models produce the vector representations.

---

### Quick Comparison

| Model | Pricing (per 1M tokens) | Dimensions | Context | Strengths |
|-------|------------------------|------------|---------|-----------|
| text-embedding-3-small | $0.02 | 1,536 | 8K | Best cost-to-performance ratio |
| text-embedding-3-large | $0.13 | 3,072 | 8K | Highest quality (OpenAI) |
| Voyage 3.5 | $0.06 | — | 32K | Strong general-purpose, long context |
| Voyage Code 3 | $0.18 | — | 32K | Code-specialised |
| Voyage Law 2 | — | — | 32K | Legal-specialised |
| Voyage Finance 2 | $0.12 | — | 32K | Finance-specialised |
| Cohere Embed v3 | $0.10 | 1,024 | 512 | 100+ languages |
| Cohere Embed v4 | $0.12 (text), $0.47 (image) | 1,536 | — | Multimodal (text + images) |
| BGE-M3 | Free (self-hosted) | — | — | MIT licence, multilingual, multi-retrieval |
| Nomic Embed v1.5 | Free (self-hosted) | — | 8K | Open-source, outperforms OpenAI on some tasks |
| Nomic Embed Text V2 | Free (self-hosted) | — | — | MoE architecture, ~100 languages |
| E5-Mistral-7B | Free (self-hosted) | — | — | 82–90% Top-5 accuracy in RAG benchmarks |
| GTE | Free (self-hosted) | — | — | Multilingual, good for RAG |
| Jina Embeddings v3 | — | — | 8K | Long context (underperforms on ranking) |

---

### Detailed Assessments

**text-embedding-3-small (OpenAI):** The default API embedding model for most use cases. At $0.02/M tokens, it is cheap enough to embed entire document corpora. 48.6% relevance score in benchmarks — identifies general information areas well. Batch API halves the cost to $0.01/M tokens.

**text-embedding-3-large (OpenAI):** Use when semantic precision is critical — legal document retrieval, research paper matching. 3,072 dimensions provide finer-grained representation. 6.5x the cost of small.

**Voyage AI:** Domain-specialised embeddings are Voyage's differentiator. Voyage Law 2 for legal retrieval, Voyage Finance 2 for financial document search, Voyage Code 3 for code retrieval. The 32K context window handles longer documents without chunking. Voyage 4 models (January 2026) are the newest, pricing details still emerging.

**Cohere Embed v3/v4:** Strongest multilingual coverage (100+ languages). Embed v4 adds image embedding — useful when retrieval spans both text and images. Competitive pricing at $0.10–0.12/M tokens.

**BGE-M3 (BAAI):** Best open-source option. MIT licence, self-hosted, no per-query cost. Supports multiple retrieval methods. Production-ready. Trades setup complexity for cost elimination at scale.

**Nomic Embed:** Open-source, performant, free. ModernBERT-based architecture. The MoE variant (Text V2) covers ~100 languages.

**E5-Mistral-7B:** 7B parameters make it the largest embedding model listed — and the most expensive to self-host. 82–90% Top-5 accuracy is strong, but the 7B parameter count means GPU-only deployment.

**Jina Embeddings v3:** Long context support is the selling point. However, recent benchmarks show it underperforming competitors on ranking quality. Use only if long-context embedding is the specific requirement.

---

### Koher Fit Guidance for Embeddings

**Most deployments do not need embeddings.** Koher's default architecture (classifier + rules + narration) operates without a retrieval step. Embeddings become relevant when:

1. The input corpus is large and the classifier needs to find relevant sections first (legal discovery, research paper corpus analysis)
2. The prospect wants "find similar documents" functionality alongside quality classification
3. The architecture includes RAG — retrieval-augmented generation for Stage 3 narration

**Default recommendation:** text-embedding-3-small for API-based retrieval. BGE-M3 for self-hosted. Voyage specialised models for legal/financial domains.

---

## Section 5: Fine-Tuning Approaches

How to adapt models for Koher-style dimension classification.

---

### Full Fine-Tuning

**What it is.** Update all model parameters on your training data.

**When to use:**
- Small models (DeBERTa-v3-base, ELECTRA, DistilBERT) — full fine-tuning is affordable and effective
- Highly specialised tasks where the domain differs significantly from pre-training data
- Maximum accuracy is the goal and compute is available

**Requirements:**
- GPU memory proportional to model size (8 GB for DeBERTa-base, 48 GB for large models)
- Training time: 1–3 epochs typical, 30 minutes to 4 hours depending on dataset size
- Risk of catastrophic forgetting if not careful with learning rate (use 1e-5 to 3e-5)

**Koher recommendation.** Full fine-tuning is the default for Stage 1 classifiers. DeBERTa-v3-base is small enough that full fine-tuning is straightforward and yields the best results.

---

### LoRA (Low-Rank Adaptation)

**What it is.** Train small low-rank adapter matrices that modify the attention layers, while freezing the base model. Reduces trainable parameters by 10–100x.

**When to use:**
- Medium to large models (>1B parameters) where full fine-tuning exceeds GPU memory
- Multi-task scenarios where you need different adapters for different prospects (swap adapters, keep base model)
- Rapid iteration — LoRA fine-tuning is faster than full fine-tuning

**Requirements:**
- 24–48 GB VRAM for large models (vs 80+ GB for full fine-tuning)
- Start with rank 8 or 16, benchmark before scaling up
- Near-identical accuracy to full fine-tuning on most tasks

**Koher recommendation.** Use LoRA when fine-tuning LLMs for specialised Stage 3 narration, or when adapting large models (DeBERTa-v3-large, RoBERTa-large) with limited GPU access.

---

### QLoRA (Quantised LoRA)

**What it is.** LoRA + 4-bit quantisation of the frozen base model. 75% memory savings compared to naive fine-tuning.

**When to use:**
- Very large models (30B+ parameters) on consumer hardware
- Fine-tuning a 65B model on a single 48 GB GPU
- Budget-constrained deployments where GPU rental is minimised

**Performance:** Within ~0.5 points of full fine-tuning accuracy on most benchmarks.

**Koher recommendation.** Use when fine-tuning Llama 3.3 70B or similar for self-hosted Stage 3. The memory savings make large-model fine-tuning accessible on rental GPUs.

---

### Adapters (Houlsby, Pfeiffer)

**What it is.** Small trainable modules inserted between transformer layers. Unlike LoRA (which modifies attention), adapters add new computation paths.

**When to use:**
- Multi-task or continual learning where isolating task-specific parameters prevents interference
- Multiple prospects sharing the same base model with different adapter modules
- When catastrophic forgetting between tasks is a concern

**Koher recommendation.** Consider for a multi-tenant deployment where each prospect has different dimensions but shares the same base classifier. Each prospect's adapter encodes their domain-specific dimensions.

---

### Prompt Tuning / P-Tuning

**What it is.** Learn a small set of soft prompt embeddings prepended to the input. The model backbone is completely frozen. P-tuning v2 inserts trainable tokens at every layer.

**When to use:**
- When the base model cannot be modified at all (API access only, or shared infrastructure)
- LLM-based classifiers where you want to adapt behaviour through learned prompts
- Only ~2% additional parameters required

**Limitations:**
- Performance plateaus when prompt length exceeds certain thresholds
- Requires exponentially many tokens for memorising arbitrary datasets
- Generally weaker than LoRA for classification tasks

**Koher recommendation.** Niche. Prefer LoRA or full fine-tuning for Stage 1 classifiers. Prompt tuning is more relevant for adapting Stage 3 LLMs when fine-tuning is not possible.

---

### SetFit (Few-Shot Classification)

**What it is.** Few-shot fine-tuning framework for classification using Sentence Transformers. Generates training pairs through contrastive learning.

**Key advantage: 8 labelled examples per class** achieves competitive performance with models fine-tuned on 3,000+ examples.

**Performance:**
- Outperforms GPT-3 on 7 of 11 classification tasks while being 1,600x smaller
- AUC of 0.865 on security bug report identification with limited data
- No handcrafted prompts or verbalizers needed

**When to use:**
- Early-stage prospect engagement: "Can we build a prototype with the 50 examples you have?"
- Domain where labelled data is expensive (medical, legal — expert annotation costs)
- Rapid proof-of-concept before investing in full training data collection

**Koher recommendation.** Extremely valuable for prospect demonstrations. When a prospect asks "will this work for my domain?", SetFit can produce a working prototype with minimal labelled examples. Transition to full fine-tuning (DeBERTa-v3-base) once sufficient training data is collected.

---

### Training Data Requirements

| Data per dimension | Expected result | Context |
|-------------------|-----------------|---------|
| 8–20 examples | SetFit prototype. Demonstrates feasibility | Prospect demo, proof-of-concept |
| 50–100 examples | Rough classifier. Identifies major patterns | Early development, hypothesis testing |
| 200–500 examples | Reasonable classifier. ~85–90% accuracy | Minimum for production consideration |
| 500–2,000 examples | Strong classifier. ~90–95% accuracy | Production-ready for most domains |
| 2,000–5,000 examples | High-accuracy classifier. ~95–98% accuracy | Refined production, complex dimensions |
| 5,000+ examples | Diminishing returns unless dimensions are very nuanced | Complex domains (legal, medical) |

**Koher achieved 98.38% accuracy with ~5,600 training examples across 5 dimensions** (~1,120 per dimension average).

---

### Evaluation Methodology

**Train/val/test splits:** 70/15/15 or 80/10/10. Never evaluate on training data.

**Cross-validation:** 5-fold cross-validation when dataset is small (<1,000 total examples). Ensures results are not dependent on a lucky split.

**Per-dimension metrics:** Report accuracy, precision, recall, and F1 for each dimension independently. Overall accuracy can mask poor performance on individual dimensions.

**Confusion matrix:** Essential for understanding where the classifier fails. Are errors between adjacent severity levels (3 vs 4) or catastrophic (1 vs 5)?

**Calibration:** Check that confidence scores correlate with actual accuracy. A classifier that says "95% confident" should be right 95% of the time.

---

## Section 6: Deployment Options

---

### API-Based (No Infrastructure)

| Provider | Models Available | Pricing Model | Strengths |
|----------|-----------------|---------------|-----------|
| **Anthropic API** | Claude family | Per-token | Direct access, best Claude performance |
| **Google AI Studio** | Gemini family | Per-token | Free tier available, 1M context |
| **AWS Bedrock** | Claude, Llama, Mistral, Cohere | Per-token | AWS integration, Indian region (Mumbai) |
| **GCP Vertex AI** | Gemini, Claude, Llama | Per-token | Google Cloud integration, Mumbai region |
| **Azure AI** | Llama, Mistral, Phi, Cohere | Per-token | Azure integration, Central India region |
| **OpenRouter** | 300+ models | Per-token + 5.5% fee | Multi-model access, unified API |
| **Together AI** | Open-source models | Per-token | Competitive open-source pricing |
| **Fireworks AI** | Open-source models | Per-token (tiered by params) | Lowest baseline rates for small models |
| **Replicate** | Open-source models | Per-second (hardware) | Pay for compute time, not tokens |
| **DeepSeek API** | DeepSeek V3, R1 | Per-token | Extremely cheap, off-peak discounts |

**For Indian prospects:** AWS Bedrock (Mumbai region), GCP Vertex AI (Mumbai region), and Azure AI (Central India region) offer the lowest latency from India. Anthropic API and Google AI Studio route through US/EU regions — expect 100–300ms additional latency.

---

### Self-Hosted Options

| Framework | Best For | GPU Required | Throughput | Setup Complexity |
|-----------|---------|-------------|------------|-----------------|
| **vLLM** | Production, high-throughput | Yes (A10G+) | 35x+ over llama.cpp at scale | Medium |
| **TGI (Text Generation Inference)** | Enterprise, monitoring | Yes (A10G+) | High | Medium-High |
| **Ollama** | Development, prototyping | Optional (GPU accelerated) | Limited | Very Low |
| **llama.cpp** | CPU-only, edge | No (CPU viable) | 8–15 tok/sec single request | Medium |

**vLLM** is the production standard. PagedAttention memory management, distributed inference, near-instantaneous time-to-first-token. Use for any production self-hosted deployment.

**Ollama** is for prototyping. Single-command setup, but limited throughput and no production monitoring. Start here, migrate to vLLM when ready.

**llama.cpp** is for CPU-only. A 13B model runs in 8 GB RAM with 4-bit quantisation. Single-user only — not suitable for multi-user production.

**TGI** is for enterprise. Prometheus/Grafana integration, guided generation, grammar constraints. Choose when observability and enterprise features matter.

---

### Edge Deployment

| Runtime | Hardware | Strengths | Use Case |
|---------|----------|-----------|----------|
| **ONNX Runtime** | CPU, GPU, accelerators | Cross-platform, hardware-agnostic | Heterogeneous edge deployments |
| **TensorRT** | NVIDIA GPUs only | Best latency/throughput on NVIDIA | NVIDIA-centric deployments |
| **Core ML** | Apple Silicon | iOS/macOS native | Apple device deployment |
| **ONNX + TensorRT** | NVIDIA GPUs | 50% faster than DirectML | Windows/RTX deployment |

**For Stage 1 classifiers:** Export DeBERTa-v3-base to ONNX format, quantise to INT8, deploy via ONNX Runtime. This enables CPU inference at <50ms per classification on modern hardware.

**Quantisation guidance:**
- FP16: Minimal accuracy loss, 2x speed improvement
- INT8: ~0.5% accuracy loss, 4x speed improvement
- INT4/2-bit: Noticeable accuracy loss, use only for edge with severe constraints

---

### Indian Cloud Options

| Provider | Region | GPU Options | Hourly Cost (Entry) |
|----------|--------|-------------|-------------------|
| **AWS Mumbai** | ap-south-1 | g5.xlarge (A10G) | $1.006/hr |
| **GCP Mumbai** | asia-south1 | L4 (24 GB) | ₹60.74/hr (~$0.73) |
| **GCP Mumbai** | asia-south1 | A100 80 GB | ₹491.53/hr (~$5.90) |
| **Azure Central India** | centralindia | Various | Varies |
| **AceCloud (Indian)** | India | H100 clusters | ~60% cheaper than AWS/GCP |

**For Stage 1 classifier hosting:** A single g5.xlarge (AWS) or L4 (GCP) is sufficient for DeBERTa-v3-base inference. Cost: $0.73–1.00/hr, or ~$530–720/month for always-on.

**For self-hosted Stage 3:** Llama 3.3 70B requires 2x A100 80 GB. Monthly cost: ~$8,500 on GCP Mumbai. Consider AceCloud for significant savings.

---

### Cost Comparison: API vs Self-Hosted Breakeven

**Stage 3 (Language Model) Breakeven Analysis:**

Assumptions: Claude Haiku 4.5 at $1/$5 per 1M tokens, ~2,500 tokens per analysis (input + output).

| Monthly Analyses | API Cost (Haiku) | Self-Hosted Cost (Llama 70B on 2xA100) | Winner |
|-----------------|-----------------|---------------------------------------|--------|
| 1,000 | $5 | ~$8,500 | API |
| 10,000 | $50 | ~$8,500 | API |
| 100,000 | $500 | ~$8,500 | API |
| 500,000 | $2,500 | ~$8,500 | Self-hosted |
| 1,000,000 | $5,000 | ~$8,500 | Self-hosted |

**Breakeven: ~340,000 analyses/month** with Haiku pricing. Below that volume, API is cheaper.

With cheaper API models (Gemini 2.0 Flash, DeepSeek), breakeven shifts much higher — potentially 2M+ analyses/month.

**Stage 1 (Classifier) Breakeven:**

DeBERTa-v3-base runs on CPU. Self-hosting on a $50/month VPS handles thousands of classifications per day. API-based classification (via Hugging Face Inference API or similar) costs ~$0.001 per classification.

| Monthly Analyses | API Cost | Self-Hosted VPS | Winner |
|-----------------|---------|----------------|--------|
| 1,000 | $1 | $50 | API |
| 10,000 | $10 | $50 | API |
| 100,000 | $100 | $50 | Self-hosted |

**Breakeven: ~50,000 analyses/month** for classifier self-hosting.

---

## Section 7: Model Selection Decision Trees

### Stage 1 Classifier Selection

```
What is the input type?
│
├── TEXT ONLY
│   │
│   ├── Input length?
│   │   ├── Short (<512 tokens)
│   │   │   ├── Language?
│   │   │   │   ├── English → DeBERTa-v3-base (DEFAULT)
│   │   │   │   ├── Indian languages → XLM-RoBERTa-large
│   │   │   │   └── Multiple languages → XLM-RoBERTa-large
│   │   │   │
│   │   │   └── Domain-specific vocabulary?
│   │   │       ├── Medical → MedicalBERT or BioBERT → fine-tune
│   │   │       ├── Legal → LegalBERT → fine-tune
│   │   │       ├── Financial → FinBERT → fine-tune
│   │   │       ├── Scientific → SciBERT → fine-tune
│   │   │       └── General → DeBERTa-v3-base → fine-tune
│   │   │
│   │   ├── Medium (512–8,192 tokens) → ModernBERT-base
│   │   │
│   │   └── Long (>8,192 tokens) → Longformer or BigBird
│   │       ├── Legal documents → Longformer
│   │       └── Medical/scientific → BigBird
│   │
│   └── Accuracy insufficient with base model?
│       ├── Try DeBERTa-v3-large
│       ├── Still insufficient? → More training data or dimension redesign
│       └── Edge/mobile deployment? → DistilBERT or ALBERT
│
├── IMAGES
│   ├── Zero-shot (no training data) → SigLIP 2 or CLIP
│   ├── Object detection needed → YOLO11 (default) or YOLOv8 (small objects)
│   ├── Medical images → BiomedCLIP
│   └── Image + text matching → SigLIP 2
│
├── SCANNED DOCUMENTS
│   ├── Structured forms → LayoutLMv3
│   ├── Mixed handwritten/printed → Donut or TrOCR + LayoutLM
│   └── Simple OCR then classify → Extract text → route to TEXT ONLY
│
└── MIXED TEXT + IMAGES
    ├── API-based → Gemini 2.5 Pro or Claude Sonnet (vision)
    └── Self-hosted → Llama 4 Maverick (natively multimodal)
```

### Stage 3 Language Model Selection

```
What matters most?
│
├── COST (lowest possible)
│   ├── API acceptable? → Gemma 3 12B ($0.03/$0.10) or Gemini 2.0 Flash ($0.10/$0.40)
│   └── Self-hosted? → Phi-4 14B (single consumer GPU)
│
├── QUALITY (best narration)
│   ├── Budget allows $5/$25? → Claude Opus 4.5/4.6
│   ├── Budget allows $3/$15? → Claude Sonnet 4.5
│   └── Budget allows $1/$5? → Claude Haiku 4.5 (DEFAULT)
│
├── REASONING (complex diagnostics)
│   ├── API acceptable? → DeepSeek-R1 ($0.12/$0.20) — best reasoning per dollar
│   └── Self-hosted? → Llama 3.3 70B with QLoRA fine-tuning
│
├── MULTILINGUAL (Indian languages)
│   ├── Hindi/Gujarati narration → Qwen 2.5 or Mistral Large 3
│   └── Code-switched text → XLM-RoBERTa embedding + multilingual LLM
│
├── DATA SOVEREIGNTY (no external API)
│   ├── GPU available? → vLLM + Llama 3.3 70B or Mistral Large 3
│   └── CPU only? → llama.cpp + Phi-4 14B (quantised)
│
├── LONG CONTEXT (>200K tokens)
│   ├── Budget allows? → Gemini 2.5 Pro (1M context, $1.25/$10)
│   └── Cost-sensitive? → Gemini 2.0 Flash (1M context, $0.10/$0.40)
│
└── RETRIEVAL-AUGMENTED
    └── Document citation needed → Command R+ or RAG pipeline with embeddings
```

### Deployment Decision

```
Monthly analysis volume?
│
├── <1,000 → API only (any provider)
│   └── Recommend: Haiku for quality, Gemini 2.0 Flash for cost
│
├── 1,000–50,000 → API for Stage 3, consider self-hosted Stage 1
│   └── Stage 1: VPS with DeBERTa on CPU ($50/month)
│   └── Stage 3: Haiku API ($5–50/month)
│
├── 50,000–340,000 → Self-hosted Stage 1, API for Stage 3
│   └── Stage 1: Dedicated GPU instance
│   └── Stage 3: Haiku API ($50–$500/month) — still cheaper than self-hosted LLM
│
└── >340,000 → Self-hosted everything
    └── Stage 1: GPU cluster
    └── Stage 3: vLLM + Llama 70B on 2xA100
```

---

## Section 8: Cost Estimation Templates

### Pattern 1: Text Classification + Haiku Narration (Current Koher Pattern)

The baseline Koher architecture.

**Components:**
- Stage 1: DeBERTa-v3-base (self-hosted on CPU or inference API)
- Stage 2: Deterministic rules (negligible compute cost)
- Stage 3: Claude Haiku 4.5 via API

**Per-analysis cost:**
- Stage 1: ~$0.001 (inference API) or ~$0.0001 (self-hosted CPU)
- Stage 3: ~$0.005 (2K input tokens + 500 output tokens)
- **Total: ~$0.005–0.006 per analysis**

| Monthly Volume | Stage 1 (API) | Stage 3 (Haiku) | Total |
|---------------|--------------|-----------------|-------|
| 100 | $0.10 | $0.50 | $0.60 |
| 1,000 | $1.00 | $5.00 | $6.00 |
| 10,000 | $10.00 | $50.00 | $60.00 |
| 100,000 | $100.00 | $500.00 | $600.00 |

---

### Pattern 2: Text Classification + Self-Hosted Narration (Cost-Optimised)

For cost-sensitive prospects or those requiring data sovereignty.

**Components:**
- Stage 1: DeBERTa-v3-base on VPS CPU ($50/month)
- Stage 2: Deterministic rules (same VPS)
- Stage 3: Phi-4 14B on consumer GPU ($200/month rental) or Llama 70B on 2xA100 ($8,500/month)

**Phi-4 deployment (budget):**

| Monthly Volume | Stage 1 (VPS) | Stage 3 (GPU rental) | Total |
|---------------|--------------|---------------------|-------|
| 100 | $50 | $200 | $250 |
| 1,000 | $50 | $200 | $250 |
| 10,000 | $50 | $200 | $250 |
| 100,000 | $50 | $200 | $250 |

Fixed cost regardless of volume. Breaks even with Pattern 1 at ~4,200 analyses/month.

**Llama 70B deployment (quality):**

Fixed cost ~$8,550/month. Breaks even with Pattern 1 at ~142,500 analyses/month.

---

### Pattern 3: Long Document Classification + API Narration (Legal/Medical)

For prospects with documents exceeding 512 tokens.

**Components:**
- Stage 1: Longformer-base on GPU ($1.00/hr, ~$720/month)
- Stage 2: Deterministic rules
- Stage 3: Claude Sonnet 4.5 (higher quality for professional output)

**Per-analysis cost:**
- Stage 1: ~$0.005 (GPU inference for long documents)
- Stage 3: ~$0.015 (3K input tokens + 800 output tokens at Sonnet rates)
- **Total: ~$0.02 per analysis**

| Monthly Volume | Stage 1 (GPU) | Stage 3 (Sonnet) | Total |
|---------------|--------------|-----------------|-------|
| 100 | $720 | $1.50 | $722 |
| 1,000 | $720 | $15.00 | $735 |
| 10,000 | $720 | $150.00 | $870 |

Stage 1 GPU is the dominant cost at low volumes. Consider batch processing (spin up GPU only when needed) to reduce to ~$0.01 per analysis for the GPU component.

---

### Pattern 4: Multimodal Classification + API Narration (Real Estate/Design)

For prospects whose inputs include images alongside text.

**Components:**
- Stage 1: SigLIP 2 for image embeddings + DeBERTa-v3-base for text → fused classification
- Stage 2: Deterministic rules
- Stage 3: Gemini 2.5 Pro (multimodal, can reference images in narration)

**Per-analysis cost:**
- Stage 1: ~$0.01 (image processing + text classification)
- Stage 3: ~$0.02 (image + text input at Gemini Pro rates)
- **Total: ~$0.03 per analysis**

| Monthly Volume | Stage 1 | Stage 3 (Gemini Pro) | Total |
|---------------|---------|---------------------|-------|
| 100 | $1 | $2 | $3 |
| 1,000 | $10 | $20 | $30 |
| 10,000 | $100 | $200 | $300 |

---

### Cost Summary Across Patterns

| Pattern | Per Analysis | 1K/month | 10K/month | Description |
|---------|-------------|----------|-----------|-------------|
| 1. Text + Haiku | $0.006 | $6 | $60 | Default Koher |
| 2. Text + Self-Hosted | $0.003* | $250** | $250** | Fixed cost |
| 3. Long Doc + Sonnet | $0.02 | $735 | $870 | Legal/Medical |
| 4. Multimodal + Gemini | $0.03 | $30 | $300 | Real Estate/Design |

*At scale (amortised fixed cost). **Fixed monthly regardless of volume.

---

## Appendix: Model Parameter Quick Reference

### Encoder Models (Stage 1)

| Model | Parameters | Max Tokens | GPU Required |
|-------|-----------|-----------|-------------|
| DistilBERT | 66M | 512 | No |
| ALBERT-base | 12M | 512 | No |
| ELECTRA-small | 14M | 512 | No |
| ELECTRA-base | 110M | 512 | No |
| BERT-base | 110M | 512 | No |
| DeBERTa-v3-base | 86M | 512 | No* |
| RoBERTa-base | 125M | 512 | No |
| XLM-RoBERTa-base | 125M | 512 | No |
| ModernBERT-base | 139M | 8,192 | No* |
| Longformer-base | 149M | 4,096 | Yes |
| BigBird-base | 128M | 4,096 | Yes |
| DeBERTa-v3-large | 178M | 512 | Yes |
| BERT-large | 340M | 512 | Yes |
| RoBERTa-large | 355M | 512 | Yes |
| XLM-RoBERTa-large | 355M | 512 | Yes |
| ModernBERT-large | 395M | 8,192 | Yes |

*CPU inference is viable but slower. GPU recommended for production throughput.

### Language Models (Stage 3)

| Model | Parameters | Context | Self-Hostable |
|-------|-----------|---------|---------------|
| Phi-4 | 14B | 16K | Yes (1x consumer GPU) |
| Gemma 3 12B | 12B | 128K | Yes (1x consumer GPU) |
| Llama 4 Scout | 17B MoE | 328K | Yes (1x A10G) |
| Mistral Small 3.1 | 24B | 128K | Yes (1x A10G) |
| Llama 3.3 | 70B | 128K | Yes (2x A100) |
| Mistral Large 3 | 675B MoE | 128K | Challenging |
| DeepSeek-V3 | 671B MoE | 131K | Challenging |

---

*Author: Prayas Abhinav*
*Last Updated: 10 February 2026*
