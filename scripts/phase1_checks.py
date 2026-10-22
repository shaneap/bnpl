"""Phase 1 checks: variable inventory detail, skip-logic verification, 2023 vs 2024 late
payment comparison, and 2025 panel BNPL counts.

Wording and codes come from the codebook PDFs (scripts/codebook.py). "Asked of" rules are
checked against the public CSVs: the rule must select exactly the rows with a nonmissing
answer. Counts here are UNWEIGHTED unless a column says otherwise.

Outputs
  docs/variable_inventory.md            generated section between the GENERATED markers
  reports/tables/phase1_universe.csv    one row per item x wave: rule check results
  reports/tables/phase1_panel_bnpl.csv  2025 recontacts by BNPL use in 2024 and 2025
"""
import dataclasses
import difflib
import hashlib
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bnpl.paths import INTERIM, ROOT, TABLES, WAVES, codebook_pdf, raw_csv  # noqa: E402
from codebook import parse  # noqa: E402

INVENTORY = ROOT / "docs" / "variable_inventory.md"
BEGIN, END = "<!-- BEGIN GENERATED: scripts/phase1_checks.py -->", "<!-- END GENERATED -->"


# Universe rules. Each takes a wave's DataFrame (all columns as str, "" = missing) and
# returns the boolean mask of rows that should have been asked.
# Each rule carries `parents`: the items it conditions on, whose imputation flags can explain
# a mismatch (an imputed parent answer does not route the respondent).
def rule(parents):
    def wrap(fn):
        fn.parents = parents
        return fn
    return wrap


@rule([])
def everyone(d):
    return pd.Series(True, index=d.index)


def eq(col, val):
    return rule([col])(lambda d: d[col] == val)


def ne(col, val):
    return rule([col])(lambda d: d[col] != val)


@rule(["BNPL1", "BK2_f"])
def bnpl_users_with_overdraft(d):
    return (d.BNPL1 == "Yes") & (d.BK2_f == "Yes")


@rule(["BNPL1", "BNPL4_"])
def bnpl_users_any_reason(d):
    reasons = [c for c in d.columns if c.startswith("BNPL4_") and not c.endswith("_iflag")]
    return (d.BNPL1 == "Yes") & (d[reasons] == "Yes").any(axis=1)


@rule(["EF5C", "EF5D"])
def ef8_universe(d):
    return (d.EF5C == "No") | (d.EF5D == "Yes")


@rule([])
def ef7_universe(d):
    return d.dov_ef7 == "1" if "dov_ef7" in d else everyone(d)


@rule([])
def dov_ef_400(d):
    return d.DOV_EF_amount == "$400" if "DOV_EF_amount" in d else everyone(d)


