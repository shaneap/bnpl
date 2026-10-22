# Decisions log

Every judgment call (recodes, exclusions, missing value handling), dated, with the reason.

## 2026-10-22 (Phase 0–1)

- **Raw data out of git, manifest in.** `.gitignore` excludes `data/raw/*` except `data/raw/MANIFEST.md`, so hashes and dates are versioned while the files are not. Reason: the spec asks for a manifest of untracked raw files.
- **Download date source.** `MANIFEST.md` takes the download date from the macOS quarantine timestamp Chrome wrote at download (all files: 2026-10-22). The CSVs' modification times (Nov 2025 to Jul 2026) are the dates stored inside the Fed's zip files, not download dates. Both are recorded.
- **Added `pypdf==6.21.2`.** Needed to read the codebook PDFs; `pdftotext` is not installed.
- **"Who was asked" is inferred from the data.** The codebooks don't print routing and the questionnaire appendix isn't in `data/raw/`. Each rule in `scripts/phase1_checks.py` must select exactly the rows with an answer; mismatches are allowed only where the item or its parent was imputed (`_iflag` = 1). Reason: this is checkable against the files we have. Weakness: it can't distinguish "not asked" from a missing-by-design rule we didn't think of.
- **Panel linkage on `shedid`.** 2025 recontacts (nonmissing `panel_weight`) are linked to 2024 by `shedid`. The codebook does not state that `shedid` persists across waves, but all 4,419 recontacts match a unique 2024 `shedid`. One 2025 row without a panel weight also matches a 2024 `shedid`; it is not treated as a recontact, because the codebook defines recontacts by the panel weight.
- **Open for Phase 2 (not decided):** keep or drop imputed values (`_iflag` = 1); how to treat the 2022 $500 arm of EF3/EF5B/EF6B; how to treat the 2025 EF7/EF7A split; income harmonization across the 2023 I40 bracket change (`inc_4cat_50k` is the candidate).
