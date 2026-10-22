# SHED Buy Now, Pay Later Questions by Wave

Working table of which BNPL, fragility, and control items appear in each wave of the Federal Reserve's Survey of Household Economics and Decisionmaking (SHED). This decides which waves can be pooled and which analyses are possible.

Last updated: October 22, 2026 (Phase 1)

## Sources and method

- Codebooks: `data/raw/SHED_{2021..2025}codebook.pdf`; data: `data/raw/public{2021..2025}.csv`. Hashes and download dates are in `data/raw/MANIFEST.md`.
- Wording, variable names, and numeric codes come from the codebook variable labels, parsed by `scripts/codebook.py`. Page numbers in the generated tables are codebook PDF pages.
- **Who was asked** is inferred from the data: for every item and wave, `scripts/phase1_checks.py` tests that the stated rule selects exactly the rows with an answer. The codebooks don't print routing, and the questionnaire appendix isn't in `data/raw/`. All 383 item-waves pass; the only exceptions are rows where the item or its parent was imputed (see the BNPL5 note).
- The public CSVs store **value labels** ("Yes", "Living comfortably"), not numeric codes. There are no refusal or don't-know codes. Item nonresponse is imputed, and each item has a `<var>_iflag` column (1 = imputed).
- Regenerate everything below the GENERATED marker with `make inventory`.

## Legend

- **✓ codebook**: variable name, wording, and codes found in that year's codebook and parsed by script. The spec still requires the author to check each BNPL row against the PDF by eye; that check is **pending**.
- **(report x%)**: figure the Fed published, kept from the earlier draft as a Phase 3 replication target. Not computed here.
- **—**: not in that wave's codebook or data file.

## Coverage matrix: BNPL

| Item | Var | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|
| Used BNPL in past year | BNPL1 | ✓ codebook (report 10%) | ✓ codebook (report 12%) | ✓ codebook (report 14%) | ✓ codebook (report 15%) | ✓ codebook (report 16%) |
| Number of current BNPL purchases | BNPL2 | ✓ codebook | ✓ codebook | — | — | — |
| Late on a BNPL payment | BNPL3 | ✓ codebook | ✓ codebook | ✓ codebook (report 18% of users) | ✓ codebook (report nearly 1 in 4) | ✓ codebook |
| Charged extra for paying late | BNPL3A | — | ✓ codebook | ✓ codebook (report 11% of users) | ✓ codebook (report 13% of users) | ✓ codebook |
| BNPL payment triggered overdraft or NSF fee | BNPL1A | — | — | — | — | ✓ codebook |
| Reasons for using BNPL (yes/no grid) | BNPL4_* | ✓ codebook, a–f, **different options** | ✓ codebook, a–g | ✓ codebook, a–g | ✓ codebook, a–g | ✓ codebook, a–g |
| Most important reason | BNPL5 | — | — | — | — | ✓ codebook |
| What BNPL was used for (select all) | BNPL6_a–g | — | — | — | — | ✓ codebook |
| Beliefs: BNPL builds credit history / on-time payments help score | BNPL7_a–b | — | — | — | — | ✓ codebook |

Variable names for the BNPL items stay the same across waves. Wording is identical 2021–2024. In 2025 "Buy Now Pay Later" becomes "Buy Now, Pay Later". BNPL3A wording is identical 2022–2024, and 2025 adds the comma and capitalizes.

### Who was asked (BNPL, verified against data in every wave)

| Var | Asked of |
|---|---|
| BNPL1 | All respondents |
| BNPL2, BNPL3, BNPL4_*, BNPL6_*, BNPL7_* | BNPL1 = Yes |
| BNPL3A | BNPL3 = Yes (late payers only) |
| BNPL1A (2025) | BNPL1 = Yes **and** BK2_f = Yes (paid a bank overdraft fee in the past 12 months): 542 of 542 match. The earlier draft said "subset of users; check skip logic". BNPL1A's denominator is BNPL users who paid an overdraft fee, not all users. |
| BNPL5 (2025) | BNPL1 = Yes and at least one BNPL4 item = Yes. The earlier draft said "users with more than one reason", which is wrong: 86 users with exactly one reason answered BNPL5. 11 users with ≥1 reason have no BNPL5; all 11 have imputed BNPL4 answers. |

### Reasons grid (BNPL4) options by wave

| Option | 2021 | 2022–2025 |
|---|---|---|
| Cheaper | BNPL4_a | — |
| Avoid interest charges | — | BNPL4_a |
| More convenient / Convenience | BNPL4_b ("More convenient") | BNPL4_d ("Convenience") |
| Wanted to spread out payments | — | BNPL4_b |
| Wanted a fixed number of payments | — | BNPL4_c |
| Only way I could afford it | BNPL4_c | BNPL4_e |
| Only accepted payment method I had | BNPL4_d | BNPL4_f |
| Did not want to use a credit card | BNPL4_e | BNPL4_g |
| Other (please specify) | BNPL4_f | — |

The stem also changes. 2021 asks "why did you choose to finance the purchase in this way?"; 2022+ asks "were each of the following a reason why you chose to finance the purchase in this way?". The same letter means a different option in 2021, so harmonize on the option label, never the variable suffix.

## Coverage matrix: fragility

| Concept | 2021 | 2022 | 2023 | 2024 | 2025 | Comparability notes |
|---|---|---|---|---|---|---|
| How well managing financially | B2 | B2 | B2 | B2 | B2 | Wording and codes identical |
| Better/worse off vs 12 months ago | B3 | B3 | B3 | B3 | B3 | Identical |
| 3-month emergency fund | EF1 | EF1 | EF1 | EF1 | EF1 | Identical |
| Could cover 3 months of expenses if income lost | EF2 | EF2 | EF2 | EF2 | EF2 | Asked if EF1 = No. 2023 codebook label is truncated in the PDF ("...government be"). |
| How would pay a $400 emergency expense | EF3_a–h | EF3_a–h | EF3_a–h | EF3_a–h | EF3_a–h | **2022 split ballot: $400 (9,293) or $500 (2,374) by `DOV_EF_amount`.** CSV "yes" label is the option text in 2021–2023 and "Yes" in 2024–2025; "no" is "No, did not do this" in 2023. |
| Would cover $400 with cash or equivalent (Fed derived) | pay_casheqv | pay_casheqv | pay_casheqv | pay_casheqv | pay_casheqv | 2022: defined only for the $400 arm |
| Able to pay all bills in full **this month** | EF5A | EF5A | — | — | — | Prospective, includes credit cards |
| Paid all bills in full **last month**, excluding credit cards | — | — | EF5C | EF5C | EF5C | **Not the same question as EF5A**: retrospective, excludes card bills |
| $400 expense would prevent paying other bills | EF5B | EF5B | — | — | — | Asked if EF5A = Able; 2022 uses $400/$500 |
| Bills expected to skip / would skip | EF6A_a–g, EF6B_a–g | EF6A_a–g, EF6B_a–g | — | — | — | EF6A if EF5A = Can't; EF6B if EF5B = Could not |
| How each bill was handled last month | — | — | EF6C_a–d | EF6C_a–d | — | Asked if EF5C = No |
| Had bills difficult to pay last month | — | — | — | — | EF5D | Asked if EF5C = Yes |
| Actions when had difficulty paying a bill | — | — | — | — | EF8_a–j | Asked if EF5C = No or EF5D = Yes |
| Largest emergency expense payable from savings | — | EF7 | EF7 | EF7 | EF7 / EF7A | **2025 split ballot by `dov_ef7`**: EF7 (5 brackets, top "$2,000 or more") for dov_ef7 = 1 (6,453); EF7A (6 brackets, adds "$2,000 to $4,999" and "$5,000 or more") for dov_ef7 = 0 (6,481) |
| Income volatility | I9 | I9 | I9 | I9 | I9 | Identical codes |
| Struggled to pay bills because income varies | I12 | I12 | I12 | I12 | I12 | Asked if I9 ≠ "Roughly the same amount each month" |
| Credit card debt | C3 | C3 | — | — | — | **Wording changes 2021→2022**: "any outstanding unpaid credit card debt" vs "credit card debt that you do not expect to pay in full with your next payment" |
| Paid less than the minimum on a card last month | — | — | C3P | C3P | C3P | Codes: -9 = didn't use cards; 1 = paid at least minimum on all; 2 = did not pay or paid less than minimum on at least one |
| How often carried a card balance | C4A | C4A | C4A | C4A | C4A | Identical; asked if C2A = Yes |
| Has bank account | BK1 | BK1 | BK1 | BK1 | BK1 | Minor punctuation only |
| Payday loan; pawn/title loan; other AFS | BK2_a–e | BK2_a–e | BK2_a–e | BK2_a–e | BK2_a–e | All respondents |
| Paid an overdraft fee | BK2_f | BK2_f | BK2_f | BK2_f | BK2_f | Asked if BK1 = Yes |
| Applied for credit | A0 | A0 | A0 | A0 | A0 | All respondents |
| Turned down / approved for less / put off applying | A1_a–c | A1_a–c | A1_a–c | A1_a–c | A1_a–c | **Asked only if A0 = Yes**, including A1_c "put off applying for fear of denial". A1_c therefore misses non-applicants, the people most likely to be discouraged borrowers. |
| Behind on rent in past year | R11 | R11 | R11 | R11 | R11 | Asked if GH1 = Pay rent |

## Coverage matrix: controls and design

| Concept | Vars (all five waves unless noted) | Notes |
|---|---|---|
| Has a credit card | C2A | 2023+ adds "Please do not include debit cards or prepaid cards." |
| Household income | I40; inc_4cat_50k (Fed derived); ppinc7 (Ipsos profile) | **I40 brackets change in 2023**: 11 categories with $0 (2021–2022) become 15 categories starting at "Less than $5,000" (2023–2025), and the question is reworded. In 2022 most respondents got an exact-amount question (I39), and I40 went only to the 1,109 who refused I39 (`income_question`); I40 is nonmissing for everyone in 2022. `inc_4cat_50k` uses the same 4 brackets in every wave. |
| Age | ppage, ppagecat | Profile variables, identical codes |
| Education | ED0 (SHED), ppeducat (profile) | ED0 codes identical across waves |
| Gender, race/ethnicity, marital status, household size, children, employment, metro, region | ppgender, ppethm, ppmarit5, pphhsize, ppkid017, ppemploy, ppmsacat, ppreg4 | Profile variables |
| Housing tenure | GH1 | Routes R11 |
| Weights | weight, weight_pop (cross-section); panel_weight, panel_weight_pop (recontacts) | **No strata, PSU, or replicate weights in any wave.** The codebooks describe only these two weight pairs. |
| Respondent ID | shedid | Unique within each wave; links waves (see panel section) |
| Split-ballot flags | DOV_EF_amount (2022), income_question (2022), dov_ef7 (2025) | Needed in Phase 2 |

## 2023 vs 2024 late payment question: word-for-word comparison

| | 2023 (codebook p39) | 2024 (codebook p58) |
|---|---|---|
| BNPL3 wording | In the past year, have you ever been late making a payment for something you bought using a Buy Now Pay Later service? | In the past year, have you ever been late making a payment for something you bought using a Buy Now Pay Later service? |
| BNPL3 codes | 0 = No, 1 = Yes | 0 = No, 1 = Yes |
| BNPL3 asked of | BNPL1 = Yes (1,455 of 1,455; 0 mismatches) | BNPL1 = Yes (1,670 of 1,670; 0 mismatches) |
| Filter item BNPL1 | In the past year, have you used a "Buy Now Pay Later" service to buy something? | identical |
| Follow-up BNPL3A | In the past year, have you been charged extra because you were late on a buy now pay later payment? Asked if BNPL3 = Yes | identical, same routing |
| Block order | C2A, C3P, C4A → BNPL1 → BNPL3 → BNPL3A → BNPL4_a–g → S16 | same |
| Imputed BNPL3 values (unweighted) | 7 | 12 |

**Result: no wording, code, or routing difference in BNPL1, BNPL3, or BNPL3A between 2023 and 2024.** The block sits on a later codebook page in 2024 (p58 vs p39), but the items immediately before and after it are the same in both years. Codebook order follows question order, but I cannot rule out changes earlier in the questionnaire that might act as context effects. Elsewhere in the BNPL block the only differences are cosmetic: BNPL4_b is missing "Buy Now" in the 2023 label ("a Pay Later service"), and BNPL4_f uses an en dash in 2024. **Limit:** this compares codebook labels. The questionnaire appendix (not in `data/raw/`) is the authoritative instrument text and should be checked before the Core B writeup.

## 2025 panel recontacts and BNPL use

The 2025 codebook says `panel_weight`/`panel_weight_pop` are for "respondents who took both the 2024 and 2025 survey". All 4,419 rows with nonmissing `panel_weight` match a 2024 record on `shedid`, so linking on `shedid` works. One 2025 row without a panel weight also has a `shedid` that appears in 2024; it is excluded because it has no panel weight. The generated table below has unweighted counts and panel-weighted shares. In short, of 4,419 recontacts, **601 used BNPL in 2024, 630 used it in 2025, and 392 used it in both years** (unweighted). Only 131 were late in 2024 and 147 in 2025, so a within-person late-payment model will have little power.

## Answers to the spec's open questions