# (group, concept, item-prefix-or-var, universe rule, rule description, waves or None=all)
ITEMS = [
    ("BNPL", "Used BNPL in past year", "BNPL1", everyone, "All respondents", None),
    ("BNPL", "Number of current BNPL purchases", "BNPL2", eq("BNPL1", "Yes"), "BNPL1 = Yes", None),
    ("BNPL", "Late on a BNPL payment", "BNPL3", eq("BNPL1", "Yes"), "BNPL1 = Yes", None),
    ("BNPL", "Charged extra for paying late", "BNPL3A", eq("BNPL3", "Yes"), "BNPL3 = Yes", None),
    ("BNPL", "BNPL payment triggered overdraft/NSF fee", "BNPL1A", bnpl_users_with_overdraft,
     "BNPL1 = Yes and BK2_f (paid an overdraft fee) = Yes", None),
    ("BNPL", "Reasons for using BNPL (grid)", "BNPL4_", eq("BNPL1", "Yes"), "BNPL1 = Yes", None),
    ("BNPL", "Most important reason", "BNPL5", bnpl_users_any_reason,
     "BNPL1 = Yes and at least one BNPL4 item = Yes", None),
    ("BNPL", "What BNPL was used for (select all)", "BNPL6_", eq("BNPL1", "Yes"), "BNPL1 = Yes", None),
    ("BNPL", "Beliefs about BNPL and credit", "BNPL7_", eq("BNPL1", "Yes"), "BNPL1 = Yes", None),
    ("Fragility", "How well managing financially", "B2", everyone, "All respondents", None),
    ("Fragility", "Doing at least okay (derived from B2)", "atleast_okay", everyone, "All respondents", None),
    ("Fragility", "Better/worse off than 12 months ago", "B3", everyone, "All respondents", None),
    ("Fragility", "3-month emergency fund", "EF1", everyone, "All respondents", None),
    ("Fragility", "Could cover 3 months if income lost", "EF2", eq("EF1", "No"), "EF1 = No", None),
    ("Fragility", "How would pay a $400 emergency expense (grid)", "EF3_", everyone,
     "All respondents (2022: amount is $400 or $500 by DOV_EF_amount)", None),
    ("Fragility", "Would cover $400 with cash or equivalent (derived)", "pay_casheqv", dov_ef_400,
     "All respondents; 2022: DOV_EF_amount = $400 only", None),
    ("Fragility", "Able to pay all bills in full this month", "EF5A", everyone, "All respondents", None),
    ("Fragility", "Effect of $400 expense on paying other bills", "EF5B", eq("EF5A", "Able to pay all bills"),
     "EF5A = Able to pay all bills", None),
    ("Fragility", "Bills expected to skip this month (grid)", "EF6A_", ne("EF5A", "Able to pay all bills"),
     "EF5A = Can't pay some bills", None),
    ("Fragility", "Bills would skip after $400 expense (grid)", "EF6B_", eq("EF5B", "Could not pay some bills"),
     "EF5B = Could not pay some bills", None),
    ("Fragility", "Paid all non-card bills in full last month", "EF5C", everyone, "All respondents", None),
    ("Fragility", "Had bills difficult to pay last month", "EF5D", eq("EF5C", "Yes"), "EF5C = Yes", None),
    ("Fragility", "How handled each bill last month (grid)", "EF6C_", eq("EF5C", "No"), "EF5C = No", None),
    ("Fragility", "Actions when had difficulty paying a bill (grid)", "EF8_", ef8_universe,
     "EF5C = No or EF5D = Yes", None),
    ("Fragility", "Largest emergency expense from savings (5 brackets)", "EF7", ef7_universe,
     "All respondents; 2025: dov_ef7 = 1 only", None),
    ("Fragility", "Largest emergency expense from savings (6 brackets)", "EF7A", eq("dov_ef7", "0"),
     "dov_ef7 = 0", None),
    ("Fragility", "Income volatility", "I9", everyone, "All respondents", None),
    ("Fragility", "Struggled to pay bills because income varies", "I12",
     ne("I9", "Roughly the same amount each month"), "I9 = varies (occasionally or often)", None),
    ("Fragility", "Has unpaid credit card debt", "C3", eq("C2A", "Yes"), "C2A = Yes", None),
    ("Fragility", "How handled credit card bills last month", "C3P", eq("C2A", "Yes"), "C2A = Yes", None),
    ("Fragility", "How often carried a card balance", "C4A", eq("C2A", "Yes"), "C2A = Yes", None),
    ("Fragility", "Has bank account", "BK1", everyone, "All respondents", None),
    ("Fragility", "Alternative financial services (grid)", "BK2_", everyone,
     "All respondents; BK2_f: BK1 = Yes", None),
    ("Fragility", "Applied for credit", "A0", everyone, "All respondents", None),
    ("Fragility", "Credit outcomes (grid)", "A1_", eq("A0", "Yes"), "A0 = Yes", None),
    ("Fragility", "Behind on rent in past year", "R11", eq("GH1", "Pay rent"), "GH1 = Pay rent", None),
    ("Controls", "Has a credit card", "C2A", everyone, "All respondents", None),
    ("Controls", "Household income (SHED, brackets)", "I40", everyone, "All respondents (see notes for 2022)", None),
    ("Controls", "Household income, 4 categories (derived from I40)", "inc_4cat_50k", everyone,
     "All respondents", None),
    ("Controls", "Household income (Ipsos profile)", "ppinc7", everyone, "All respondents", None),
    ("Controls", "Age", "ppage", everyone, "All respondents", None),
    ("Controls", "Age, 7 categories", "ppagecat", everyone, "All respondents", None),
    ("Controls", "Highest education (SHED)", "ED0", everyone, "All respondents", None),
    ("Controls", "Education, 4 categories (profile)", "ppeducat", everyone, "All respondents", None),
    ("Controls", "Gender (profile)", "ppgender", everyone, "All respondents", None),
    ("Controls", "Race/ethnicity (profile)", "ppethm", everyone, "All respondents", None),
    ("Controls", "Marital status (profile)", "ppmarit5", everyone, "All respondents", None),
    ("Controls", "Household size (profile)", "pphhsize", everyone, "All respondents", None),
    ("Controls", "Children 0-17 in household (profile)", "ppkid017", everyone, "All respondents", None),
    ("Controls", "Employment status (profile)", "ppemploy", everyone, "All respondents", None),
    ("Controls", "Metro status (profile)", "ppmsacat", everyone, "All respondents", None),
    ("Controls", "Census region (profile)", "ppreg4", everyone, "All respondents", None),
    ("Controls", "Housing tenure", "GH1", everyone, "All respondents", None),
    ("Design", "Respondent ID (links waves)", "shedid", everyone, "All respondents", None),
    ("Design", "Cross-section weight, sample scale", "weight", everyone, "All respondents", None),
    ("Design", "Cross-section weight, population scale", "weight_pop", everyone, "All respondents", None),
    ("Design", "Panel weight, sample scale", "panel_weight", None, "Recontacts from prior wave", None),
    ("Design", "Panel weight, population scale", "panel_weight_pop", None, "Recontacts from prior wave", None),
    ("Design", "Split ballot: $400 vs $500 emergency expense", "DOV_EF_amount", everyone, "All respondents", None),
    ("Design", "Split ballot: which income question", "income_question", everyone, "All respondents", None),
    ("Design", "Split ballot: EF7 vs EF7A", "dov_ef7", everyone, "All respondents", None),
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def codebook(wave: int) -> dict:
    """Parsed codebook, cached in data/interim keyed by the PDF hash."""
    pdf = codebook_pdf(wave)
    cache = INTERIM / f"codebook_{wave}_{sha(pdf)}.json"
    if cache.exists():
        return json.loads(cache.read_text())
    out = {k: dataclasses.asdict(v) for k, v in parse(pdf).items()}
    cache.write_text(json.dumps(out))
    return out


def load(wave: int) -> pd.DataFrame:
    return pd.read_csv(raw_csv(wave), dtype=str, keep_default_na=False)


def members(prefix: str, columns) -> list[str]:
    if prefix.endswith("_"):
        return [c for c in columns if c.startswith(prefix) and not c.endswith("_iflag")]
    return [prefix] if prefix in columns else []


def universe(rule_fn, var):
    return eq("BK1", "Yes") if var == "BK2_f" else rule_fn


def imputed(d, var, rule_fn) -> pd.Series:
    """Rows where the item itself or one of the items its rule conditions on was imputed."""
    flags = [f"{var}_iflag"] + [
        c for p in rule_fn.parents for c in d.columns
        if c.endswith("_iflag") and (c == f"{p}_iflag" or (p.endswith("_") and c.startswith(p)))
    ]
    flags = [f for f in flags if f in d.columns]
    return (d[flags] == "1").any(axis=1) if flags else pd.Series(False, index=d.index)


def check_universe(d, var, rule_fn):
    answered = d[var] != ""
    if rule_fn is None:
        return answered.sum(), None, None
    rule_fn = universe(rule_fn, var)
    miss = answered != rule_fn(d)
    explained = (miss & imputed(d, var, rule_fn)).sum()
    return answered.sum(), int(miss.sum()), int(explained)


def codes_text(cb_var: dict | None, d_col: pd.Series) -> str:
    if cb_var and cb_var["codes"]:
        parts = [f"{c}={l}" for _, c, l in cb_var["codes"] if c != "."]
        if parts and all(p.split("=", 1)[1] for p in parts):
            return "; ".join(parts)
        # Unlabeled codes (e.g. BNPL2 1, 2): keep the code alone.
        return "; ".join(p if p.split("=", 1)[1] else p.split("=")[0] for p in parts)
    vals = sorted(v for v in d_col.unique() if v != "")
    if len(vals) > 20:
        return "numeric/continuous (no value labels)"
    return "CSV labels (codebook prints no full tabulation): " + "; ".join(vals)


def md_escape(s: str) -> str:
    return s.replace("|", "\\|").replace("$", "\\$")


def build():
    TABLES.mkdir(parents=True, exist_ok=True)
    INTERIM.mkdir(parents=True, exist_ok=True)
    cbs = {w: codebook(w) for w in WAVES}
    data = {w: load(w) for w in WAVES}

    rows = []
    for group, concept, prefix, rule, rule_txt, _ in ITEMS:
        for w in WAVES:
            d = data[w]
            for var in members(prefix, d.columns) or [None]:
                if var is None:
                    rows.append(dict(group=group, concept=concept, item=prefix, wave=w, var="", present=False))
                    continue
                answered, mismatch, explained = check_universe(d, var, rule)
                v = cbs[w].get(var)
                rows.append(dict(
                    group=group, concept=concept, item=prefix, wave=w, var=var, present=True,
                    in_codebook=v is not None, page=v["page"] if v else None,
                    wording=v["label"] if v else "", codes=codes_text(v, d[var]),
                    asked_of=("BK1 = Yes" if var == "BK2_f" else rule_txt),
                    answered_unweighted=int(answered), total=len(d),
                    rule_mismatches=mismatch, mismatches_with_imputed_items=explained,
                ))
    uni = pd.DataFrame(rows)
    uni.to_csv(TABLES / "phase1_universe.csv", index=False)

    late = compare_late(cbs, data)
    panel = panel_counts(data)
    panel.to_csv(TABLES / "phase1_panel_bnpl.csv", index=False)
    write_inventory(uni, late, panel)
    print(late)
    print(panel.to_string(index=False))
    bad = uni[uni.present & (uni.rule_mismatches.fillna(0) > uni.mismatches_with_imputed_items.fillna(0))]
    print(f"universe rules: {int(uni.present.sum())} item-waves checked, "
          f"{len(bad)} with mismatches not explained by imputation")
    if len(bad):
        print(bad[["wave", "var", "asked_of", "rule_mismatches", "mismatches_with_imputed_items"]].to_string())


def compare_late(cbs, data) -> str:
    out = ["### 2023 vs 2024: late payment block, word for word", ""]
    out.append("| Var | Wording 2023 = 2024 | Codes 2023 = 2024 | Asked of (data check) | Preceding items | Differences |")
    out.append("|---|---|---|---|---|---|")
    for var in ["BNPL1", "BNPL3", "BNPL3A"]:
        a, b = cbs[2023][var], cbs[2024][var]
        same_w = a["label"] == b["label"]
        ca = [(c, l) for _, c, l in a["codes"] if c != "."]
        cb = [(c, l) for _, c, l in b["codes"] if c != "."]
        diffs = []
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a["label"], b["label"]).get_opcodes():
            if op != "equal":
                diffs.append(f"{op} {a['label'][i1:i2]!r} -> {b['label'][j1:j2]!r}")
        rule = {"BNPL1": everyone, "BNPL3": eq("BNPL1", "Yes"), "BNPL3A": eq("BNPL3", "Yes")}[var]
        checks = []
        for w in (2023, 2024):
            _, mm, ex = check_universe(data[w], var, rule)
            checks.append(f"{w}: {mm} mismatches ({ex} imputed)")
        keys = {w: list(cbs[w]) for w in (2023, 2024)}
        prev = {w: keys[w][keys[w].index(var) - 1] for w in (2023, 2024)}
        out.append(
            f"| {var} | {'identical' if same_w else 'DIFFERENT'} | {'identical' if ca == cb else 'DIFFERENT'} "
            f"| {'; '.join(checks)} | 2023: {prev[2023]}; 2024: {prev[2024]} | {'; '.join(diffs) or 'none'} |"
        )
    return "\n".join(out)


