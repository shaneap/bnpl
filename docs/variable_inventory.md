# SHED Buy Now, Pay Later Questions by Wave

Working table of which BNPL questions appear in each wave of the Federal Reserve's Survey of Household Economics and Decisionmaking (SHED). This decides which waves can be pooled and which analyses are possible.

Last updated: October 22, 2026

## Legend

- **✓ codebook**: exact wording and variable name verified in that year's public codebook
- **✓ report**: the Fed published a statistic for that year, so the item exists, but wording and variable name are not yet verified
- **?**: not yet checked

## Coverage matrix

| Item | Var (2025) | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|
| Used BNPL in past year | BNPL1 | ✓ report (10%) | ✓ report (12%) | ✓ report (14%) | ✓ report (15%) | ✓ codebook (16%) |
| Late on a BNPL payment | BNPL3 | ? | ? | ✓ report (18% of users) | ✓ report (nearly 1 in 4) | ✓ codebook |
| Charged extra for paying late | BNPL3A | ? | ? | ✓ report (11% of users) | ✓ report (13% of users) | ✓ codebook |
| BNPL payment triggered overdraft or NSF fee | BNPL1A | ? | ? | ? | ? | ✓ codebook |
| Reasons for using BNPL (select all) | BNPL4_a to g | ? | ? | ? | ? | ✓ codebook |
| Most important reason | BNPL5 | ? | ? | ? | ? | ✓ codebook |
| What BNPL was used for | BNPL6_a onward | ? | ? | ? | ? | ✓ codebook |

Usage shares by year come from the Fed's August 2026 Consumer & Community Context note (2021 to 2025 series). The 2023 and 2024 late payment and late fee figures come from the Fed's annual reports. Variable names can change between years, so match on wording, not names.

## 2025 wording (verified)

Source: `SHED_2025codebook.pdf`. Counts are unweighted. Do not use them as estimates.

| Var | Wording | Asked of | Unweighted n |
|---|---|---|---|
| BNPL1 | In the past year, have you used a "Buy Now, Pay Later" service to buy something? | All respondents | 2,004 yes of 12,934 |
| BNPL3 | In the past year, have you ever been late making a payment for something you bought using a Buy Now, Pay Later service? | BNPL users | 487 yes of 2,004 |
| BNPL3A | In the past year, have you been charged extra because you were late on a Buy Now, Pay Later payment? | Late payers | 302 yes of 487 |
| BNPL1A | In the past year, did any of your BNPL payments trigger an overdraft or non-sufficient-funds (NSF) fee on your bank account? | Subset of users (542 answered; check skip logic) | 206 yes |
| BNPL4_a to g | Thinking about the most recent time you used a Buy Now, Pay Later service, were each of the following a reason why you chose to finance the purchase in this way? Options: avoid interest charges; wanted to spread out payments; wanted a fixed number of payments; convenience; only way I could afford it; only accepted payment method I had; did not want to use a credit card | BNPL users | 1,161 said "only way I could afford it" |
| BNPL5 | Thinking about the most recent time you used a Buy Now Pay Later service, which of the following was the most important reason why you chose to finance the purchase in this way? | Users with more than one reason (1,935 answered) | 574 chose "only way I could afford it" |
| BNPL6_* | In the past year, when you have used Buy Now, Pay Later, which of the following have you used it for? Categories include clothing or accessories, groceries or food delivery, travel expenses, and more | BNPL users | 375 groceries or food delivery |

## Fragility variables available in 2025 (same file)

These are candidate predictors for the late payment logit. Check each one against earlier waves before pooling.

| Var | Measure |
|---|---|
| B2 | How well managing financially (finding it difficult to get by, just getting by, doing okay, living comfortably) |
| C2A, C3P, C4A | Has a credit card; paid less than the minimum last month; how often carried a balance |
| BK2_f | Paid an overdraft fee in past 12 months (bank account holders only) |
| BK2_c, BK2_d | Payday loan; pawn or auto title loan |
| A1_a, A1_c | Turned down for credit; put off applying for fear of denial |
| R11 | Behind on rent in past year (renters only) |
| $400 expense and largest emergency expense items | Further in the codebook; confirm variable names |

## Notes that change the plan

1. **Check the 2023 and 2024 late payment wording before anything else.** The decomposition targets the jump from 18% to nearly a quarter. If the question wording or skip logic changed between those years, part of that jump is a survey artifact. This check comes first.
2. **2025 includes a recontact panel.** The 2025 file carries `panel_weight` for respondents who took both the 2024 and 2025 surveys (about 4,400 people). That allows a within person check: does fragility measured in 2024 predict late payment in 2025? It speaks directly to the concern that fragility comes before BNPL use. Confirm how many of those recontacts used BNPL before relying on it, because the subsample may be small.
3. **Analysis 1 on 2025 alone is already being done.** A Research Square preprint (Kaibo Tang, 2025 SHED, not peer reviewed) models late payment among the same 2,004 users, and the Fed's August 2026 note reports fee and overdraft rates by purchase type. Cite both. The original contribution is the multiwave decomposition and the panel check, not a single year logit.
4. **The necessity angle lives in BNPL4, BNPL5, and BNPL6.** The Fed's August 2026 note found grocery and food delivery users were charged late fees or overdrafts far more often than clothing buyers (43% vs 25%). Whether those items exist in 2023 and 2024 decides if the necessity angle can be tracked over time or stays a 2025 cross section.

## To fill the ? cells

1. Download the public data and codebooks for 2021 to 2024 from the SHED data page (federalreserve.gov/consumerscommunities/shed_data.htm).
2. Extract the BNPL block from each codebook:
   ```bash
   pdftotext -layout SHED_2023codebook.pdf - | grep -n -i -A8 "pay later"
   ```
   Search on "pay later" rather than "BNPL", since variable prefixes may differ by year.
3. For each item, record the exact wording, the variable name, and who was asked. Mark any change in wording or skip logic.