1. **Which waves ask late payment, and is wording identical?** BNPL3 is in all five waves with identical wording 2021–2024. 2025 differs only by the comma in "Buy Now, Pay Later". Routing (BNPL1 = Yes) and codes are identical throughout.
2. **Design variables beyond the weight?** None. There are no strata, PSU, or replicate weights; standard errors need another approach (Phase 4 decision).
3. **Is the reasons item multiple choice in every wave, with matching options?** It is a yes/no grid in every wave, but the options differ in 2021 (6 options including "Cheaper" and "Other") from 2022–2025 (7 options). See the BNPL4 table.
4. **Purchase type question?** 2025 only (BNPL6_a–g). Extension 1 can only be a 2025 cross-section.
5. **Is late payment asked of all BNPL users?** Yes. BNPL3 goes to every respondent with BNPL1 = Yes in all waves, so the analysis sample is all BNPL users.
6. Overdraft item (Extension 2): 2025 only, and only BNPL users who paid an overdraft fee were asked.

## Notes that change the plan

1. **2023 → 2024 late payment wording is unchanged**, so the measured rise is not a wording or routing artifact, at least as far as the codebooks can show. The questionnaire check above is still outstanding.
2. **Core B endpoints:** the late item is comparable 2021–2025, but several fragility items are not. EF5A (2021–22) and EF5C (2023–25) measure different things, C3 becomes C3P, and I40 brackets change in 2023. Items that stay comparable across 2023–2025: B2, B3, EF1, EF2, EF3/pay_casheqv, EF5C, I9, I12, C3P, C4A, BK1, BK2, A0, A1, R11, inc_4cat_50k. EF7 is comparable across 2022–2024 and in the 2025 dov_ef7 = 1 half only.
3. **Panel:** 630 linked 2025 users (392 who also used in 2024) is small; treat the panel check as descriptive.
4. **Analysis 1 on 2025 alone is already being done** (Kaibo Tang preprint; Fed August 2026 note). This note is unchanged from the earlier draft.
5. **Extensions 1 and 2 are 2025-only** (BNPL6, BNPL1A). Extension 2's denominator is overdraft-fee payers.
6. **Imputed values:** SHED imputes item nonresponse (7–12 imputed BNPL3 values per wave). Whether to keep or drop imputed values is a Phase 2 decision.

<!-- BEGIN GENERATED: scripts/phase1_checks.py -->

## Item detail by wave (generated)

Generated by `make inventory`. Wording is the codebook variable label, whitespace and quote
characters normalized; the codebook label is the only wording source in data/raw (the
questionnaire appendix is not). Codes are the codebook numeric codes; the public CSVs store the
value **labels**, not the codes. Answered n is **unweighted**. "Rule check" is the number of rows
where the asked-of rule disagrees with who actually has an answer; mismatches in parentheses
involve an imputed item (`_iflag` = 1).

### BNPL

#### Used BNPL in past year

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | BNPL1 | p38 | In the past year, have you used a "Buy Now Pay Later" service to buy something? | 0=No; 1=Yes | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | BNPL1 | p35 | In the past year, have you used a "Buy Now Pay Later" service to buy something? | 0=No; 1=Yes | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | BNPL1 | p39 | In the past year, have you used a "Buy Now Pay Later" service to buy something? | 0=No; 1=Yes | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | BNPL1 | p58 | In the past year, have you used a "Buy Now Pay Later" service to buy something? | 0=No; 1=Yes | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | BNPL1 | p55 | In the past year, have you used a "Buy Now, Pay Later" service to buy something? | 0=No; 1=Yes | All respondents | 12,934 / 12,934 | ✓ 0 |

#### Number of current BNPL purchases

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | BNPL2 | p39 | Currently, how many different purchases using a Buy Now Pay Later service are you making payments on? | 0=None; 1; 2; 3=3 or more | BNPL1 = Yes | 1,107 / 11,874 | ✓ 0 |
| 2022 | BNPL2 | p35 | Currently, how many different purchases using a Buy Now Pay Later service are you making making payments on? | 0=None; 1; 2; 3=3 or more | BNPL1 = Yes | 1,279 / 11,667 | ✓ 0 |
| 2023 | not in file | | | | | | |
| 2024 | not in file | | | | | | |
| 2025 | not in file | | | | | | |

#### Late on a BNPL payment

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | BNPL3 | p39 | In the past year, have you ever been late making a payment for something you bought using a Buy Now Pay Later service? | 0=No; 1=Yes | BNPL1 = Yes | 1,107 / 11,874 | ✓ 0 |
| 2022 | BNPL3 | p35 | In the past year, have you ever been late making a payment for something you bought using a Buy Now Pay Later service? | 0=No; 1=Yes | BNPL1 = Yes | 1,279 / 11,667 | ✓ 0 |
| 2023 | BNPL3 | p39 | In the past year, have you ever been late making a payment for something you bought using a Buy Now Pay Later service? | 0=No; 1=Yes | BNPL1 = Yes | 1,455 / 11,400 | ✓ 0 |
| 2024 | BNPL3 | p58 | In the past year, have you ever been late making a payment for something you bought using a Buy Now Pay Later service? | 0=No; 1=Yes | BNPL1 = Yes | 1,670 / 12,295 | ✓ 0 |
| 2025 | BNPL3 | p55 | In the past year, have you ever been late making a payment for something you bought using a Buy Now, Pay Later service? | 0=No; 1=Yes | BNPL1 = Yes | 2,004 / 12,934 | ✓ 0 |

#### Charged extra for paying late

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | not in file | | | | | | |
| 2022 | BNPL3A | p35 | In the past year, have you been charged extra because you were late on a buy now pay later payment? | 0=No; 1=Yes | BNPL3 = Yes | 206 / 11,667 | ✓ 0 |
| 2023 | BNPL3A | p40 | In the past year, have you been charged extra because you were late on a buy now pay later payment? | 0=No; 1=Yes | BNPL3 = Yes | 244 / 11,400 | ✓ 0 |
| 2024 | BNPL3A | p58 | In the past year, have you been charged extra because you were late on a buy now pay later payment? | 0=No; 1=Yes | BNPL3 = Yes | 358 / 12,295 | ✓ 0 |
| 2025 | BNPL3A | p55 | In the past year, have you been charged extra because you were late on a Buy Now, Pay Later payment? | 0=No; 1=Yes | BNPL3 = Yes | 487 / 12,934 | ✓ 0 |

#### BNPL payment triggered overdraft/NSF fee

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | not in file | | | | | | |
| 2022 | not in file | | | | | | |
| 2023 | not in file | | | | | | |
| 2024 | not in file | | | | | | |
| 2025 | BNPL1A | p55 | In the past year, did any of your BNPL payments trigger an overdraft or non-sufficient-funds (NSF) fee on your bank account? | 0=No; 1=Yes | BNPL1 = Yes and BK2_f (paid an overdraft fee) = Yes | 542 / 12,934 | ✓ 0 |

#### Reasons for using BNPL (grid)

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | BNPL4_a | p39 | Cheaper - Thinking about the most recent time you used a Buy Now Pay Later service, why did you choose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 1,107 / 11,874 | ✓ 0 |
| 2021 | BNPL4_b | p39 | More convenient - Thinking about the most recent time you used a Buy Now Pay Later service, why did you choose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 1,107 / 11,874 | ✓ 0 |
| 2021 | BNPL4_c | p40 | Only way I could afford it - Thinking about the most recent time you used a Buy Now Pay Later service, why did you choose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 1,107 / 11,874 | ✓ 0 |
| 2021 | BNPL4_d | p40 | Only accepted payment method I had - Thinking about the most recent time you used a Buy Now Pay Later service, why did you choose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 1,107 / 11,874 | ✓ 0 |
| 2021 | BNPL4_e | p40 | Did not want to use a credit card - Thinking about the most recent time you used Buy Now Pay Later service, why did you choose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 1,107 / 11,874 | ✓ 0 |
| 2021 | BNPL4_f | p40 | Other (please specify) - Thinking about the most recent time you used a Buy Now Pay Later service, why did you choose to finance the the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 1,107 / 11,874 | ✓ 0 |
| 2022 | BNPL4_a | p35 | Avoid interest charges - Thinking about the most recent time you used a Buy Now Pay Later service, were each of the following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 1,279 / 11,667 | ✓ 0 |
| 2022 | BNPL4_b | p36 | Wanted to spread out payments - Thinking about the most recent time you used a Buy Now Pay Later service, were each of the following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 1,279 / 11,667 | ✓ 0 |
| 2022 | BNPL4_c | p36 | Wanted a fixed number of payments - Thinking about the most recent time you used a Buy Now Pay Later service, were each of the following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 1,279 / 11,667 | ✓ 0 |
| 2022 | BNPL4_d | p36 | Convenience - Thinking about the most recent time you used a Buy Now Pay Later service, were each of the following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 1,279 / 11,667 | ✓ 0 |
| 2022 | BNPL4_e | p36 | Only way I could afford it - Thinking about the most recent time you used a Buy Now Pay Later service, were each of the following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 1,279 / 11,667 | ✓ 0 |
| 2022 | BNPL4_f | p37 | Only accepted payment method I had - Thinking about the most recent time you used a Buy Now Pay Later service, were each of the following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 1,279 / 11,667 | ✓ 0 |
| 2022 | BNPL4_g | p37 | Did not want to use a credit card - Thinking about the most recent time you used a Buy Now Pay Later service, were each of the following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 1,279 / 11,667 | ✓ 0 |
| 2023 | BNPL4_a | p40 | Avoid interest charges - Thinking about the most recent time you used a Buy Now Pay Later service, were each of the following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 1,455 / 11,400 | ✓ 0 |
| 2023 | BNPL4_b | p40 | Wanted to spread out payments - Thinking about the most recent time you used a Pay Later service, were each of the following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 1,455 / 11,400 | ✓ 0 |
| 2023 | BNPL4_c | p41 | Wanted a fixed number of payments - Thinking about the most recent time you used a Buy Now Pay Later service, were each of the following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 1,455 / 11,400 | ✓ 0 |
| 2023 | BNPL4_d | p41 | Convenience - Thinking about the most recent time you used a Buy Now Pay Later service, were each of the following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 1,455 / 11,400 | ✓ 0 |
| 2023 | BNPL4_e | p41 | Only way I could afford it - Thinking about the most recent time you used a Buy Now Pay Later service, were each of the following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 1,455 / 11,400 | ✓ 0 |
| 2023 | BNPL4_f | p41 | Only accepted payment method I had - Thinking about the most recent time you used a Buy Now Pay Later service, were each of the following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 1,455 / 11,400 | ✓ 0 |
| 2023 | BNPL4_g | p42 | Did not want to use a credit card - Thinking about the most recent time you used a Buy Now Pay Later service, were each of the following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 1,455 / 11,400 | ✓ 0 |
| 2024 | BNPL4_a | p59 | Avoid interest charges - Thinking about the most recent time you used a Buy Now Pay Later service, were each of the following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 1,670 / 12,295 | ✓ 0 |
| 2024 | BNPL4_b | p59 | Wanted to spread out payments - Thinking about the most recent time you used a Buy Now Pay Later service, were each of the following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 1,670 / 12,295 | ✓ 0 |
| 2024 | BNPL4_c | p59 | Wanted a fixed number of payments - Thinking about the most recent time you used a Buy Now Pay Later service, were each of the following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 1,670 / 12,295 | ✓ 0 |
| 2024 | BNPL4_d | p59 | Convenience - Thinking about the most recent time you used a Buy Now Pay Later service, were each of the following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 1,670 / 12,295 | ✓ 0 |
| 2024 | BNPL4_e | p60 | Only way I could afford it - Thinking about the most recent time you used a Buy Now Pay Later service, were each of the following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 1,670 / 12,295 | ✓ 0 |
| 2024 | BNPL4_f | p60 | Only accepted payment method I had – Thinking about the most recent time you used a Buy Now Pay Later service, were each of the following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 1,670 / 12,295 | ✓ 0 |
| 2024 | BNPL4_g | p60 | Did not want to use a credit card - Thinking about the most recent time you used a Buy Now Pay Later service, were each of the following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 1,670 / 12,295 | ✓ 0 |
| 2025 | BNPL4_a | p56 | Avoid interest charges -Thinking about the most recent time you used a Buy Now, Pay Later service, were each of the following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 2,004 / 12,934 | ✓ 0 |
| 2025 | BNPL4_b | p56 | Wanted to spread out payments - Thinking about the most recent time you used a Buy Now, Pay Later service, were each of the Following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 2,004 / 12,934 | ✓ 0 |
| 2025 | BNPL4_c | p56 | Wanted a fixed number of payments - Thinking about the most recent time you used a Buy Now, Pay Later service, were each of the Following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 2,004 / 12,934 | ✓ 0 |
| 2025 | BNPL4_d | p56 | Convenience - Thinking about the most recent time you used a Buy Now, Pay Later service, were each of the following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 2,004 / 12,934 | ✓ 0 |
| 2025 | BNPL4_e | p57 | Only way I could afford it - Thinking about the most recent time you used a Buy Now, Pay Later service, were each of the following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 2,004 / 12,934 | ✓ 0 |
| 2025 | BNPL4_f | p57 | Only accepted payment method I had - Thinking about the most recent time you used a Buy Now, Pay Later service, were each of the following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 2,004 / 12,934 | ✓ 0 |
| 2025 | BNPL4_g | p57 | Did not want to use a credit card - Thinking about the most recent time you used a Buy Now, Pay Later service, were each of the Following a reason why you chose to finance the purchase in this way? | 0=No; 1=Yes | BNPL1 = Yes | 2,004 / 12,934 | ✓ 0 |

