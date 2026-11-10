# Financial Fragility and Late Payment Among BNPL Users

Is late payment on Buy Now, Pay Later loans a sign of household liquidity strain, and why did it rise so quickly? This project uses five waves of the Federal Reserve's Survey of Household Economics and Decisionmaking (SHED, 2021 to 2025) to find out.

> **Status: in progress.** Data pipeline and replication of published Fed figures are complete. Core models are underway. Results below will be filled in as each phase finishes.

## Why this matters

About one in six U.S. adults used BNPL in 2025, and the share of users who paid late rose from 18% in 2023 to 26% in 2025. BNPL is marketed as interest free convenience, but use is concentrated among households with little emergency savings. If late payment tracks financial fragility, a missed installment is less a budgeting slip than a signal that a household is running out of room. That matters most for the low income families who rely on BNPL to get by.

## Research questions

1. **Fragility and late payment.** Among BNPL users, is late payment associated with financial fragility after controlling for income, age, education, and credit card ownership?
2. **Why late payment rose.** How much of the rise comes from a change in *who* uses BNPL (composition), and how much from similar users paying late *more often* (behavior)?

## Key results

<!-- TODO: replace each line with the real number once the phase is complete. Do not fill these in by hand. -->

- **Replication:** Weighted BNPL use and late payment shares match the Federal Reserve's published figures for every wave, within rounding.
- **Fragility and late payment:** _Pending (Phase 4)._
- **Decomposition of the rise:** _Pending (Phase 5)._

## Data

| Source | Use | Access |
| --- | --- | --- |
| [SHED public microdata](https://www.federalreserve.gov/consumerscommunities/shed.htm), 2021–2025 | All analyses | Free download, one data file and codebook per wave |
| SHED annual reports and Fed notes | Replication targets | Public |

Raw files are not committed. Download each wave's data file and codebook from the SHED page into `data/raw/`. `data/raw/MANIFEST.md` records the download date and SHA256 hash of each file used.

Question wording changes across waves. Every harmonized variable is defined in `config/variables.yaml`, which maps each concept to its source column and recode for each wave, with the exact question text. The full item inventory is in `docs/variable_inventory.md`.

## Methods

- **Survey weights throughout.** Every estimate uses the weight for its wave.
- **Fragility indicators** follow the constraint measures in Hayashi and Routh (2025), including the ability to cover a $400 emergency expense, revolving card debt (restricted to cardholders), and overdrafts.
- **Fragility model:** weighted logit of late payment on fragility indicators with demographic controls and year effects, reported as average marginal effects with bootstrapped confidence intervals.
- **Decomposition:** Fairlie nonlinear decomposition of the change in late payment between the first and last usable waves, with DiNardo, Fortin, and Lemieux reweighting as a robustness check.ß

## Reproducing the results

```bash
git clone https://github.com/shaneap/bnpl.git
cd bnpl-fragility
pip install -r requirements.txt

# place SHED data files and codebooks in data/raw/ (see MANIFEST.md)
make all        # harmonize, replicate, model, and build figures
pytest          # harmonization and replication checks
```

Individual stages: `make data`, `make models`, `make figures`.

## Repository layout

```
config/variables.yaml       harmonized variable map, by wave
data/raw/                   untouched downloads (not committed)
data/processed/             pooled analysis file
docs/variable_inventory.md  every BNPL related item by wave, exact wording
docs/decisions.md           dated log of every judgment call
src/bnpl/                   loading, harmonization, indicators, models, decomposition
tests/                      harmonization and replication tests
reports/                    tables, figures, and the writeup
```

## Limitations

- **Associations, not causes.** SHED surveys a new sample each year, so it cannot follow a household before and after it starts using BNPL. Prior work finds that users' financial strain often predates BNPL use.
- **Self reported.** Late payment and BNPL use are self reported and may be underreported.
- **Changing questionnaire.** Items and wording shift across waves; each harmonization choice is logged in `docs/decisions.md`.
- **No loan level detail.** SHED does not observe loan amounts, the number of simultaneous loans, or which provider was used.

## Related work

- Hayashi, F. and Routh, A. (2025). *Financial Constraints Among Buy Now, Pay Later Users.* Federal Reserve Bank of Kansas City Economic Review.
- Larrimore, J., Lloro, A., Merchant, Z., and Tranfaglia, A. (2024). *"The Only Way I Could Afford It": Who Uses BNPL and Why.* FEDS Notes.
- deHaan, E., Kim, J., Lourie, B., and Zhu, C. (2024). *Buy Now Pay (Pain?) Later.* Management Science.
- Di Maggio, M., Katz, J., and Williams, E. (2022). *Buy Now, Pay Later Credit: User Characteristics and Effects on Spending Patterns.* NBER Working Paper 30508.
- Fairlie, R. (2005). *An Extension of the Blinder-Oaxaca Decomposition Technique to Logit and Probit Models.* Journal of Economic and Social Measurement.

## Author

**Shane Patandin**, M.S. Data Science, Stony Brook University
[GitHub](https://github.com/shaneap) · [LinkedIn](https://linkedin.com/in/shane-patandin)

This is an independent research project. Data are from the Board of Governors of the Federal Reserve System; the analysis and conclusions are my own.