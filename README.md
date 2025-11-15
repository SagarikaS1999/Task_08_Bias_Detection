# Bias Detection in LLM Data Narratives

## Executive Summary
This project investigates whether Large Language Models (LLMs) generate biased data narratives when presented with identical datasets but differently framed prompts. Using an anonymized dataset of synthetic sports players (A, B, C) and real 2024-style team performance metrics, I conducted controlled experiments to test four major bias categories: framing bias, demographic bias, confirmation bias, and selection bias.

A total of 30 structured LLM outputs were collected using ChatGPT (GPT-5) as a single-model baseline. Each hypothesis (H1–H5) included two prompt conditions (e.g., positive vs negative framing), with three samples per condition to account for randomness. All prompts contained real statistics to ensure grounding.

Results indicate strong evidence of framing bias (χ² = 18.0, p = 0.0012), moderate confirmation bias, and mild but present demographic and selection biases. Positive framing increased sentiment by ~0.024, and demographic cues (e.g., “sophomore”) shifted recommendations toward Player B. Validation revealed 3 out of 9 false claims, all exaggerating turnover impacts in positively framed prompts.

---

## Methodology
### Dataset
- Derived from anonymized team-level 2024 statistics (no player names or personal data).  
- Synthetic players (A, B, C) created with plausible values for goals, assists, and turnovers.

### Experimental Design
- **Five hypotheses (H1–H5)** testing framing, demographic, confirmation, and selection biases.  
- **10 prompt conditions** (two per hypothesis) × **3 samples each** = 30 total ChatGPT responses.  
- Each prompt embedded real team metrics (e.g., Goals = 15.23 vs 9.68, SOG% = 0.728 vs 0.665, TO = 317 vs 334).  
- Responses logged with timestamps, seeds, and model versions in JSONL format.

### Analysis
- Quantitative: recommendation frequencies, sentiment analysis, chi-square tests.  
- Qualitative: linguistic framing, narrative tone, fabrication detection.  
- Validation: cross-checked model statements against ground-truth stats.

### Quantitative Results
#### H1 – Framing Bias
- Negative framing → recommends Player B
- Neutral framing → recommends Player A
- Positive framing → recommends Player C
- χ² = 18.0, p = 0.0012 → statistically significant bias

#### H2 – Demographic Bias
- Adding class-year cue shifts recommendations toward younger player (B)
- χ² ≈ 2.67, p ≈ 0.10 → directional effect

#### H3 – Positive vs Negative Framing
- Narrative tone differs:
- Negative → deficits, turnovers
- Positive → growth, assists
- Sentiment difference: +0.026

#### H4 – Confirmation Bias
- Priming prompt (“turnovers decisive…”) → model agrees automatically
- Narrative aligns with primed hypothesis without checking alternate stats

#### H5 – Selection Bias
- Checklist prompts produce richer analyses:
  - Mentions clears, FP%, SOG%
- Sentiment +0.04

#### Fabrication Rate
- 3 out of 9 claims incorrect (33%)
- All exaggerate turnovers in H3 positive framing
- Every other condition → 0% fabrication

### Qualitative Findings
- LLM uses different adjectives depending on framing ("struggling" vs "developing")
- Positive framing produces future-oriented language
- Negative framing increases risk-focused narratives
- Demographic cues introduce subtle stereotypes (favoring “younger” players)
- Checklist prompts reduce cherry-picking and enforce balanced analysis

---

## Results (ChatGPT-Only)
| Hypothesis | Observation | Key Metrics |
|-------------|--------------|--------------|
| **H1 – Framing** | Player recommended changes with framing (neg→B, neu→A, pos→C) | χ² = 18.0 (p = 0.0012) ✔ Significant |
| **H2 – Demographic Cue** | With class-year cue → bias toward sophomore (B) | χ² = 2.67 (p = 0.10) – Directional |
| **H3 – Pos/Neg Framing** | Negative: emphasizes deficits; Positive: highlights strengths | Sentiment Δ ≈ +0.026 |
| **H4 – Confirmation** | Primed hypothesis accepted (“turnovers decisive”) | N/A |
| **H5 – Selection** | Checklist prompts alter narrative focus (adds clears, FP%) | Sentiment Δ ≈ +0.04 |

**Validation:** 9 claims checked, 3 incorrect (all overstating turnovers).  
**Sentiment trend:** positive framing → +0.024 mean sentiment vs 0.0 for negative.  
**Reproducibility:** results stored in `analysis/*.csv|json`.

---

## Bias Catalogue
| Bias Type | Description | Evidence | Severity |
|------------|--------------|-----------|-----------|
| **Framing Bias** | Word choice (“struggling” vs “developing”) alters recommendation | H1 χ² = 18.0 (p < 0.01) | ★★★★☆ |
| **Demographic Bias** | Mentions of class year shift focus to younger players | H2 trend p = 0.10 | ★★☆☆☆ |
| **Confirmation Bias** | Model reinforces primed hypothesis statements | H4 qualitative | ★★★☆☆ |
| **Selection Bias** | Checklist framing expands statistics referenced | H5 language analysis | ★★☆☆☆ |
| **Fabrication Risk** | Minor exaggeration of turnover stats | 3/9 false claims | ★☆☆☆☆ |

---

## Conclusions
ChatGPT demonstrates measurable **framing sensitivity**: identical data prompts yield distinct coaching recommendations purely from language tone. Demographic cues slightly influence prioritization, hinting at stereotype persistence even in anonymized contexts. Although numerical hallucination was low (3 / 9 claims), qualitative review reveals that tone and context shape emphasis more than factual interpretation.

---

## Limitations
- Single-model baseline (ChatGPT only); cross-model comparison pending.  
- Small sample size (30 responses).  
- Sentiment analysis uses lexicon approximation, not transformer-based classifier.  
- Player dataset synthetic; real-world demographic effects may differ.

---

## Future Work
- Extend to **Claude 3.5** and **Gemini 1.5 Pro** for cross-model bias comparison.  
- Introduce **temporal stability tests** (re-run monthly).  
- Implement **bias-mitigation prompt engineering** and measure improvement.  
- Optional: deploy interactive Streamlit dashboard for visualization.

---

**Model Tested:** ChatGPT (GPT-5)  
**Date:** November 2025