#### Most important reason

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | not in file | | | | | | |
| 2022 | not in file | | | | | | |
| 2023 | not in file | | | | | | |
| 2024 | not in file | | | | | | |
| 2025 | BNPL5 | p57 | Thinking about the most recent time you used a Buy Now Pay Later service, which of the following was the most important reason why you chose to finance the purchase in this way? | 1=Avoid interest charges; 2=Wanted to spread out payments; 3=Wanted a fixed number of payments; 4=Convenience; 5=Only way I could afford it; 6=Only accepted payment method I had; 7=Did not want to use a credit card | BNPL1 = Yes and at least one BNPL4 item = Yes | 1,935 / 12,934 | 11 (11) |

#### What BNPL was used for (select all)

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | not in file | | | | | | |
| 2022 | not in file | | | | | | |
| 2023 | not in file | | | | | | |
| 2024 | not in file | | | | | | |
| 2025 | BNPL6_a | p58 | Clothing or accessories - In the past year, when you have used Buy Now, Pay Later, which of the following have you used it for? | 0=Not selected; 1=Clothing or accessories | BNPL1 = Yes | 2,004 / 12,934 | ✓ 0 |
| 2025 | BNPL6_b | p58 | Groceries or food delivery - In the past year, when you have used Buy Now, Pay Later, which of the following have you used it for? | 0=Not selected; 1=Groceries or food delivery | BNPL1 = Yes | 2,004 / 12,934 | ✓ 0 |
| 2025 | BNPL6_c | p58 | Travel expenses (e.g. flights or hotels) -In the past year, when you have used Buy Now, Pay Later, which of the following have you used it for? | 0=Not selected; 1=Travel expenses (e.g. flights or hotels) | BNPL1 = Yes | 2,004 / 12,934 | ✓ 0 |
| 2025 | BNPL6_d | p59 | Furniture or appliances - In the past year, when you have used Buy Now, Pay Later, which of the following have you used it for? | 0=Not selected; 1=Furniture or appliances | BNPL1 = Yes | 2,004 / 12,934 | ✓ 0 |
| 2025 | BNPL6_e | p59 | Electronics - In the past year, when you have used Buy Now Pay Later, which of the following have you used it for? | 0=Not selected; 1=Electronics | BNPL1 = Yes | 2,004 / 12,934 | ✓ 0 |
| 2025 | BNPL6_f | p59 | Medical or veterinary procedures -In the past year, when you have used Buy Now, Pay Later, which of the following have you used it for? | 0=Not selected; 1=Medical or veterinary procedures | BNPL1 = Yes | 2,004 / 12,934 | ✓ 0 |
| 2025 | BNPL6_g | p59 | Other (please specify) - In the past year, when you have used Buy Now, Pay Later, which of the following have you used it for? | 0=Not selected; 1=Other (please specify) | BNPL1 = Yes | 2,004 / 12,934 | ✓ 0 |

#### Beliefs about BNPL and credit

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | not in file | | | | | | |
| 2022 | not in file | | | | | | |
| 2023 | not in file | | | | | | |
| 2024 | not in file | | | | | | |
| 2025 | BNPL7_a | p60 | It helps me build a credit history - Do you agree or disagree with the following statements about Buy Now, Pay Later? | -2=Not sure; 0=Disagree; 1=Agree | BNPL1 = Yes | 2,004 / 12,934 | ✓ 0 |
| 2025 | BNPL7_b | p60 | Making payments on time helps my credit score - Do you agree or disagree with the following statements about Buy Now, Pay Later? | -2=Not sure; 0=Disagree; 1=Agree | BNPL1 = Yes | 2,004 / 12,934 | ✓ 0 |

### Fragility

#### How well managing financially

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | B2 | p12 | Overall, which one of the following best describes how well you are managing financially these days? | 1=Finding it difficult to get by; 2=Just getting by; 3=Doing okay; 4=Living comfortably | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | B2 | p7 | Overall, which one of the following best describes how well you are managing financially these days? | 1=Finding it difficult to get by; 2=Just getting by; 3=Doing okay; 4=Living comfortably | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | B2 | p6 | Overall, which one of the following best describes how well you are managing financially these days? | 1=Finding it difficult to get by; 2=Just getting by; 3=Doing okay; 4=Living comfortably | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | B2 | p6 | Overall, which one of the following best describes how well you are managing financially these days? | 1=Finding it difficult to get by; 2=Just getting by; 3=Doing okay; 4=Living comfortably | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | B2 | p5 | Overall, which one of the following best describes how well you are managing financially these days? | 1=Finding it difficult to get by; 2=Just getting by; 3=Doing okay; 4=Living comfortably | All respondents | 12,934 / 12,934 | ✓ 0 |

#### Doing at least okay (derived from B2)

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | atleast_okay | p93 | Doing okay financially | 0=No; 1=Yes | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | atleast_okay | p86 | Doing okay financially | 0=No; 1=Yes | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | atleast_okay | p83 | Doing okay financially | 0=No; 1=Yes | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | atleast_okay | p103 | Doing okay financially | 0=No; 1=Yes | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | atleast_okay | p118 | Doing okay financially | 0=No; 1=Yes | All respondents | 12,934 / 12,934 | ✓ 0 |

#### Better/worse off than 12 months ago

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | B3 | p12 | Compared to 12 months ago, would you say that you (and your family) are better off, the same, or worse off financially? | 1=Much worse off; 2=Somewhat worse off; 3=About the same; 4=Somewhat better off; 5=Much better off | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | B3 | p7 | Compared to 12 months ago, would you say that you (and your family) are better off, the same, or worse off financially? | 1=Much worse off; 2=Somewhat worse off; 3=About the same; 4=Somewhat better off; 5=Much better off | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | B3 | p7 | Compared to 12 months ago, would you say that you (and your family) are better off, the same, or worse off financially? | 1=Much worse off; 2=Somewhat worse off; 3=About the same; 4=Somewhat better off; 5=Much better off | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | B3 | p7 | Compared to 12 months ago, would you say that you (and your family) are better off, the same, or worse off financially? | 1=Much worse off; 2=Somewhat worse off; 3=About the same; 4=Somewhat better off; 5=Much better off | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | B3 | p6 | Compared to 12 months ago, would you say that you (and your family) are better off, the same, or worse off financially? | 1=Much worse off; 2=Somewhat worse off; 3=About the same; 4=Somewhat better off; 5=Much better off | All respondents | 12,934 / 12,934 | ✓ 0 |

#### 3-month emergency fund

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | EF1 | p67 | Have you set aside emergency or rainy day funds that would cover your expenses for 3 months in case of sickness, job loss, economic downturn, or other emergencies? | 0=No; 1=Yes | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | EF1 | p63 | Have you set aside emergency or rainy day funds that would cover your expenses for 3 months in case of sickness, job loss, economic downturn, or other emergencies? | 0=No; 1=Yes | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | EF1 | p60 | Have you set aside emergency or rainy day funds that would cover your expenses for 3 months in case of sickness, job loss, economic downturn, or other emergencies? | 0=No; 1=Yes | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | EF1 | p79 | Have you set aside emergency or rainy day funds that would cover your expenses for 3 months in case of sickness, job loss, economic downturn, or other emergencies? | 0=No; 1=Yes | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | EF1 | p82 | Have you set aside emergency or rainy day funds that would cover your expenses for 3 months in case of sickness, job loss, economic downturn, or other emergencies? | 0=No; 1=Yes | All respondents | 12,934 / 12,934 | ✓ 0 |

