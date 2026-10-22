# BNPL Fragility Project

Research project using Federal Reserve SHED microdata (2021–2025) to study
late payment among Buy Now, Pay Later users. Full spec: docs/SPEC.md.

## Rules
- Never invent SHED variable names, codes, or question wording. Every variable
  must trace to docs/variable_inventory.md, which cites the codebook. If an item
  is not in the inventory, stop and ask.
- Never hardcode or estimate a result. All numbers come from code run on data.
- Every estimate uses the survey weight for its wave. Unweighted results only
  when explicitly labeled as such.
- Never modify files in data/raw/.
- Log any judgment call (recodes, exclusions, missing value handling) in
  docs/decisions.md with the date and the reason.
- Do not write src/bnpl/models.py or src/bnpl/decompose.py. The author writes
  these. You may review them and suggest changes.
- Results are associations. Never use causal language in output text.

## Workflow
- Work one phase at a time (see docs/SPEC.md, Build phases). State the phase
  at the start of the session and stop when its acceptance check passes.
- Add or update tests in tests/ for every harmonization change.
- Run `make all` and `pytest` before finishing a session.

## Stack
Python 3.11, pandas, numpy, statsmodels, scikit-learn, matplotlib, pyyaml,
pytest. Add packages only with a pinned version in requirements.txt.
