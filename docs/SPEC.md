# BNPL Fragility Project: Build Spec

Oct 3, 2026 · @Shane Patandin

## Overview

This project tests whether late payment on Buy Now, Pay Later loans reflects household liquidity strain, and explains why the late payment share among users rose from 18% in 2023 to 26% in 2025, using public Federal Reserve SHED microdata from 2021 to 2025.

**Research questions**

1. Among BNPL users, is late payment associated with financial fragility after controlling for income, age, education, and card ownership?
2. How much of the rise in late payment comes from a change in who uses BNPL (composition), and how much from similar users paying late more often (behavior)?

**Finished deliverables**

- A reproducible repo: one command rebuilds every table and figure from raw data.
- A README written like an abstract, with the headline result on the first screen.
- A four to six page writeup as a PDF.
- A project page on the resume site with two figures.

**How to use this spec.** Export it as Markdown and save it in the repo as `docs/SPEC.md`. Paste the CLAUDE.md block below into the repo root. Then run Claude Code one phase at a time, checking each phase's acceptance criteria before moving on.

## Analysis menu

Build the two core analyses first. Add at most two extensions, chosen by which roles you are targeting. Every extension depends on whether its question appears in enough waves, so Phase 1 confirms that before you commit.

| Analysis | Question | Method | Why it is interesting | Data risk |
| --- | --- | --- | --- | --- |
| **Core A: Fragility and late payment** | Does fragility predict late payment once income and demographics are held fixed? | Survey weighted logit, average marginal effects, pooled waves with year effects | Hayashi and Routh (2025) showed raw counts for one wave. Controls plus newer waves turn that into an estimate. | Low. Late payment and fragility items exist in recent waves. |
| **Core B: Why late payment rose** | Is the 18% to 26% rise about who uses BNPL or how users behave? | Fairlie nonlinear decomposition, with DFL reweighting as a robustness check | Either answer has a policy reading. Composition points to expansion into fragile groups; behavior points to stress hitting existing users. | Medium. Needs consistent late payment wording across waves. |
| Extension 1: Essentials as a stress signal | Are users who buy groceries with BNPL more likely to pay late at the same income? | Logit with purchase type indicators and income controls | The Fed found this pattern in 2025. Testing it across waves turns a single observation into a trend. | High. Purchase type may appear only in recent waves. |
| Extension 2: The overdraft channel | Who has a BNPL autopay trigger an overdraft, and is it concentrated among those with low savings? | Logit on the overdraft item by emergency savings bucket | Shows a concrete cost of BNPL that a 0% APR label hides. | High. The item may be new in 2025. |
| Extension 3: Prediction versus explanation | Does a flexible model predict late payment much better than the logit, and do the same fragility factors drive both? | Gradient boosting with SHAP values, compared with the logit on held out data | Gives the project a genuine ML component, and comparing interpretations is a good interview topic. | Low. Uses Core A's data. |
| Extension 4: Complaint narratives | What harms do BNPL users report, and does the autopay overdraft issue show up? | Classify CFPB narratives by issue type with a hand labeled validation set | Adds consumer voice and real NLP. | Medium. Requires the BNPL identification work from the CFPB plan. |

**Recommended pairings.** For data science and economics roles, choose Core A, Core B, and Extension 1. For ML roles, choose Core A, Core B, and Extension 3, adding Extension 4 only if time allows.

**Interpretation rule for every analysis.** SHED surveys new people each year, so results are associations. Write "associated with," never "causes."

## Data sources

The core analyses need only SHED. Download each wave's public data file and codebook manually from the [SHED page](https://www.federalreserve.gov/consumerscommunities/shed.htm), then place them in `data/raw/`. Don't have Claude Code scrape the site.

| Source | Used for | Access | Notes |
| --- | --- | --- | --- |
| SHED public microdata, 2021 to 2025 | All core analyses | Free download, one file and codebook per wave | BNPL questions start in 2021. Each wave has its own weight variable, and question wording changes, so read every codebook. |
| SHED annual reports and the Aug 2026 Consumer & Community Context note | Validation targets | Free PDFs and web pages | Published figures, such as 16% BNPL use in 2025 and 26% late payment, are what your replication must match. |
| CFPB complaint database bulk CSV | Extension 4 only | files.consumerfinance.gov/ccdb/complaints.csv.zip | No BNPL category exists. Use the company and keyword identification plan. |
| Affirm shareholder letters | One context figure only | SEC EDGAR | Descriptive only, never in a model. |

Record the download date and SHA256 hash of every raw file in `data/raw/MANIFEST.md`. Raw files are never edited, and they stay out of git if size or licensing requires it.

## Repo structure

The layout separates raw data, a harmonized dataset, and analysis, so every result traces back to a documented variable definition.