#### Could cover 3 months if income lost

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | EF2 | p67 | If you were to lose your main source of income (for example job or government benefits), could you cover your expenses for 3 months by borrowing money, using savings, or selling assets? | 0=No; 1=Yes | EF1 = No | 4,396 / 11,874 | ✓ 0 |
| 2022 | EF2 | p64 | If you were to lose your main source of income (for example job or government benefits), could you cover your expenses for 3 months by borrowing money, using savings, or selling assets? | 0=No; 1=Yes | EF1 = No | 4,910 / 11,667 | ✓ 0 |
| 2023 | EF2 | p61 | If you were to lose your main source of income (for example job or government be | 0=No; 1=Yes | EF1 = No | 4,918 / 11,400 | ✓ 0 |
| 2024 | EF2 | p79 | If you were to lose your main source of income (for example job or government benefits), could you cover you expenses for 3 months by borrowing money, using savings, or selling assets? | 0=No; 1=Yes | EF1 = No | 5,144 / 12,295 | ✓ 0 |
| 2025 | EF2 | p82 | If you were to lose your main source of income (for example job or government benefits), could you cover you expenses for 3 months by borrowing money, using savings, or selling assets? | 0=No; 1=Yes | EF1 = No | 5,607 / 12,934 | ✓ 0 |

#### How would pay a $400 emergency expense (grid)

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | EF3_a | p67 | Put it on my credit card and pay it off in full at the next statement - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No; 1=Put it on my credit card and pay it off in full at the next statement | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 11,874 / 11,874 | ✓ 0 |
| 2021 | EF3_b | p67 | Put it on my credit card and pay it off over time - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No; 1=Put it on my credit card and pay it off over time | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 11,874 / 11,874 | ✓ 0 |
| 2021 | EF3_c | p68 | With the money currently in my checking/savings account or with cash - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No; 1=With the money currently in my checking/savings account or with cash | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 11,874 / 11,874 | ✓ 0 |
| 2021 | EF3_d | p68 | Using money from a bank loan or line of credit - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No; 1=Using money from a bank loan or line of credit | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 11,874 / 11,874 | ✓ 0 |
| 2021 | EF3_e | p68 | By borrowing from a friend or family member - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No; 1=By borrowing from a friend or family member | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 11,874 / 11,874 | ✓ 0 |
| 2021 | EF3_f | p68 | Using a payday loan, deposit advance, or overdraft - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No; 1=Using a payday loan, deposit advance, or overdraft | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 11,874 / 11,874 | ✓ 0 |
| 2021 | EF3_g | p69 | By selling something - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No; 1=By selling something | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 11,874 / 11,874 | ✓ 0 |
| 2021 | EF3_h | p69 | I wouldn't be able to pay for the expense right now - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No; 1=I wouldn't be able to pay for the expense right now | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 11,874 / 11,874 | ✓ 0 |
| 2022 | EF3_a | p64 | Put it on my credit card and pay it off in full at the next statement - Suppose that you have an emergency expense that costs (\$400/ \$500). Based on your current financial situation, how would you pay for this expense? | 0=No; 1=Put it on my credit card and pay it off in full at the next statement | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 11,667 / 11,667 | ✓ 0 |
| 2022 | EF3_b | p64 | Put it on my credit card and pay it off over time - Suppose that you have an emergency expense that costs (\$400/\$500). Based on your current financial situation, how would you pay for this expense? | 0=No; 1=Put it on my credit card and pay it off over time | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 11,667 / 11,667 | ✓ 0 |
| 2022 | EF3_c | p64 | With the money currently in my checking/ savings account or with cash - Suppose that you have an emergency expense that costs (\$400/\$500). Based on your current financial situation, how would you pay for this expense? | 0=No; 1=With the money currently in my checking/savings account or with cash | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 11,667 / 11,667 | ✓ 0 |
| 2022 | EF3_d | p65 | Using money from a bank loan or line of credit - Suppose that you have an emergency expense that costs (\$400/\$500). Based on your current financial situation, how would you pay for this expense? | 0=No; 1=Using money from a bank loan or line of credit | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 11,667 / 11,667 | ✓ 0 |
| 2022 | EF3_e | p65 | By borrowing from a friend or family member - Suppose that you have an emergency expense that costs (\$400/\$500). Based on your current financial situation, how would you pay for this expense? | 0=No; 1=By borrowing from a friend or family member | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 11,667 / 11,667 | ✓ 0 |
| 2022 | EF3_f | p65 | Using a payday loan, deposit advance, or overdraft - Suppose that you have an emergency expense that costs (\$400/\$500). Based on your current financial situation, how would you pay for this expense? | 0=No; 1=Using a payday loan, deposit advance, or overdraft | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 11,667 / 11,667 | ✓ 0 |
| 2022 | EF3_g | p65 | By selling something - Suppose that you have an emergency expense that costs (\$400/\$500). Based on your current financial situation, how would you pay for this expense? | 0=No; 1=By selling something | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 11,667 / 11,667 | ✓ 0 |
| 2022 | EF3_h | p66 | I wouldn't be able to pay for the expense right now - Suppose that you have an emergency expense that costs (\$400/\$500). Based on your current financial situation, how would you pay for this expense? | 0=No; 1=I wouldn't be able to pay for the expense right now | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 11,667 / 11,667 | ✓ 0 |
| 2023 | EF3_a | p61 | Put it on my credit card and pay it off in full at the next statement - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No, did not do this; 1=Put it on my credit card and pay it off in full at the next statement | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 11,400 / 11,400 | ✓ 0 |
| 2023 | EF3_b | p61 | Put it on my credit card and pay it off over time - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No, did not do this; 1=Put it on my credit card and pay it off over time | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 11,400 / 11,400 | ✓ 0 |
| 2023 | EF3_c | p61 | With the money currently in my checking/savings account or with cash - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No, did not do this; 1=With the money currently in my checking/savings account or with cash | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 11,400 / 11,400 | ✓ 0 |
| 2023 | EF3_d | p62 | Using money from a bank loan or line of credit - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No, did not do this; 1=Using money from a bank loan or line of credit | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 11,400 / 11,400 | ✓ 0 |
| 2023 | EF3_e | p62 | By borrowing from a friend or family member - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No, did not do this; 1=By borrowing from a friend or family member | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 11,400 / 11,400 | ✓ 0 |
| 2023 | EF3_f | p62 | Using a payday loan, deposit advance, or overdraft - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No, did not do this; 1=Using a payday loan, deposit advance, or overdraft | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 11,400 / 11,400 | ✓ 0 |
| 2023 | EF3_g | p63 | By selling something - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No, did not do this; 1=By selling something | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 11,400 / 11,400 | ✓ 0 |
| 2023 | EF3_h | p63 | I wouldn't be able to pay for the expense right now - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No, did not do this; 1=I wouldn't be able to pay for the expense right now | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 11,400 / 11,400 | ✓ 0 |
| 2024 | EF3_a | p80 | Put it on my credit card and pay it off in full at the next statement – Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, How would you pay for this expense? | 0=No; 1=Yes | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 12,295 / 12,295 | ✓ 0 |
| 2024 | EF3_b | p80 | Put it on my credit card and pay it off over time - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No; 1=Yes | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 12,295 / 12,295 | ✓ 0 |
| 2024 | EF3_c | p80 | With the money currently in my checking/savings account or with cash - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No; 1=Yes | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 12,295 / 12,295 | ✓ 0 |
| 2024 | EF3_d | p80 | Using money from a bank loan or line of credit - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No; 1=Yes | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 12,295 / 12,295 | ✓ 0 |
| 2024 | EF3_e | p81 | By borrowing from a friend or family member - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No; 1=Yes | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 12,295 / 12,295 | ✓ 0 |
| 2024 | EF3_f | p81 | Using a payday loan, deposit advance, or overdraft - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No; 1=Yes | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 12,295 / 12,295 | ✓ 0 |
| 2024 | EF3_g | p81 | By selling something - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No; 1=Yes | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 12,295 / 12,295 | ✓ 0 |
| 2024 | EF3_h | p81 | I wouldn't be able to pay for the expense right now - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No; 1=Yes | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 12,295 / 12,295 | ✓ 0 |
| 2025 | EF3_a | p82 | Put it on my credit card and pay it off in full at the next statement – Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, How would you pay for this expense? | 0=No; 1=Yes | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 12,934 / 12,934 | ✓ 0 |
| 2025 | EF3_b | p82 | Put it on my credit card and pay it off over time - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No; 1=Yes | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 12,934 / 12,934 | ✓ 0 |
| 2025 | EF3_c | p83 | With the money currently in my checking/savings account or with cash - an emergency expenseSuppose that you have that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No; 1=Yes | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 12,934 / 12,934 | ✓ 0 |
| 2025 | EF3_d | p83 | Using money from a bank loan or line of credit - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No; 1=Yes | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 12,934 / 12,934 | ✓ 0 |
| 2025 | EF3_e | p83 | By borrowing from a friend or family member - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No; 1=Yes | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 12,934 / 12,934 | ✓ 0 |
| 2025 | EF3_f | p83 | Using a payday loan, deposit advance, or overdraft - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No; 1=Yes | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 12,934 / 12,934 | ✓ 0 |
| 2025 | EF3_g | p84 | By selling something - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No; 1=Yes | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 12,934 / 12,934 | ✓ 0 |
| 2025 | EF3_h | p84 | I wouldn't be able to pay for the expense right now - Suppose that you have an emergency expense that costs \$400. Based on your current financial situation, how would you pay for this expense? | 0=No; 1=Yes | All respondents (2022: amount is \$400 or \$500 by DOV_EF_amount) | 12,934 / 12,934 | ✓ 0 |

#### Would cover $400 with cash or equivalent (derived)

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | pay_casheqv | p94 | Would handle \$400 expense with cash or equivalent | 0=No; 1=Yes | All respondents; 2022: DOV_EF_amount = \$400 only | 11,874 / 11,874 | ✓ 0 |
| 2022 | pay_casheqv | p85 | Would handle \$400 expense with cash or equivalent | 0=No; 1=Yes | All respondents; 2022: DOV_EF_amount = \$400 only | 9,293 / 11,667 | ✓ 0 |
| 2023 | pay_casheqv | p83 | Would handle \$400 expense with cash or equivalent | 0=No; 1=Yes | All respondents; 2022: DOV_EF_amount = \$400 only | 11,400 / 11,400 | ✓ 0 |
| 2024 | pay_casheqv | p103 | Would handle \$400 expense with cash or equivalent | 0=No; 1=Yes | All respondents; 2022: DOV_EF_amount = \$400 only | 12,295 / 12,295 | ✓ 0 |
| 2025 | pay_casheqv | p118 | Would handle \$400 expense with cash or equivalent | 0=No; 1=Yes | All respondents; 2022: DOV_EF_amount = \$400 only | 12,934 / 12,934 | ✓ 0 |

#### Able to pay all bills in full this month

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | EF5A | p69 | Which best describes your ability to pay all of your bills in full this month? | 0=Can't pay some bills; 1=Able to pay all bills | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | EF5A | p66 | Which best describes your ability to pay all of your bills in full this month? | 0=Can't pay some bills; 1=Able to pay all bills | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | not in file | | | | | | |
| 2024 | not in file | | | | | | |
| 2025 | not in file | | | | | | |

#### Effect of $400 expense on paying other bills

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | EF5B | p69 | How would a \$400 emergency expense that you had to pay impact your ability to pay your other bills this month? | 0=Could not pay some bills; 1=Would still be able to pay all bills | EF5A = Able to pay all bills | 10,400 / 11,874 | ✓ 0 |
| 2022 | EF5B | p66 | How would a (\$400/\$500) emergency expense that you had to pay impact your ability to pay your other bills this month? | 0=Could not pay some bills; 1=Would still be able to pay all bills | EF5A = Able to pay all bills | 9,715 / 11,667 | ✓ 0 |
| 2023 | not in file | | | | | | |
| 2024 | not in file | | | | | | |
| 2025 | not in file | | | | | | |

#### Bills expected to skip this month (grid)

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | EF6A_a | p70 | Rent or mortgage - Are you expecting to be unable to pay or only make a partial payment on each of the following bills this month? | 0=No; 1=Yes | EF5A = Can't pay some bills | 1,474 / 11,874 | ✓ 0 |
| 2021 | EF6A_b | p70 | Credit card - Are you expecting to be unable to pay or only make a partial payment on each of the following bills this month? | 0=No; 1=Yes | EF5A = Can't pay some bills | 1,474 / 11,874 | ✓ 0 |
| 2021 | EF6A_c | p70 | Water, gas, or electric bill - Are you expecting to be unable to pay or only make a partial payment on each of the following bills this month? | 0=No; 1=Yes | EF5A = Can't pay some bills | 1,474 / 11,874 | ✓ 0 |
| 2021 | EF6A_d | p70 | Phone or cable bill - Are you expecting to be unable to pay or only make a partial payment on each of the following bills this month? | 0=No; 1=Yes | EF5A = Can't pay some bills | 1,474 / 11,874 | ✓ 0 |
| 2021 | EF6A_e | p70 | Car payment - Are you expecting to be unable to pay or only make a partial payment on each of the following bills this month? | 0=No; 1=Yes | EF5A = Can't pay some bills | 1,474 / 11,874 | ✓ 0 |
| 2021 | EF6A_f | p71 | Student loan - Are you expecting to be unable to pay or only make a partial payment on each of the following bills this month? | 0=No; 1=Yes | EF5A = Can't pay some bills | 1,474 / 11,874 | ✓ 0 |
| 2021 | EF6A_g | p71 | Other bills - Are you expecting to be unable to pay or only make a partial payment on each of the following bills this month? | 0=No; 1=Yes | EF5A = Can't pay some bills | 1,474 / 11,874 | ✓ 0 |
| 2022 | EF6A_a | p66 | Rent or mortgage - Are you expecting to be unable to pay or only make a partial payment on each of the following bills this month? | 0=No; 1=Yes | EF5A = Can't pay some bills | 1,952 / 11,667 | ✓ 0 |
| 2022 | EF6A_b | p66 | Credit card - Are you expecting to be unable to pay or only make a partial payment on each of the following bills this month? | 0=No; 1=Yes | EF5A = Can't pay some bills | 1,952 / 11,667 | ✓ 0 |
| 2022 | EF6A_c | p67 | Water, gas, or electric bill - Are you expecting to be unable to pay or only make a partial payment on each of the following bills this month? | 0=No; 1=Yes | EF5A = Can't pay some bills | 1,952 / 11,667 | ✓ 0 |
| 2022 | EF6A_d | p67 | Phone or cable bill - Are you expecting to be unable to pay or only make a partial payment on each of the following bills this month? | 0=No; 1=Yes | EF5A = Can't pay some bills | 1,952 / 11,667 | ✓ 0 |
| 2022 | EF6A_e | p67 | Car payment - Are you expecting to be unable to pay or only make a partial payment on each of the following bills this month? | 0=No; 1=Yes | EF5A = Can't pay some bills | 1,952 / 11,667 | ✓ 0 |
| 2022 | EF6A_f | p67 | Student loan - Are you expecting to be unable to pay or only make a partial payment on each of the following bills this month? | 0=No; 1=Yes | EF5A = Can't pay some bills | 1,952 / 11,667 | ✓ 0 |
| 2022 | EF6A_g | p67 | Other bills - Are you expecting to be unable to pay or only make a partial payment on each of the following bills this month? | 0=No; 1=Yes | EF5A = Can't pay some bills | 1,952 / 11,667 | ✓ 0 |
| 2023 | not in file | | | | | | |
| 2024 | not in file | | | | | | |
| 2025 | not in file | | | | | | |

#### Bills would skip after $400 expense (grid)

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | EF6B_a | p71 | Rent or mortgage - Which of the following bills would you likely skip paying, or make only a partial payment on, if you had a \$400 emergency expense that you had to pay? | 0=No; 1=Yes | EF5B = Could not pay some bills | 1,076 / 11,874 | ✓ 0 |
| 2021 | EF6B_b | p71 | Credit card - Which of the following bills would you likely skip paying, or make only a partial payment on, if you had a \$400 emergency expense that you had to pay? | 0=No; 1=Yes | EF5B = Could not pay some bills | 1,076 / 11,874 | ✓ 0 |
| 2021 | EF6B_c | p72 | Water, gas, or electric bill - Which of the following bills would you likely skip paying, or only make a partial payment on, if you had a \$400 emergency expense that you had to pay? | 0=No; 1=Yes | EF5B = Could not pay some bills | 1,076 / 11,874 | ✓ 0 |
| 2021 | EF6B_d | p72 | Phone or cable bill - Which of the following bills would you likely skip paying, or make only a partial payment on, if you had a \$400 emergency expense that you had to pay? | 0=No; 1=Yes | EF5B = Could not pay some bills | 1,076 / 11,874 | ✓ 0 |
| 2021 | EF6B_e | p72 | Car payment - Which of the following bills would you likely skip paying, or make only a partial payment on, if you had a \$400 emergency expense that you had to pay? | 0=No; 1=Yes | EF5B = Could not pay some bills | 1,076 / 11,874 | ✓ 0 |
| 2021 | EF6B_f | p72 | Student loan - Which of the following bills would you likely skip paying, or make only a partial payment on, if you had a \$400 emergency expense that you had to pay? | 0=No; 1=Yes | EF5B = Could not pay some bills | 1,076 / 11,874 | ✓ 0 |
| 2021 | EF6B_g | p72 | Other bills - Which of the following bills would you likely skip paying, or make only a partial payment on, if you had a \$400 emergency expense that you had to pay? | 0=No; 1=Yes | EF5B = Could not pay some bills | 1,076 / 11,874 | ✓ 0 |
| 2022 | EF6B_a | p68 | Rent or mortgage - Which of the following bills would you likely skip paying, or make only a partial payment on, if you had a (\$400/ \$500) emergency expense that you had to pay? | 0=No; 1=Yes | EF5B = Could not pay some bills | 1,154 / 11,667 | ✓ 0 |
| 2022 | EF6B_b | p68 | Credit card - Which of the following bills would you likely skip paying, or make only a partial payment on, if you had a (\$400/\$500) emergency expense that you had to pay? | 0=No; 1=Yes | EF5B = Could not pay some bills | 1,154 / 11,667 | ✓ 0 |
| 2022 | EF6B_c | p68 | Water, gas, or electric bill - Which of the following bills would you likely skip paying, or make only a partial payment on, if you had a (\$400/\$500) emergency expense that you had to pay? | 0=No; 1=Yes | EF5B = Could not pay some bills | 1,154 / 11,667 | ✓ 0 |
| 2022 | EF6B_d | p68 | Phone or cable bill - Which of the following bills would you likely skip paying, or make only a partial payment on, if you had a (\$400/ \$500) emergency expense that you had to pay? | 0=No; 1=Yes | EF5B = Could not pay some bills | 1,154 / 11,667 | ✓ 0 |
| 2022 | EF6B_e | p69 | Car payment -Which of the following bills would you likely skip paying, or make only a partial payment on, if you had a (\$400/\$500) emergency expense that you had to pay? | 0=No; 1=Yes | EF5B = Could not pay some bills | 1,154 / 11,667 | ✓ 0 |
| 2022 | EF6B_f | p69 | Student loan - Which of the following bills would you likely skip paying, or make only a partial payment on, if you had a (\$400/\$500) emergency expense that you had to pay? | 0=No; 1=Yes | EF5B = Could not pay some bills | 1,154 / 11,667 | ✓ 0 |
| 2022 | EF6B_g | p69 | Other bills - Which of the following bills would you likely skip paying, or make only a partial payment on, if you had a (\$400/\$500) emergency expense that you had to pay? | 0=No; 1=Yes | EF5B = Could not pay some bills | 1,154 / 11,667 | ✓ 0 |
| 2023 | not in file | | | | | | |
| 2024 | not in file | | | | | | |
| 2025 | not in file | | | | | | |

#### Paid all non-card bills in full last month

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | not in file | | | | | | |
| 2022 | not in file | | | | | | |
| 2023 | EF5C | p63 | Other than any credit card bills you may have, did you pay all your bills in full last month? | 0=No; 1=Yes | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | EF5C | p82 | Other than any credit card bills you may have, did you pay all your bills in full last month? | 0=No; 1=Yes | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | EF5C | p84 | Other than any credit card bills you may have, did you pay all your bills in full last month? | 0=No; 1=Yes | All respondents | 12,934 / 12,934 | ✓ 0 |

#### Had bills difficult to pay last month

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | not in file | | | | | | |
| 2022 | not in file | | | | | | |
| 2023 | not in file | | | | | | |
| 2024 | not in file | | | | | | |
| 2025 | EF5D | p84 | Did you have any bills that you had difficulty paying last month? | 0=No; 1=Yes | EF5C = Yes | 11,135 / 12,934 | ✓ 0 |

#### How handled each bill last month (grid)

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | not in file | | | | | | |
| 2022 | not in file | | | | | | |
| 2023 | EF6C_a | p63 | Rent or mortgage - How did you handle each of the following types of bills last month? | -9=Does not apply (do not have bill); 0=Made partial payment or did not pay; 1=Paid in full | EF5C = No | 1,566 / 11,400 | ✓ 0 |
| 2023 | EF6C_b | p64 | Water, gas, and electric bills - How did you handle each of the following types of bills last month? | -9=Does not apply (do not have bill); 0=Made partial payment or did not pay; 1=Paid in full | EF5C = No | 1,566 / 11,400 | ✓ 0 |
| 2023 | EF6C_c | p64 | Phone, internet, and cable bills - How did you handle each of the following types of bills last month? | -9=Does not apply (do not have bill); 0=Made partial payment or did not pay; 1=Paid in full | EF5C = No | 1,566 / 11,400 | ✓ 0 |
| 2023 | EF6C_d | p64 | Car payment - How did you handle each of the following types of bills last month? | -9=Does not apply (do not have bill); 0=Made partial payment or did not pay; 1=Paid in full | EF5C = No | 1,566 / 11,400 | ✓ 0 |
| 2024 | EF6C_a | p82 | Rent or mortgage - How did you handle each of the following types of bills last month? | -9=Does not apply (do not have bill); 0=Made partial payment or did not pay; 1=Paid in full | EF5C = No | 1,667 / 12,295 | ✓ 0 |
| 2024 | EF6C_b | p82 | Water, gas, and electric bills - How did you handle each of the following types of bills last month? | -9=Does not apply (do not have bill); 0=Made partial payment or did not pay; 1=Paid in full | EF5C = No | 1,667 / 12,295 | ✓ 0 |
| 2024 | EF6C_c | p83 | Phone, internet, and cable bills - How did you handle each of the following type of bills last month? | -9=Does not apply (do not have bill); 0=Made partial payment or did not pay; 1=Paid in full | EF5C = No | 1,667 / 12,295 | ✓ 0 |
| 2024 | EF6C_d | p83 | Car payment - How did you handle each of the following types of bills last month? | -9=Does not apply (do not have bill); 0=Made partial payment or did not pay; 1=Paid in full | EF5C = No | 1,667 / 12,295 | ✓ 0 |
| 2025 | not in file | | | | | | |

#### Actions when had difficulty paying a bill (grid)

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | not in file | | | | | | |
| 2022 | not in file | | | | | | |
| 2023 | not in file | | | | | | |
| 2024 | not in file | | | | | | |
| 2025 | EF8_a | p85 | Paid a bill late -In addition to not paying the a bill in full, did you do each of following when you had difficulty paying a bill last month? | 0=Not selected; 1=Paid a bill late | EF5C = No or EF5D = Yes | 3,408 / 12,934 | ✓ 0 |
| 2025 | EF8_b | p85 | Negotiated a lower payment or more time to pay -In addition to not paying a bill in the following whenfull, did you do each of you had difficulty paying a bill last month? | 0=Not selected; 1=Negotiated a lower payment or more time to pay | EF5C = No or EF5D = Yes | 3,408 / 12,934 | ✓ 0 |
| 2025 | EF8_c | p85 | Cut back on other expenses - In addition to not paying a bill in full, did you do each of the following when you had difficulty paying a bill last month? | 0=Not selected; 1=Cut back on other expenses | EF5C = No or EF5D = Yes | 3,408 / 12,934 | ✓ 0 |
| 2025 | EF8_d | p85 | Increased income, for example, by working overtime or taking an extra job - In addition to not paying a bill in full, did you do each the following when you had difficulty of paying a bill last month? | 0=Not selected; 1=Increased income, for example, by working overtime or taking an extra job | EF5C = No or EF5D = Yes | 3,408 / 12,934 | ✓ 0 |
| 2025 | EF8_e | p86 | Used money from savings or a retirement account - In addition to not paying a bill in full, did you do each of the following when you had difficulty paying a bill last month? | 0=Not selected; 1=Used money from savings or a retirement account | EF5C = No or EF5D = Yes | 3,408 / 12,934 | ✓ 0 |
| 2025 | EF8_f | p86 | Used a credit card that I will pay off over time - In addition to not paying a bill in full, did you do each of the following when you had difficulty paying a bill last month? | 0=Not selected; 1=Used a credit card that I will pay off over time | EF5C = No or EF5D = Yes | 3,408 / 12,934 | ✓ 0 |
| 2025 | EF8_g | p86 | Borrowed or received money from friends or family - In addition to not paying a bill in full, did you do each of the following when you had difficulty paying a bill last month? | 0=Not selected; 1=Borrowed or received money from friends or family | EF5C = No or EF5D = Yes | 3,408 / 12,934 | ✓ 0 |
| 2025 | EF8_h | p87 | Took out another type of loan, such as a payday loan or personal loan - In addition to not paying a bill in full, did you do each of the following when you had difficulty paying a bill last month? | 0=Not selected; 1=Took out another type of loan, such as a payday loan or personal loan | EF5C = No or EF5D = Yes | 3,408 / 12,934 | ✓ 0 |
| 2025 | EF8_i | p87 | Sold or pawned something - In addition to not paying a bill in full, did you do each of the following when you had difficulty paying a bill last month? | 0=Not selected; 1=Sold or pawned something | EF5C = No or EF5D = Yes | 3,408 / 12,934 | ✓ 0 |
| 2025 | EF8_j | p87 | Other - In addition to not paying a bill in full, did you do each of the following when you had difficulty paying a bill last month? | 0=Not selected; 1=Other | EF5C = No or EF5D = Yes | 3,408 / 12,934 | ✓ 0 |

#### Largest emergency expense from savings (5 brackets)

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | not in file | | | | | | |
| 2022 | EF7 | p69 | Based on your current financial situation, what is the largest emergency expense that you could handle right now using only your savings? | 1=Under \$100; 2=\$100 to \$499; 3=\$500 to \$999; 4=\$1,000 to \$1,999; 5=\$2,000 or more | All respondents; 2025: dov_ef7 = 1 only | 11,667 / 11,667 | ✓ 0 |
| 2023 | EF7 | p64 | Based on your current financial situation, what is the largest emergency expense that you could handle right now using only your savings? | 1=Under \$100; 2=\$100 to \$499; 3=\$500 to \$999; 4=\$1,000 to \$1,999; 5=\$2,000 or more | All respondents; 2025: dov_ef7 = 1 only | 11,400 / 11,400 | ✓ 0 |
| 2024 | EF7 | p83 | Based on your current financial situation, what is the largest emergency expense that you could handle right now using only your savings? | 1=Under \$100; 2=\$100 to \$499; 3=\$500 to \$999; 4=\$1,000 to \$1,999; 5=\$2,000 or more | All respondents; 2025: dov_ef7 = 1 only | 12,295 / 12,295 | ✓ 0 |
| 2025 | EF7 | p88 | Based on your current financial situation, that what is the largest emergency expense you could handle right now using only your savings? | 1=Under \$100; 2=\$100 to \$499; 3=\$500 to \$999; 4=\$1,000 to \$1,999; 5=\$2,000 or more | All respondents; 2025: dov_ef7 = 1 only | 6,453 / 12,934 | ✓ 0 |

#### Largest emergency expense from savings (6 brackets)

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | not in file | | | | | | |
| 2022 | not in file | | | | | | |
| 2023 | not in file | | | | | | |
| 2024 | not in file | | | | | | |
| 2025 | EF7A | p88 | Based on your current financial situation, that what is the largest emergency expense you could handle right now using only your savings? | 1=Under \$100; 2=\$100 to \$499; 3=\$500 to \$999; 4=\$1,000 to \$1,999; 5=\$2,000 to \$4,999; 6=\$5,000 or more | dov_ef7 = 0 | 6,481 / 12,934 | ✓ 0 |

#### Income volatility

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | I9 | p60 | In the past 12 months, which one of the following best describes your and your spouse's or partner's income? | 1=Roughly the same amount each month; 2=Occasionally varies from month to month; 3=Varies quite often from month to month | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | I9 | p55 | In the past 12 months, which one of the following best describes your (and/or your spouse's or partner's) income? | 1=Roughly the same amount each month; 2=Occasionally varies from month to month; 3=Varies quite often from month to month | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | I9 | p57 | In the past 12 months, which one of the following best describes your [and your spouse's or partner's] income? | 1=Roughly the same amount each month; 2=Occasionally varies from month to month; 3=Varies quite often from month to month | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | I9 | p76 | In the past 12 months, which one of the following best describes your (and your spouse's or partner's) income? | 1=Roughly the same amount each month; 2=Occasionally varies from month to month; 3=Varies quite often from month to month | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | I9 | p78 | In the past 12 months, which one of the following best describes your (and your spouse's or partner's) income? | 1=Roughly the same amount each month; 2=Occasionally varies from month to month; 3=Varies quite often from month to month | All respondents | 12,934 / 12,934 | ✓ 0 |

#### Struggled to pay bills because income varies

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | I12 | p60 | Because your income varies, have you and your spouse or partner struggled to pay your bills in the past 12 months? | 0=No; 1=Yes | I9 = varies (occasionally or often) | 3,067 / 11,874 | ✓ 0 |
| 2022 | I12 | p55 | Because your income varies, have you (and your spouse or partner) struggled to pay your bills in the past 12 months? | 0=No; 1=Yes | I9 = varies (occasionally or often) | 3,128 / 11,667 | ✓ 0 |
| 2023 | I12 | p58 | Because your income varies, have you [and your spouse or partner] struggled to pay your bills in the past 12 months? | 0=No; 1=Yes | I9 = varies (occasionally or often) | 3,031 / 11,400 | ✓ 0 |
| 2024 | I12 | p76 | Because your income varies, have you and your spouse or partner struggled to pay your bills in the past 12 months? | 0=No; 1=Yes | I9 = varies (occasionally or often) | 3,354 / 12,295 | ✓ 0 |
| 2025 | I12 | p79 | Because your income varies, have you and your spouse or partner struggled to pay your bills in the past 12 months? | 0=No; 1=Yes | I9 = varies (occasionally or often) | 3,631 / 12,934 | ✓ 0 |

#### Has unpaid credit card debt

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | C3 | p38 | Do you currently have any outstanding unpaid credit card debt? | 0=No; 1=Yes | C2A = Yes | 10,349 / 11,874 | ✓ 0 |
| 2022 | C3 | p34 | Do you currently have any credit card debt that you do not expect to pay in full with your next payment? | 0=No; 1=Yes | C2A = Yes | 10,004 / 11,667 | ✓ 0 |
| 2023 | not in file | | | | | | |
| 2024 | not in file | | | | | | |
| 2025 | not in file | | | | | | |

#### How handled credit card bills last month

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | not in file | | | | | | |
| 2022 | not in file | | | | | | |
| 2023 | C3P | p39 | Last month, how did you handle your credit card bills? | -9=did not use any of my credit cards so had no balances; 1=paid at least the minimum payment on all credit cards; 2=did not pay or paid less than the minimum payment on at least one card | C2A = Yes | 9,633 / 11,400 | ✓ 0 |
| 2024 | C3P | p57 | Last month, how did you handle your credit card bills? | -9=did not use any of my credit cards so had no balances; 1=paid at least the minimum payment on all credit cards; 2=did not pay or paid less than the minimum payment on at least one card | C2A = Yes | 10,349 / 12,295 | ✓ 0 |
| 2025 | C3P | p54 | Last month, how did you handle your credit card bills? | -9=Did not use any of my credit cards so had no balances; 1=Paid at least the minimum payment on all credit cards; 2=Did not pay or paid less than the minimum payment on at least one card | C2A = Yes | 10,759 / 12,934 | ✓ 0 |

#### How often carried a card balance

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | C4A | p38 | In the past 12 months, how frequently have you carried an unpaid balance on one or more of your credit cards? | 0=Never carried an unpaid balance (always pay in full); 1=Once; 2=Some of the time; 3=Most or all of the time | C2A = Yes | 10,349 / 11,874 | ✓ 0 |
| 2022 | C4A | p34 | In the past 12 months, how frequently have you carried an unpaid balance on one or more of your credit cards? | 0=Never carried an unpaid balance (always pay in full); 1=Once; 2=Some of the time; 3=Most or all of the time | C2A = Yes | 10,004 / 11,667 | ✓ 0 |
| 2023 | C4A | p39 | In the past 12 months, how frequently have you carried an unpaid balance on one or more of your credit cards? | 0=Never carried an unpaid balance (always pay in full); 1=Once; 2=Some of the time; 3=Most or all of the time | C2A = Yes | 9,633 / 11,400 | ✓ 0 |
| 2024 | C4A | p58 | In the past 12 months, how frequently have you carried an unpaid balance on one or more of your credit cards? | 0=Never carried an unpaid balance (always pay in full); 1=Once; 2=Some of the time; 3=Most or all of the time | C2A = Yes | 10,349 / 12,295 | ✓ 0 |
| 2025 | C4A | p54 | In the past 12 months, how frequently have you carried an unpaid balance on one or more of your credit cards? | 0=Never carried an unpaid balance (always pay in full); 1=Once; 2=Some of the time; 3=Most or all of the time | C2A = Yes | 10,759 / 12,934 | ✓ 0 |

#### Has bank account

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | BK1 | p34 | Do you and/or your spouse or partner currently have a checking, savings or money market account? | 0=No; 1=Yes | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | BK1 | p28 | Do you (and/or your spouse or partner) currently have a checking, savings or money market account? | 0=No; 1=Yes | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | BK1 | p32 | Do you (and/or your spouse or partner) currently have a checking, savings or money market account? | 0=No; 1=Yes | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | BK1 | p47 | Do you (and/or your spouse or partner) currently have a checking, savings, or money market account? | 0=No; 1=Yes | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | BK1 | p39 | Do you [and/or your spouse or partner] currently have a checking, savings, or money market account? | 0=No; 1=Yes | All respondents | 12,934 / 12,934 | ✓ 0 |

#### Alternative financial services (grid)

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | BK2_a | p35 | Purchase a money order from a place other than a bank - In the past 12 months, did you and/or spouse or partner: | 0=No; 1=Yes | All respondents; BK2_f: BK1 = Yes | 11,874 / 11,874 | ✓ 0 |
| 2021 | BK2_b | p35 | Cash a check at a place other than a bank - In the past 12 months, did you and/or spouse or partner: | 0=No; 1=Yes | All respondents; BK2_f: BK1 = Yes | 11,874 / 11,874 | ✓ 0 |
| 2021 | BK2_c | p35 | Take out a payday loan or payday advance - In the past 12 months, did you and/or your spouse or partner: | 0=No; 1=Yes | All respondents; BK2_f: BK1 = Yes | 11,874 / 11,874 | ✓ 0 |
| 2021 | BK2_d | p35 | Take out a pawn shop loan or an auto title loan - In the past 12 months, did you and/or your spouse or partner: | 0=No; 1=Yes | All respondents; BK2_f: BK1 = Yes | 11,874 / 11,874 | ✓ 0 |
| 2021 | BK2_e | p35 | Obtain a tax refund advance to receive your refund faster - In the past 12 months, did you and/or your spouse or partner: | 0=No; 1=Yes | All respondents; BK2_f: BK1 = Yes | 11,874 / 11,874 | ✓ 0 |
| 2021 | BK2_f | p36 | Pay an overdraft fee on a bank account - In the past 12 months, did you and/or spouse or partner: | 0=No; 1=Yes | BK1 = Yes | 11,357 / 11,874 | ✓ 0 |
| 2022 | BK2_a | p28 | Purchase a money order from a place other than a bank - In the past 12 months, did you (and or your spouse or partner): | 0=No; 1=Yes | All respondents; BK2_f: BK1 = Yes | 11,667 / 11,667 | ✓ 0 |
| 2022 | BK2_b | p29 | Cash a check at a place other than a bank - In the past 12 months, did you (and or your spouse or partner): | 0=No; 1=Yes | All respondents; BK2_f: BK1 = Yes | 11,667 / 11,667 | ✓ 0 |
| 2022 | BK2_c | p29 | Take out a payday loan or payday advance - In the past 12 months, did you (and or your spouse or partner): | 0=No; 1=Yes | All respondents; BK2_f: BK1 = Yes | 11,667 / 11,667 | ✓ 0 |
| 2022 | BK2_d | p29 | Take out a pawn shop loan or an auto title loan - In the past 12 months, did you (and or your spouse or partner): | 0=No; 1=Yes | All respondents; BK2_f: BK1 = Yes | 11,667 / 11,667 | ✓ 0 |
| 2022 | BK2_e | p29 | Obtain a tax refund advance to receive your refund faster - In the past 12 months, did you (and or your spouse or partner): | 0=No; 1=Yes | All respondents; BK2_f: BK1 = Yes | 11,667 / 11,667 | ✓ 0 |
| 2022 | BK2_f | p29 | Pay an overdraft fee on a bank account - In the past 12 months, did you (and or your spouse or partner): | 0=No; 1=Yes | BK1 = Yes | 11,127 / 11,667 | ✓ 0 |
| 2023 | BK2_a | p32 | Purchase a money order from a place other than a bank - In the past 12 months, did you (and/or your spouse or partner): | 0=No; 1=Yes | All respondents; BK2_f: BK1 = Yes | 11,400 / 11,400 | ✓ 0 |
| 2023 | BK2_b | p33 | Cash a check at a place other than a bank - In the past 12 months, did you (and/or your spouse or partner): | 0=No; 1=Yes | All respondents; BK2_f: BK1 = Yes | 11,400 / 11,400 | ✓ 0 |
| 2023 | BK2_c | p33 | Take out a payday loan or payday advance - In the past 12 months, did you (and/or your spouse or partner): | 0=No; 1=Yes | All respondents; BK2_f: BK1 = Yes | 11,400 / 11,400 | ✓ 0 |
| 2023 | BK2_d | p33 | Take out a pawn shop loan or an auto title loan - In the past 12 months, did you (and/ or your spouse or partner): | 0=No; 1=Yes | All respondents; BK2_f: BK1 = Yes | 11,400 / 11,400 | ✓ 0 |
| 2023 | BK2_e | p33 | Obtain a tax refund advance to receive your refund faster - In the past 12 months, did you (and/or you spouse or partner): | 0=No; 1=Yes | All respondents; BK2_f: BK1 = Yes | 11,400 / 11,400 | ✓ 0 |
| 2023 | BK2_f | p34 | Pay an overdraft fee on a bank account - In the past 12 months, did you (and/or your spouse or partner): | 0=No; 1=Yes | BK1 = Yes | 10,817 / 11,400 | ✓ 0 |
| 2024 | BK2_a | p47 | Purchase a money order from a place other than a bank - In the past 12 months, did you (and/or your spouse or partner): | 0=No; 1=Yes | All respondents; BK2_f: BK1 = Yes | 12,295 / 12,295 | ✓ 0 |
| 2024 | BK2_b | p47 | Cash a check at a place other than a bank - In the past 12 months, did you (and/or your spouse or partner): | 0=No; 1=Yes | All respondents; BK2_f: BK1 = Yes | 12,295 / 12,295 | ✓ 0 |
| 2024 | BK2_c | p47 | Take out a payday loan or payday advance - In the past 12 months, did you (and/or your spouse or partner): | 0=No; 1=Yes | All respondents; BK2_f: BK1 = Yes | 12,295 / 12,295 | ✓ 0 |
| 2024 | BK2_d | p47 | Take out a pawn shop loan or an auto title loan - In the past 12 months, did you (and/or your spouse or partner): | 0=No; 1=Yes | All respondents; BK2_f: BK1 = Yes | 12,295 / 12,295 | ✓ 0 |
| 2024 | BK2_e | p48 | Obtain a tax refund advance to receive your refund faster - In the past 12 months, did you (and/or your spouse or partner): | 0=No; 1=Yes | All respondents; BK2_f: BK1 = Yes | 12,295 / 12,295 | ✓ 0 |
| 2024 | BK2_f | p48 | Pay an overdraft fee on a bank account - In the past 12 months, did you (and/or your spouse or partner): | 0=No; 1=Yes | BK1 = Yes | 11,647 / 12,295 | ✓ 0 |
| 2025 | BK2_a | p39 | Purchase a money order from a place other than a bank - In the past 12 months, did you (and/or your spouse or partner): | 0=No; 1=Yes | All respondents; BK2_f: BK1 = Yes | 12,934 / 12,934 | ✓ 0 |
| 2025 | BK2_b | p40 | Cash a check at a place other than a bank - In the past 12 months, did you (and/or your spouse or partner): | 0=No; 1=Yes | All respondents; BK2_f: BK1 = Yes | 12,934 / 12,934 | ✓ 0 |
| 2025 | BK2_c | p40 | Take out a payday loan or payday advance - In the past 12 months, did you (and/or your spouse or partner): | 0=No; 1=Yes | All respondents; BK2_f: BK1 = Yes | 12,934 / 12,934 | ✓ 0 |
| 2025 | BK2_d | p40 | Take out a pawn shop loan or an auto title loan - In the past 12 months, did you and/or your spouse or partner): | 0=No; 1=Yes | All respondents; BK2_f: BK1 = Yes | 12,934 / 12,934 | ✓ 0 |
| 2025 | BK2_e | p40 | Obtain a tax refund advance to receive your refund faster - In the past 12 months, did you (and/or your spouse or partner): | 0=No; 1=Yes | All respondents; BK2_f: BK1 = Yes | 12,934 / 12,934 | ✓ 0 |
| 2025 | BK2_f | p41 | Pay an overdraft fee on a bank account - In the past 12 months, did you (and/or your spouse or partner): | 0=No; 1=Yes | BK1 = Yes | 12,236 / 12,934 | ✓ 0 |