def panel_counts(data) -> pd.DataFrame:
    d25 = data[2025][["shedid", "panel_weight", "BNPL1", "BNPL3"]]
    d24 = data[2024][["shedid", "BNPL1", "BNPL3"]]
    p = d25[d25.panel_weight != ""].merge(d24, on="shedid", how="left", suffixes=("_2025", "_2024"),
                                         indicator=True)
    w = p.panel_weight.astype(float)
    u24, u25 = p.BNPL1_2024 == "Yes", p.BNPL1_2025 == "Yes"
    rows = [
        ("2025 recontacts (panel_weight nonmissing)", len(p), 1.0),
        ("  linked to a 2024 record by shedid", int((p._merge == "both").sum()),
         w[p._merge == "both"].sum() / w.sum()),
        ("  used BNPL in 2024 (2024 BNPL1 = Yes)", int(u24.sum()), w[u24].sum() / w.sum()),
        ("  used BNPL in 2025 (2025 BNPL1 = Yes)", int(u25.sum()), w[u25].sum() / w.sum()),
        ("  used BNPL in both years", int((u24 & u25).sum()), w[u24 & u25].sum() / w.sum()),
        ("  used BNPL in 2024 or 2025", int((u24 | u25).sum()), w[u24 | u25].sum() / w.sum()),
        ("  2025 BNPL users who were late in 2025 (BNPL3 = Yes)", int((u25 & (p.BNPL3_2025 == "Yes")).sum()),
         w[u25 & (p.BNPL3_2025 == "Yes")].sum() / w.sum()),
        ("  2024 users who were late in 2024 (BNPL3 = Yes)", int((u24 & (p.BNPL3_2024 == "Yes")).sum()),
         w[u24 & (p.BNPL3_2024 == "Yes")].sum() / w.sum()),
    ]
    return pd.DataFrame(rows, columns=["group", "n_unweighted", "share_of_recontacts_panel_weighted"])


