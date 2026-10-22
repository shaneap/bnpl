"""Weighted shares by wave and the Phase 3 replication table."""
import numpy as np
import pandas as pd
import yaml

from bnpl.harmonize import read_pooled
from bnpl.paths import CONFIG, TABLES

# stat -> (outcome column, denominator description, denominator mask)
STATS = {
    "bnpl_use": ("bnpl_use", "all adults", lambda d: d.bnpl_use.notna()),
    "bnpl_late": ("bnpl_late", "BNPL users", lambda d: d.bnpl_use == 1),
    "bnpl_late_fee": ("bnpl_late_fee", "BNPL users", lambda d: d.bnpl_use == 1),
    "bnpl_late_fee_among_late": ("bnpl_late_fee", "late payers", lambda d: d.bnpl_late == 1),
    "bnpl_overdraft_among_asked": ("bnpl_overdraft", "BNPL users who paid an overdraft fee",
                                   lambda d: d.bnpl_overdraft.notna()),
}


def weighted_share(y: pd.Series, w: pd.Series) -> float:
    return float(np.sum(y * w) / np.sum(w))


def shares(pooled: pd.DataFrame, weight: str = "weight") -> pd.DataFrame:
    rows = []
    for wave, d in pooled.groupby("wave"):
        for stat, (col, denom, mask) in STATS.items():
            sub = d[mask(d)]
            if sub[col].isna().all() or len(sub) == 0:
                continue
            # Within the denominator, "not asked" for a follow-up means "no" (e.g. not late -> no late fee).
            y = sub[col].fillna(0).astype(float)
            rows.append(dict(stat=stat, wave=wave, denominator=denom, n_unweighted=len(sub),
                             pct=100 * weighted_share(y, sub[weight]),
                             n_imputed=int(sub[f"{col}_imputed"].fillna(0).sum())))
    return pd.DataFrame(rows)


def replication(est: pd.DataFrame) -> pd.DataFrame:
    tg = yaml.safe_load((CONFIG / "replication_targets.yaml").read_text())
    t = pd.DataFrame(tg["targets"]).rename(columns={"pct": "published_pct"})
    out = t.merge(est, on=["stat", "wave"], how="left")
    out["estimate_rounded"] = out.pct.round().astype("Int64")
    out["match"] = out.estimate_rounded == out.published_pct
    q = pd.DataFrame(tg["qualitative"]).merge(est, on=["stat", "wave"], how="left")
    return out, q


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    est = shares(read_pooled())
    est.to_csv(TABLES / "weighted_shares_by_wave.csv", index=False, float_format="%.2f")
    rep, qual = replication(est)
    rep.to_csv(TABLES / "replication.csv", index=False, float_format="%.2f")
    cols = ["stat", "wave", "denominator", "n_unweighted", "pct", "estimate_rounded", "published_pct", "match"]
    print(rep[cols].to_string(index=False, float_format=lambda x: f"{x:.2f}"))
    print(qual[["stat", "wave", "text", "pct"]].to_string(index=False, float_format=lambda x: f"{x:.2f}"))
    print(f"replication: {int(rep.match.sum())}/{len(rep)} targets match to within rounding")


if __name__ == "__main__":
    main()