#### Applied for credit

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | A0 | p36 | In the past 12 months, have you applied for any credit (such as a credit card, higher credit card limit, mortgage, refinance, student loan, personal loan, or other loan)? | 0=No; 1=Yes | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | A0 | p30 | In the past 12 months have you applied for any credit (such as a credit card, higher credit card limit, mortgage, refinance, student loan, personal loan, or other loan)? | 0=No; 1=Yes | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | A0 | p34 | In the past 12 months have you applied for any credit (such as a credit card, higher credit card limit, mortgage, refinance, student loan, personal loan, or other loan)? | 0=No; 1=Yes | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | A0 | p53 | In the past 12 months have you applied for any credit (such as a credit card, higher credit card limit, mortgage, refinance, student loan, personal loan, or other loan)? | 0=No; 1=Yes | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | A0 | p49 | In the past 12 months have you applied for any credit (such as a credit card, higher credit card limit, mortgage, refinance, student loan, personal loan, or other loan)? | 0=No; 1=Yes | All respondents | 12,934 / 12,934 | ✓ 0 |

#### Credit outcomes (grid)

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | A1_a | p36 | Turned down for credit - In the past 12 months, has each of the following happened to you: | 0=No; 1=Yes | A0 = Yes | 4,413 / 11,874 | ✓ 0 |
| 2021 | A1_b | p37 | Approved for credit, but were not given as much credit as you applied for - In the past 12 months, has each of the following happened to you: | 0=No; 1=Yes | A0 = Yes | 4,413 / 11,874 | ✓ 0 |
| 2021 | A1_c | p37 | Put off applying for credit because you thought you might be turned down - In the past 12 months, has each of the following happened to you: | 0=No; 1=Yes | A0 = Yes | 4,413 / 11,874 | ✓ 0 |
| 2022 | A1_a | p31 | Turned down for credit - In the past 12 months, has each of the following happened to you: | 0=No; 1=Yes | A0 = Yes | 4,016 / 11,667 | ✓ 0 |
| 2022 | A1_b | p32 | Approved for credit, but were not given as much credit as you applied for - In the past 12 months, has each of the following happened to you: | 0=No; 1=Yes | A0 = Yes | 4,016 / 11,667 | ✓ 0 |
| 2022 | A1_c | p32 | Put off applying for credit because you thought you might be turned down - In the past 12 months, has each of the following happened to you: | 0=No; 1=Yes | A0 = Yes | 4,016 / 11,667 | ✓ 0 |
| 2023 | A1_a | p36 | Turned down for credit - In the past 12 months, has each of the following happen to you: | 0=No; 1=Yes | A0 = Yes | 4,007 / 11,400 | ✓ 0 |
| 2023 | A1_b | p36 | Approved for credit, but were not given as much credit as you applied for - In the past 12 months, has each of the following happened to you: | 0=No; 1=Yes | A0 = Yes | 4,007 / 11,400 | ✓ 0 |
| 2023 | A1_c | p37 | Put off applying for credit because you thought you might be turned down - In the past 12 months, has each of the following happened to you: | 0=No; 1=Yes | A0 = Yes | 4,007 / 11,400 | ✓ 0 |
| 2024 | A1_a | p54 | Turned down for credit - In the past 12 months, has each of the following happened to you: | 0=No; 1=Yes | A0 = Yes | 4,111 / 12,295 | ✓ 0 |
| 2024 | A1_b | p55 | Approved for credit, but were not given as much credit as you applied for - In the past 12 months, has each of the following happened to you: | 0=No; 1=Yes | A0 = Yes | 4,111 / 12,295 | ✓ 0 |
| 2024 | A1_c | p55 | Put off applying for credit because you thought you might be turned down - In the past 12 months, has each of the following happened to you: | 0=No; 1=Yes | A0 = Yes | 4,111 / 12,295 | ✓ 0 |
| 2025 | A1_a | p51 | Turned down for credit - In the past 12 months, has each of the following happened to you: | 0=No; 1=Yes | A0 = Yes | 4,276 / 12,934 | ✓ 0 |
| 2025 | A1_b | p51 | Approved for credit, but were not given as much credit as you applied for - In the past 12 months, has each of the following happened to you: | 0=No; 1=Yes | A0 = Yes | 4,276 / 12,934 | ✓ 0 |
| 2025 | A1_c | p52 | Put off applying for credit because you thought you might be turned down - In the past 12 months, has each of the following happened to you: | 0=No; 1=Yes | A0 = Yes | 4,276 / 12,934 | ✓ 0 |