```
bnpl-fragility/
├── CLAUDE.md                 # instructions for Claude Code (section below)
├── README.md                 # abstract style summary, headline result first
├── Makefile                  # make data / make models / make figures / make all
├── requirements.txt          # pinned versions
├── config/
│   └── variables.yaml        # harmonized variable map: concept -> per wave source column + recode
├── data/
│   ├── raw/                  # untouched downloads + MANIFEST.md (dates, hashes)
│   ├── interim/              # one cleaned file per wave
│   └── processed/            # pooled, harmonized analysis file
├── docs/
│   ├── SPEC.md               # this document
│   ├── variable_inventory.md # Phase 1 output: every BNPL related item by wave, exact wording
│   └── decisions.md          # log of every judgment call, dated
├── src/bnpl/
│   ├── load.py               # read raw waves
│   ├── harmonize.py          # apply variables.yaml, build pooled file
│   ├── indicators.py         # fragility indicators
│   ├── describe.py           # weighted shares, replication tables
│   ├── models.py             # logit + marginal effects (you write this)
│   ├── decompose.py          # Fairlie + DFL (you write this)
│   └── figures.py
├── tests/                    # harmonization checks, replication targets
├── notebooks/                # exploration only; nothing final lives here
└── reports/
    ├── tables/
    ├── figures/
    └── writeup/              # paper source + PDF
```

The key file is `config/variables.yaml`. Each concept, such as `late_payment`, maps to the source column and recode for each wave, with the exact question text quoted. When an interviewer asks how you handled wording changes, this file is your answer.

## Build phases

Run one phase per Claude Code session and don't start the next until its acceptance check passes. Phase 1 is the gate for everything else, because it tells you which analyses the data can actually support.

1. **Phase 0: Scaffold.** Create the repo layout, Makefile targets, pinned requirements, a test runner, and the CLAUDE.md file.
   - Accept when: `make all` runs end to end on empty stubs, and `pytest` passes.
2. **Phase 1: Variable inventory.** Read every codebook and list each item related to BNPL, fragility, and the controls, by wave, with the exact question text and response codes.
   - Output: `docs/variable_inventory.md`, a table of concept × wave.
   - Accept when: you have personally checked each BNPL row against the codebook PDF. Then choose your extensions using the Data risk column above.
3. **Phase 2: Harmonize.** Write `config/variables.yaml` and `harmonize.py`, producing one pooled file with a wave column and the correct weight per row.
   - Accept when: tests confirm that every concept is non missing in the waves where the inventory says it exists, and that weights sum to each wave's documented total.
4. **Phase 3: Replicate published numbers.** Compute weighted BNPL use and the late payment share by wave.
   - Accept when: your figures match the Fed's published ones (for example, 16% use and 26% late in 2025) to within rounding. If they don't, stop and fix the weights or coding. Nothing downstream can be trusted until this passes.
5. **Phase 4: Core A.** Build fragility indicators following Hayashi and Routh, then fit a weighted logit of late payment on fragility with controls and year effects. Report average marginal effects with bootstrapped confidence intervals.
   - Accept when: there's a results table and a marginal effects plot, plus a paragraph in `decisions.md` explaining each control.
6. **Phase 5: Core B.** Run the Fairlie decomposition of the late payment change between your first and last usable waves, with DFL reweighting as a check.
   - Accept when: both methods show the composition and behavior split with confidence intervals, and any disagreement between them is explained in writing.
7. **Phase 6: Extensions.** Only the ones Phase 1 cleared.
8. **Phase 7: Package.** Write the README, writeup, figures for the site page, and a limitations section.
   - Accept when: a fresh clone plus the raw files reproduces every number in the README with one command.

## Who builds what

Let Claude Code handle the plumbing and write the statistical core yourself, since those are the parts you'll be asked to defend line by line.

| Component | Claude Code | You |
| --- | --- | --- |
| Scaffold, Makefile, tests setup | Builds it | Reviews it |
| Variable inventory | Drafts it from codebooks | Verifies every BNPL row against the PDF |
| `variables.yaml` recodes | Proposes them | Approves each recode, logs judgment calls |
| Harmonization and loading code | Writes it | Reads it fully |
| Replication tables | Writes them | Checks them against published figures |
| Fragility indicators | Drafts from your definitions | Defines each indicator |
| Logit, marginal effects, bootstrap | Reviews your code | **Writes it** |
| Fairlie and DFL decomposition | Reviews your code | **Writes it** |
| Figures, README, writeup | Formatting help | Writes the argument and the findings |

A good test for any piece: if you couldn't rebuild it on a whiteboard, either write it yourself or keep asking Claude Code to explain it until you could.

## CLAUDE.md for the repo root

Copy this into `CLAUDE.md` so every Claude Code session starts with the same rules.

```markdown
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
```

## Open questions to settle early

Each of these changes the design, so answer them in Phase 1 rather than discovering them mid-analysis.

- [ ] Which waves ask the late payment question, and is the wording identical across them? This sets the endpoints for Core B.
- [ ] Does SHED publish design variables beyond the weight, such as strata or replicate weights? This decides how you compute standard errors.
- [ ] Is the reasons for use item multiple choice in every wave, and do the answer options match? This affects any necessity variable.
- [ ] In which waves does the purchase type question appear? This decides Extension 1.
- [ ] Is late payment asked of all BNPL users, or only some? This defines your analysis sample.
- [ ] Before claiming Core B is new, search Google Scholar and SSRN for SHED with BNPL and decomposition.