def write_inventory(uni: pd.DataFrame, late: str, panel: pd.DataFrame):
    out = [BEGIN, "", "## Item detail by wave (generated)", "",
           "Generated by `make inventory`. Wording is the codebook variable label, whitespace and quote",
           "characters normalized; the codebook label is the only wording source in data/raw (the",
           "questionnaire appendix is not). Codes are the codebook numeric codes; the public CSVs store the",
           "value **labels**, not the codes. Answered n is **unweighted**. \"Rule check\" is the number of rows",
           "where the asked-of rule disagrees with who actually has an answer; mismatches in parentheses",
           "involve an imputed item (`_iflag` = 1).", ""]
    for group in uni.group.unique():
        out += [f"### {group}", ""]
        g = uni[uni.group == group]
        for concept in g.concept.unique():
            c = g[g.concept == concept]
            out += [f"#### {concept}", "",
                    "| Wave | Var | Page | Wording (codebook) | Codes | Asked of | Answered n (unwtd) | Rule check |",
                    "|---|---|---|---|---|---|---|---|"]
            for _, r in c.iterrows():
                if not r.present:
                    out.append(f"| {r.wave} | not in file | | | | | | |")
                    continue
                chk = "n/a" if pd.isna(r.rule_mismatches) else (
                    "✓ 0" if r.rule_mismatches == 0 else f"{int(r.rule_mismatches)} ({int(r.mismatches_with_imputed_items)})")
                page = "" if pd.isna(r.page) else f"p{int(r.page)}"
                wording = md_escape(r.wording) if r.in_codebook else "_not in codebook_"
                out.append(f"| {r.wave} | {r['var']} | {page} | {wording} | {md_escape(r.codes)} | {md_escape(r.asked_of)} "
                           f"| {int(r.answered_unweighted):,} / {int(r.total):,} | {chk} |")
            out.append("")
    out += [late, "",
            "### 2025 panel recontacts and BNPL use (generated)", "",
            "| Group | n (unweighted) | Share of recontacts (panel_weight) |", "|---|---|---|"]
    for _, r in panel.iterrows():
        out.append(f"| {r.group.strip()} | {r.n_unweighted:,} | {r.share_of_recontacts_panel_weighted:.3f} |")
    out += ["", END]
    text = INVENTORY.read_text()
    block = "\n".join(out)
    if BEGIN in text:
        text = text[: text.index(BEGIN)] + block + text[text.index(END) + len(END):]
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    INVENTORY.write_text(text)


if __name__ == "__main__":
    build()