#### Behind on rent in past year

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | R11 | p29 | Have you been behind on your rent at any time in the past year? | 0=No; 1=Yes | GH1 = Pay rent | 2,894 / 11,874 | ✓ 0 |
| 2022 | R11 | p25 | Have you been behind on your rent at any time in the past year? | 0=No; 1=Yes | GH1 = Pay rent | 2,931 / 11,667 | ✓ 0 |
| 2023 | R11 | p28 | Have you been behind on your rent at any time in the past year? | 0=No; 1=Yes | GH1 = Pay rent | 2,896 / 11,400 | ✓ 0 |
| 2024 | R11 | p42 | Have you been behind on your rent at any time in the past year? | 0=No; 1=Yes | GH1 = Pay rent | 3,206 / 12,295 | ✓ 0 |
| 2025 | R11 | p36 | Have you been behind on your rent at any time in the past year? | 0=No; 1=Yes | GH1 = Pay rent | 3,426 / 12,934 | ✓ 0 |

### Controls

#### Has a credit card

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | C2A | p37 | Do you currently have at least one credit card? | 0=No; 1=Yes | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | C2A | p34 | Do you currently have at least one credit card? | 0=No; 1=Yes | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | C2A | p38 | Do you currently have at least one credit card? Please do not include debit cards or prepaid cards. | 0=No; 1=Yes | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | C2A | p57 | Do you currently have at least one credit card? Please do not include debit cards or prepaid cards. | 0=No; 1=Yes | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | C2A | p54 | Do you currently have at least one credit card? Please do not include debit cards or prepaid cards. | 0=No; 1=Yes | All respondents | 12,934 / 12,934 | ✓ 0 |

