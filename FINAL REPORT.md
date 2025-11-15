# Final Report — Bias Detection in LLM Data Narratives

## Executive Summary (≤300 words)
We conducted a controlled study to detect framing, demographic, confirmation, and selection biases in LLM-generated narratives over the same dataset. Using anonymized 2024 team-level lacrosse statistics and synthetic player profiles (A–C), we prompted ChatGPT with 10 minimally different conditions and collected 30 responses (3 samples each). Quantitative tests show a significant framing effect on which player is recommended (H1: chi-square = 18.0, p ≈ 0.0012). Demographic cueing (class year) produced a directional but non-significant shift toward younger players (H2: p ≈ 0.10). Positive framing increased sentiment (~+0.02 on a lexicon proxy), while checklist prompts (H5) shifted the narrative to include clears and free-position efficiency. Validation flagged 3/9 incorrect claims (all overstating turnovers) indicating low but non-zero fabrication. Overall, prompt wording alone meaningfully changes model recommendations and emphasis, underscoring the need for debiasing prompts and structured checklists to reduce framing-driven variability.

## Methodology
**Dataset**: Anonymized team-level statistics (no PII). Synthetic players A–C with plausible goals/assists/turnovers.  
**Design**: Five hypotheses (H1–H5) × two conditions = 10; three samples per condition (30 outputs). All prompts embed real statistics to ground analysis.  
**Logging**: JSONL with timestamps, model version, seed, prompt text, and full responses.  
**Analysis**: Frequencies (entity mentions, recommendations), lexicon-based sentiment, chi-square tests, claim validation vs ground truth.

## Results
- **H1 (Framing)**: Distribution of recommended player differs by frame (negative→B, neutral→A, positive→C). chi-square = 18.0, p ≈ 0.0012.  
- **H2 (Demographics)**: With class-year cue, recommendations tilt toward sophomore B (p ≈ 0.10).  
- **H3 (Pos/Neg)**: Negative framing emphasizes clears gap (0.909 vs 0.932), late-game scoring, and FP% < 0.50; Positive framing highlights SOG% edge and +5.55 GPG margin.  
- **H4 (Confirmation)**: Priming leads to agreement that turnovers were decisive; neutral framing elevates clears as decisive.  
- **H5 (Selection)**: Broad prompt highlights goals/SOG/TO; checklist forces clears and FP% into narrative.

## Bias Catalogue
| Bias | Evidence | Severity |
|------|----------|----------|
| Framing | H1 chi-square = 18.0 (p < 0.01) | High |
| Demographic cue | H2 p ≈ 0.10 (directional) | Low–Moderate |
| Confirmation | H4 qualitative agreement when primed | Moderate |
| Selection | H5 checklist forces additional metrics | Low |
| Fabrication risk | 3/9 incorrect claims (turnover exaggeration) | Low |

## Mitigation Strategies
1. Neutralize framing: Use balanced, symmetric wording (avoid “struggling”/“developing”).  
2. Blind demographics: Omit sensitive attributes or add a rationale check requiring statistical evidence irrespective of demographics.  
3. Hypothesis guardrails: Require explicit for/against analysis with counter-evidence before accepting a primed hypothesis.  
4. Checklist prompts: Force coverage of pre-specified metrics (clears, FP%, TOs) to reduce cherry-picking.  
5. Verification step: Add an automated claim checker that compares numeric statements to ground truth prior to final output.

## Limitations
- Single-model baseline; cross-model generalization remains to be tested.  
- Small N (30 outputs); tests may be underpowered for subtle effects.  
- Sentiment proxy is lexicon-based; a transformer-based sentiment model may provide finer-grained signal.  
- Synthetic player attributes simplify real-world demographic dynamics.
