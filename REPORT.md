# Bias Detection in LLM Data Narratives — Interim Report (Weeks 1–2)

## Executive Summary (≤300 words)
This interim report summarizes experimental design decisions and the initial data collection plan to evaluate framing, demographic, confirmation, and selection biases in LLM-generated narratives over the **same** statistics. We use anonymized lacrosse team data (Season 2024 excerpt) and a small synthetic player dataset. We pre-registered hypotheses H1–H5 and created minimally different prompt pairs to isolate the variable of interest. We specified structured logging across multiple models and seeds, with temperature control and reproducibility metadata.

## Methodology (Design)
- **Dataset**: Syracuse team season excerpt and anonymized player metrics (A–C). (See `data/`)
- **Hypotheses**: H1–H5 as documented in `prompts/prompt_templates.json`.
- **Prompt construction**: All prompts include the same base stats; variants change only framing or demographic cue.
- **Ground truth**: Numeric truth extracted from the official combined team statistics PDF (as of 2024-06-04); stored in `data/su_stats_excerpt.json`.
- **Sampling**: 2–3 models, 3–5 responses per prompt, controlled temperature.

## Data Collection (Plan & Status)
- **Manifest**: Generated via `scripts/experiment_design.py` including models, seeds, and prompts.
- **Execution**: `scripts/run_experiment.py` supports OpenAI, Anthropic, Gemini, and a **mock** provider for dry runs. Responses are logged to JSONL under `results/` with prompt, condition, hypothesis ID, seed, and model metadata.
- **Inclusion of statistics**: Each prompt contains the same base numbers to ground analysis and reduce hallucination.

## Scientific Rigor & Reproducibility
- Model names pinned in the manifest; control of temperature and seeds.
- Structured logging (JSONL) and deterministic mock mode for CI testing.
- Separate analysis scripts for quantitative bias signals and claim validation against ground truth.

## Ethics & Privacy
- All entities are anonymized as "Player A/B/C". No personally identifying data is included. Demographic cue is limited to non-sensitive "class year" (senior/sophomore/junior).

## Next Steps (Week 3)
- Run real models (if credentials available).
- Use `scripts/analyze_bias.py` to compute mention distributions and sentiment deltas per condition (H1/H2 chi-square).
- Use `scripts/validate_claims.py` to estimate a fabrication/contradiction rate per condition.

## Results


**Models:** ChatGPT (gpt-5-thinking) only; 3 samples per prompt; 10 prompt conditions (H1–H5 x 2 variants) → 33 total responses.
**Key signals:**
- **Framing effect (H1)**: Recommendation distribution differs by framing (negative→B; positive→C; neutral→A). See chi-square below.
- **Demographic cue (H2)**: With class-year provided, selections tilt toward the sophomore (B); without, toward leading scorer (A).
- **Confirmation bias (H4)**: When primed, the analysis agrees that turnovers are decisive; neutral condition emphasizes clears.
- **Selection bias (H5)**: Broad prompt highlights goals/SOG/turnovers; checklist forces discussion of clears + FP%.

**Chi-square tests (recommendations by condition):**
- H1: chi2=18.0, p=0.0012340980408667957, dof=4
- H2: chi2=2.6666666666666665, p=0.10247043485974942, dof=1

**Sentiment by condition (lexicon proxy):**
hypothesis_id         condition  mean_sentiment  n
           H1          negative        0.000000  3
           H1           neutral        0.000000  3
           H1          positive        0.024400  3
           H2           no_demo        0.000000  3
           H2         with_demo        0.000000  3
           H3    negative_frame        0.000000  3
           H3    positive_frame        0.026328  3
           H4           neutral        0.031270  3
           H4 primed_hypothesis        0.029429  3
           H5             broad        0.083430  3
           H5         checklist        0.043533  3

**Validation against ground truth:**
- No contradictions on turnovers (team 317 vs opp 334), FP% (0.482 vs 0.437), and clears (opp 0.932 > team 0.909) were flagged; claims logged in `analysis/claims_validation.json`.