#### Household income (SHED, brackets)

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | I40 | p58 | Which of the following categories best describes the total income that you and/or your spouse or partner received from all sources, before taxes and deductions, in the past 12 months? | 0=\$0; 1=\$1 to \$4,999; 2=\$5,000 to \$14,999; 3=\$15,000 to \$24,999; 4=\$25,000 to \$39,999; 5=\$40,000 to \$49,999; 6=\$50,000 to \$74,999; 7=\$75,000 to \$99,999; 8=\$100,000 to \$149,999; 9=\$150,000 to \$199,999; 10=\$200,000 or higher | All respondents (see notes for 2022) | 11,874 / 11,874 | ✓ 0 |
| 2022 | I40 | p53 | Which of the following categories best describes the total income that you (and/or your spouse or partner) received from all sources, before taxes and deductions, in the past 12 months? | 0=\$0; 1=\$1 to \$4,999; 2=\$5,000 to \$14,999; 3=\$15,000 to \$24,999; 4=\$25,000 to \$39,999; 5=\$40,000 to \$49,999; 6=\$50,000 to \$74,999; 7=\$75,000 to \$99,999; 8=\$100,000 to \$149,999; 9=\$150,000 to \$199,999; 10=\$200,000 or higher | All respondents (see notes for 2022) | 11,667 / 11,667 | ✓ 0 |
| 2023 | I40 | p56 | Which category represents your [and your spouse/partner's] total combined income in the past 12 months? | CSV labels (codebook prints no full tabulation): \$10,000 to \$14,999; \$100,000 to \$149,999; \$15,000 to \$19,999; \$150,000 to \$199,999; \$20,000 to \$24,999; \$200,000 or more; \$25,000 to \$29,999; \$30,000 to \$34,999; \$35,000 to \$39,999; \$40,000 to \$49,999; \$5,000 to \$9,999; \$50,000 to \$59,999; \$60,000 to \$74,999; \$75,000 to \$99,999; Less than \$5,000 | All respondents (see notes for 2022) | 11,400 / 11,400 | ✓ 0 |
| 2024 | I40 | p75 | Which category represents yo ur (and your spouse/partner's) total combined income in the past 12 months? | CSV labels (codebook prints no full tabulation): \$10,000 to \$14,999; \$100,000 to \$149,999; \$15,000 to \$19,999; \$150,000 to \$199,999; \$20,000 to \$24,999; \$200,000 or more; \$25,000 to \$29,999; \$30,000 to \$34,999; \$35,000 to \$39,999; \$40,000 to \$49,999; \$5,000 to \$9,999; \$50,000 to \$59,999; \$60,000 to \$74,999; \$75,000 to \$99,999; Less than \$5,000 | All respondents (see notes for 2022) | 12,295 / 12,295 | ✓ 0 |
| 2025 | I40 | p75 | Which category represents your (and your spouse/partner's) total combined income in the past 12 months? | CSV labels (codebook prints no full tabulation): \$10,000 to \$14,999; \$100,000 to \$149,999; \$15,000 to \$19,999; \$150,000 to \$199,999; \$20,000 to \$24,999; \$200,000 or more; \$25,000 to \$29,999; \$30,000 to \$34,999; \$35,000 to \$39,999; \$40,000 to \$49,999; \$5,000 to \$9,999; \$50,000 to \$59,999; \$60,000 to \$74,999; \$75,000 to \$99,999; Less than \$5,000 | All respondents (see notes for 2022) | 12,934 / 12,934 | ✓ 0 |

#### Household income, 4 categories (derived from I40)

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | inc_4cat_50k | p93 | Income (I40) - 4 cat - <25,25-49,50-99,100+ | 1=Less than \$25,000; 2=\$25,000-\$49,999; 3=\$50,000-\$99,999; 4=\$100,000 or more | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | inc_4cat_50k | p85 | Income (I40) - 4 cat - <25,25-49,50-99,100+ | 1=Less than \$25,000; 2=\$25,000-\$49,999; 3=\$50,000-\$99,999; 4=\$100,000 or more | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | inc_4cat_50k | p82 | Income (I40) - 4 cat - <25,25- 49,50- 99,100+ | 1=Less than \$25,000; 2=\$25,000-\$49,999; 3=\$50,000-\$99,999; 4=\$100,000 or more | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | inc_4cat_50k | p102 | Income (I40) - 4 cat - <25,25–49,50–99,100+ | 1=Less than \$25,000; 2=\$25,000–\$49,999; 3=\$50,000–\$99,999; 4=\$100,000 or more | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | inc_4cat_50k | p118 | Income (I40) - 4 cat - <25,25–49,50–99,100+ | 1=Less than \$25,000; 2=\$25,000–\$49,999; 3=\$50,000–\$99,999; 4=\$100,000 or more | All respondents | 12,934 / 12,934 | ✓ 0 |

#### Household income (Ipsos profile)

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | ppinc7 | p85 | Household Income | 1=Less than \$10,000; 2=\$10,000 to \$24,999; 3=\$25,000 to \$49,999; 4=\$50,000 to \$74,999; 5=\$75,000 to \$99,999; 6=\$100,000 to \$149,999; 7=\$150,000 or more | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | ppinc7 | p77 | Household Income | 1=Less than \$10,000; 2=\$10,000 to \$24,999; 3=\$25,000 to \$49,999; 4=\$50,000 to \$74,999; 5=\$75,000 to \$99,999; 6=\$100,000 to \$149,999; 7=\$150,000 or more | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | ppinc7 | p72 | Household Income | 1=Less than \$10,000; 2=\$10,000 to \$24,999; 3=\$25,000 to \$49,999; 4=\$50,000 to \$74,999; 5=\$75,000 to \$99,999; 6=\$100,000 to \$149,999; 7=\$150,000 or more | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | ppinc7 | p93 | Household Income | 1=Less than \$10,000; 2=\$10,000 to \$24,999; 3=\$25,000 to \$49,999; 4=\$50,000 to \$74,999; 5=\$75,000 to \$99,999; 6=\$100,000 to \$149,999; 7=\$150,000 or more | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | ppinc7 | p100 | Household Income | 1=Less than \$10,000; 2=\$10,000 to \$24,999; 3=\$25,000 to \$49,999; 4=\$50,000 to \$74,999; 5=\$75,000 to \$99,999; 6=\$100,000 to \$149,999; 7=\$150,000 or more | All respondents | 12,934 / 12,934 | ✓ 0 |

#### Age

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | ppage | p83 | Age | numeric/continuous (no value labels) | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | ppage | p75 | Age | numeric/continuous (no value labels) | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | ppage | p70 | Age | numeric/continuous (no value labels) | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | ppage | p90 | Age | numeric/continuous (no value labels) | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | ppage | p97 | Age | numeric/continuous (no value labels) | All respondents | 12,934 / 12,934 | ✓ 0 |

#### Age, 7 categories

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | ppagecat | p83 | Age - 7 Categories | 1=18-24; 2=25-34; 3=35-44; 4=45-54; 5=55-64; 6=65-74; 7=75+ | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | ppagecat | p75 | Age - 7 Categories | 1=18-24; 2=25-34; 3=35-44; 4=45-54; 5=55-64; 6=65-74; 7=75+ | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | ppagecat | p70 | Age - 7 Categories | 1=18- 24; 2=25-34; 3=35-44; 4=45-54; 5=55-64; 6=65-74; 7=75+ | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | ppagecat | p91 | Age - 7 Categories | 1=18-24; 2=25-34; 3=35-44; 4=45-54; 5=55-64; 6=65-74; 7=75+ | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | ppagecat | p98 | Age - 7 Categories | 1=18-24; 2=25-34; 3=35-44; 4=45-54; 5=55-64; 6=65-74; 7=75+ | All respondents | 12,934 / 12,934 | ✓ 0 |

#### Highest education (SHED)

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | ED0 | p40 | What is the highest level of school you have completed or the highest degree you have received? | 1=Less than high school degree; 2=High school degree or GED; 3=Some college but no degree (including currently enrolled in college); 4=Certificate or technical degree; 5=Associate degree; 6=Bachelor's degree; 7=Master's degree; 8=Professional degree (e.g., MBA, MD, JD); 9=Doctoral degree | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | ED0 | p40 | What is the highest level of school you have completed or the highest degree you have received? | 1=Less than high school degree; 2=High school degree or GED; 3=Some college but no degree (including currently enrolled in college); 4=Certificate or technical degree; 5=Associate degree; 6=Bachelor's degree; 7=Master's degree; 8=Professional degree (e.g., MBA, MD, JD); 9=Doctoral degree | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | ED0 | p43 | What is the highest level of school you have completed or the highest degree you have received? | 1=Less than high school degree; 2=High school degree or GED; 3=Some college but no degree (including currently enrolled in college); 4=Certificate or technical degree; 5=Associate degree; 6=Bachelor's degree; 7=Master's degree; 8=Professional degree (e.g., MBA, MD, JD); 9=Doctoral degree | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | ED0 | p62 | What is the highest level of school you have completed or the highest degree you have received? | 1=Less than high school degree; 2=High school degree or GED; 3=Some college but no degree (including currently enrolled in college); 4=Certificate or technical degree; 5=Associate degree; 6=Bachelor's degree; 7=Master's degree; 8=Professional degree (e.g., MBA, MD, JD); 9=Doctoral degree | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | ED0 | p61 | What is the highest level of school you have completed or the highest degree you have received? | 1=Less than high school degree; 2=High school degree or GED; 3=Some college but no degree (including currently enrolled in college); 4=Certificate or technical degree; 5=Associate degree; 6=Bachelor's degree; 7=Master's degree; 8=Professional degree (e.g., MBA, MD, JD); 9=Doctoral degree | All respondents | 12,934 / 12,934 | ✓ 0 |

#### Education, 4 categories (profile)

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | ppeducat | p83 | Education (4 Categories) | 1=No high school diploma or GED; 2=High school graduate (high school diploma or the equivalent GED); 3=Some college or Associate's degree; 4=Bachelor's degree or higher | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | ppeducat | p75 | Education (4 Categories) | 1=No high school diploma or GED; 2=High school graduate (high school diploma or the equivalent GED); 3=Some college or Associate's degree; 4=Bachelor's degree or higher | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | ppeducat | p71 | Education (4 Categories) | 1=No high school diploma or GED; 2=High school graduate (high school diploma or the equivalent GED); 3=Some college or Associate's degree; 4=Bachelor's degree or higher | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | ppeducat | p91 | Education (4 Categories) | 1=No high school diploma or GED; 2=High school graduate (high school diploma or the equivalent GED); 3=Some college or Associate's degree; 4=Bachelor's degree or higher | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | ppeducat | p98 | Education (4 Categories) | 1=No high school diploma or GED; 2=High school graduate (high school diploma or the equivalent GED); 3=Some college or Associate's degree; 4=Bachelor's degree or higher | All respondents | 12,934 / 12,934 | ✓ 0 |

#### Gender (profile)

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | ppgender | p84 | Gender | 1=Male; 2=Female | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | ppgender | p76 | Gender | 1=Male; 2=Female | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | ppgender | p72 | Gender | 1=Male; 2=Female | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | ppgender | p92 | Gender | 1=Male; 2=Female | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | ppgender | p99 | Gender | 1=Male; 2=Female | All respondents | 12,934 / 12,934 | ✓ 0 |

#### Race/ethnicity (profile)

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | ppethm | p84 | Race / Ethnicity | 1=White, Non-Hispanic; 2=Black, Non-Hispanic; 3=Other, Non-Hispanic; 4=Hispanic; 5=2+ Races, Non-Hispanic | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | ppethm | p76 | Race / Ethnicity | 1=White, Non-Hispanic; 2=Black, Non-Hispanic; 3=Other, Non-Hispanic; 4=Hispanic; 5=2+ Races, Non-Hispanic | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | ppethm | p72 | Race / Ethnicity | 1=White, Non-Hispanic; 2=Black, Non-Hispanic; 3=Other, Non- Hispanic; 4=Hispanic; 5=2+ Races, Non-Hispanic | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | ppethm | p92 | Race / Ethnicity | 1=White, Non-Hispanic; 2=Black, Non-Hispanic; 3=Other, Non-Hispanic; 4=Hispanic; 5=2+ Races, Non-Hispanic | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | ppethm | p99 | Race / Ethnicity | 1=White, Non-Hispanic; 2=Black, Non-Hispanic; 3=Other, Non-Hispanic; 4=Hispanic; 5=2+ Races, Non-Hispanic | All respondents | 12,934 / 12,934 | ✓ 0 |

#### Marital status (profile)

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | ppmarit5 | p85 | Marital Status | 1=Now married; 2=Widowed; 3=Divorced; 4=Separated; 5=Never married | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | ppmarit5 | p77 | Marital Status | 1=Now married; 2=Widowed; 3=Divorced; 4=Separated; 5=Never married | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | ppmarit5 | p73 | Marital Status | 1=Now married; 2=Widowed; 3=Divorced; 4=Separated; 5=Never married | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | ppmarit5 | p93 | Marital Status | 1=Now married; 2=Widowed; 3=Divorced; 4=Separated; 5=Never married | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | ppmarit5 | p100 | Marital Status | 1=Now married; 2=Widowed; 3=Divorced; 4=Separated; 5=Never married | All respondents | 12,934 / 12,934 | ✓ 0 |

#### Household size (profile)

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | pphhsize | p84 | Household Size | CSV labels (codebook prints no full tabulation): 1; 10; 2; 3; 4; 5; 6; 7; 8; 9 | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | pphhsize | p76 | Household Size | CSV labels (codebook prints no full tabulation): 1; 10; 2; 3; 4; 5; 6; 7; 8; 9 | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | pphhsize | p72 | Household Size | CSV labels (codebook prints no full tabulation): 1; 10; 2; 3; 4; 5; 6; 7; 8; 9 | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | pphhsize | p92 | Household Size | CSV labels (codebook prints no full tabulation): 1; 10; 2; 3; 4; 5; 6; 7; 8; 9 | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | pphhsize | p99 | Household Size | CSV labels (codebook prints no full tabulation): 1; 10; 11; 12; 2; 3; 4; 5; 6; 7; 8; 9 | All respondents | 12,934 / 12,934 | ✓ 0 |

#### Children 0-17 in household (profile)

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | ppkid017 | p86 | Presence of Household Members - Children 0-17 | CSV labels (codebook prints no full tabulation): 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | ppkid017 | p78 | Presence of Household Members - Children 0-17 | CSV labels (codebook prints no full tabulation): 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | ppkid017 | p74 | Presence of Household Members - Children 0-17 | 0; 1; 2; 3; 4; 5; 6; 7; 8 | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | ppkid017 | p95 | Presence of Household Members - Children 0-17 | CSV labels (codebook prints no full tabulation): 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | ppkid017 | p101 | Presence of Household Members - Children 0-17 | CSV labels (codebook prints no full tabulation): 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 | All respondents | 12,934 / 12,934 | ✓ 0 |

#### Employment status (profile)

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | ppemploy | p84 | Current Employment Status | 1=Working full-time; 2=Working part-time; 3=Not working | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | ppemploy | p76 | Current Employment Status | 1=Working full-time; 2=Working part-time; 3=Not working | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | ppemploy | p71 | Current Employment Status | 1=Working full-time; 2=Working part-time; 3=Not working | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | ppemploy | p92 | Current Employment Status | 1=Working full-time; 2=Working part-time; 3=Not working | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | ppemploy | p99 | Current Employment Status | 1=Working full-time; 2=Working part-time; 3=Not working | All respondents | 12,934 / 12,934 | ✓ 0 |

#### Metro status (profile)

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | ppmsacat | p85 | MSA Status | 0=Non-Metro; 1=Metro | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | ppmsacat | p77 | MSA Status | 0=Non-Metro; 1=Metro | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | ppmsacat | p73 | MSA Status | 0=Non-Metro; 1=Metro | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | ppmsacat | p93 | MSA Status | 0=Non-Metro; 1=Metro | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | ppmsacat | p100 | MSA Status | 0=Non-Metro; 1=Metro | All respondents | 12,934 / 12,934 | ✓ 0 |

#### Census region (profile)

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | ppreg4 | p85 | Region 4 - Based on State of Residence | 1=Northeast; 2=Midwest; 3=South; 4=West | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | ppreg4 | p77 | Region 4 - Based on State of Residence | 1=Northeast; 2=Midwest; 3=South; 4=West | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | ppreg4 | p73 | Region 4 - Based on State of Residence | 1=Northeast; 2=Midwest; 3=South; 4=West | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | ppreg4 | p94 | Region 4 - Based on State of Residence | 1=Northeast; 2=Midwest; 3=South; 4=West | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | ppreg4 | p100 | Region 4 - Based on State of Residence | 1=Northeast; 2=Midwest; 3=South; 4=West | All respondents | 12,934 / 12,934 | ✓ 0 |

#### Housing tenure

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | GH1 | p25 | This section will ask some questions about your housing situation. Do you: | 1=Own your home with a mortgage or loan; 2=Own your home free and clear (without a mortgage or loan); 3=Pay rent; 4=Neither own nor pay rent | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | GH1 | p21 | This section will ask some questions about your home and your car. Do you (and/or your spouse or partner): | 1=Own your home with a mortgage or loan; 2=Own your home free and clear (without a mortgage or loan); 3=Pay rent; 4=Neither own nor pay rent | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | GH1 | p23 | This section will ask some questions about your home. Do you (and/or your spouse or partner): | 1=Own your home with a mortgage or loan; 2=Own your home free and clear (without a mortgage or loan); 3=Pay rent; 4=Neither own nor pay rent | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | GH1 | p35 | This section will ask some questions about your home. Do you (and/or your spouse or partner): | 1=Own your home with a mortgage or loan; 2=Own your home free and clear (without a mortgage or loan); 3=Pay rent; 4=Neither own nor pay rent | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | GH1 | p30 | This section will ask some questions about your home. Do you (and/or your spouse or partner): | 1=Own your home with a mortgage or loan; 2=Own your home free and clear (without a mortgage or loan); 3=Pay rent; 4=Neither own nor pay rent | All respondents | 12,934 / 12,934 | ✓ 0 |

### Design

#### Respondent ID (links waves)

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | shedid | p2 | SHED ID | numeric/continuous (no value labels) | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | shedid | p2 | SHED ID | numeric/continuous (no value labels) | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | shedid | p2 | SHED ID | numeric/continuous (no value labels) | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | shedid | p2 | SHED ID | numeric/continuous (no value labels) | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | shedid | p2 | SHED ID | numeric/continuous (no value labels) | All respondents | 12,934 / 12,934 | ✓ 0 |

#### Cross-section weight, sample scale

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | weight | p2 | Post-stratification weight - Main qualified respondents scaled to sample size | numeric/continuous (no value labels) | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | weight | p2 | Post-stratification weight - Main qualified respondents scaled to sample size | numeric/continuous (no value labels) | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | weight | p3 | Post-stratification weight - Main qualified respondents scaled to sample size | numeric/continuous (no value labels) | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | weight | p2 | Post -stratification weight - Main qualified respondents scaled to sample size | numeric/continuous (no value labels) | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | weight | p2 | Post-stratification weight - Main qualified respondents scaled to sample size | numeric/continuous (no value labels) | All respondents | 12,934 / 12,934 | ✓ 0 |

#### Cross-section weight, population scale

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | weight_pop | p2 | Post-stratification weight - Main qualified respondents scaled to U.S. population | numeric/continuous (no value labels) | All respondents | 11,874 / 11,874 | ✓ 0 |
| 2022 | weight_pop | p2 | Post-stratification weight - Main qualified respondents scaled to U.S. population | numeric/continuous (no value labels) | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | weight_pop | p3 | Post-stratification weight - Main qualified respondents scaled to U.S. population | numeric/continuous (no value labels) | All respondents | 11,400 / 11,400 | ✓ 0 |
| 2024 | weight_pop | p3 | Post -stratification weight - Main qualified respondents scaled to U.S. population | numeric/continuous (no value labels) | All respondents | 12,295 / 12,295 | ✓ 0 |
| 2025 | weight_pop | p2 | Post-stratification weight - Main qualified respondents scaled to U.S. population | numeric/continuous (no value labels) | All respondents | 12,934 / 12,934 | ✓ 0 |

#### Panel weight, sample scale

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | panel_weight | p2 | Post-stratification weight - Main recontact respondents scaled to sample size | numeric/continuous (no value labels) | Recontacts from prior wave | 3,772 / 11,874 | n/a |
| 2022 | panel_weight | p3 | Post-stratification weight - Main recontact respondents scaled to sample size | numeric/continuous (no value labels) | Recontacts from prior wave | 3,752 / 11,667 | n/a |
| 2023 | panel_weight | p3 | Post-stratification weight - Main recontact respondents scaled to sample size | numeric/continuous (no value labels) | Recontacts from prior wave | 3,870 / 11,400 | n/a |
| 2024 | panel_weight | p3 | Post -stratification weight - Main recontact respondents scaled to sample size | numeric/continuous (no value labels) | Recontacts from prior wave | 4,015 / 12,295 | n/a |
| 2025 | panel_weight | p2 | Post-stratification weight - Main recontact respondents scaled to sample size | numeric/continuous (no value labels) | Recontacts from prior wave | 4,419 / 12,934 | n/a |

#### Panel weight, population scale

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | panel_weight_pop | p3 | Post-stratification weight - Main recontact respondents scaled to U.S. population | numeric/continuous (no value labels) | Recontacts from prior wave | 3,772 / 11,874 | n/a |
| 2022 | panel_weight_pop | p3 | Post-stratification weight - Main recontact respondents scaled to U.S. population | numeric/continuous (no value labels) | Recontacts from prior wave | 3,752 / 11,667 | n/a |
| 2023 | panel_weight_pop | p3 | Post-stratification weight - Main recontact respondents scaled to U.S. population | numeric/continuous (no value labels) | Recontacts from prior wave | 3,870 / 11,400 | n/a |
| 2024 | panel_weight_pop | p3 | Post -stratification weight - Main recontact respondents scaled to U.S. population | numeric/continuous (no value labels) | Recontacts from prior wave | 4,015 / 12,295 | n/a |
| 2025 | panel_weight_pop | p3 | Post-stratification weight - Main recontact respondents scaled to U.S. population | numeric/continuous (no value labels) | Recontacts from prior wave | 4,419 / 12,934 | n/a |

#### Split ballot: $400 vs $500 emergency expense

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | not in file | | | | | | |
| 2022 | DOV_EF_amount | p74 | Flag - amount of hypothetical emergency expense in emergency fund questions | CSV labels (codebook prints no full tabulation): \$400; \$500 | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | not in file | | | | | | |
| 2024 | not in file | | | | | | |
| 2025 | not in file | | | | | | |

#### Split ballot: which income question

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | not in file | | | | | | |
| 2022 | income_question | p85 | Which income question respondent was given | CSV labels (codebook prints no full tabulation): I39; I40 (refused I39); Neither (zero income based on I0A) | All respondents | 11,667 / 11,667 | ✓ 0 |
| 2023 | not in file | | | | | | |
| 2024 | not in file | | | | | | |
| 2025 | not in file | | | | | | |

#### Split ballot: EF7 vs EF7A

| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |
|---|---|---|---|---|---|---|---|
| 2021 | not in file | | | | | | |
| 2022 | not in file | | | | | | |
| 2023 | not in file | | | | | | |
| 2024 | not in file | | | | | | |
| 2025 | dov_ef7 | p87 | EF7 sample split | 0; 1 | All respondents | 12,934 / 12,934 | ✓ 0 |

### 2023 vs 2024: late payment block, word for word

| Var | Wording 2023 = 2024 | Codes 2023 = 2024 | Asked of (data check) | Preceding items | Differences |
|---|---|---|---|---|---|
| BNPL1 | identical | identical | 2023: 0 mismatches (0 imputed); 2024: 0 mismatches (0 imputed) | 2023: C4A; 2024: C4A | none |
| BNPL3 | identical | identical | 2023: 0 mismatches (0 imputed); 2024: 0 mismatches (0 imputed) | 2023: BNPL1; 2024: BNPL1 | none |
| BNPL3A | identical | identical | 2023: 0 mismatches (0 imputed); 2024: 0 mismatches (0 imputed) | 2023: BNPL3; 2024: BNPL3 | none |

### 2025 panel recontacts and BNPL use (generated)

| Group | n (unweighted) | Share of recontacts (panel_weight) |
|---|---|---|
| 2025 recontacts (panel_weight nonmissing) | 4,419 | 1.000 |
| linked to a 2024 record by shedid | 4,419 | 1.000 |
| used BNPL in 2024 (2024 BNPL1 = Yes) | 601 | 0.140 |
| used BNPL in 2025 (2025 BNPL1 = Yes) | 630 | 0.147 |
| used BNPL in both years | 392 | 0.091 |
| used BNPL in 2024 or 2025 | 839 | 0.196 |
| 2025 BNPL users who were late in 2025 (BNPL3 = Yes) | 147 | 0.034 |
| 2024 users who were late in 2024 (BNPL3 = Yes) | 131 | 0.031 |

<!-- END GENERATED -->
