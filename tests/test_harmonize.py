"""Phase 2 slice: harmonized BNPL concepts and weights."""
import pandas as pd
import pytest

from bnpl import harmonize
from bnpl.paths import WAVES, raw_csv

have_raw = all(raw_csv(w).exists() for w in WAVES)
needs_raw = pytest.mark.skipif(not have_raw, reason="raw SHED files not present")


def test_recode_maps_labels_and_blank_to_missing():
    s = harmonize.recode(pd.Series(["Yes", "No", ""]), {"Yes": 1, "No": 0}, "x", 2023)
    assert s.tolist()[:2] == [1, 0] and pd.isna(s.iloc[2])


def test_recode_rejects_unknown_label():
    with pytest.raises(ValueError, match="not in recode map"):
        harmonize.recode(pd.Series(["Yes", "Maybe"]), {"Yes": 1, "No": 0}, "x", 2023)


def test_config_sources_are_inventory_items():
    """Every source column in variables.yaml appears in the generated inventory."""
    from bnpl.paths import ROOT

    inv = (ROOT / "docs" / "variable_inventory.md").read_text()
    cfg = harmonize.load_config()
    for name, c in cfg["concepts"].items():
        for wave, spec in c["waves"].items():
            assert f"| {wave} | {spec['source']} | p{spec['page']} |" in inv, (name, wave)


@pytest.fixture(scope="module")
def pooled():
    return harmonize.build()


# Waves where the inventory says each concept exists.
EXISTS = {
    "bnpl_use": WAVES,
    "bnpl_late": WAVES,
    "bnpl_late_fee": (2022, 2023, 2024, 2025),
    "bnpl_overdraft": (2025,),
}


@needs_raw
@pytest.mark.parametrize("concept", EXISTS)
def test_concept_present_exactly_in_inventory_waves(pooled, concept):
    for w in WAVES:
        has = pooled.loc[pooled.wave == w, concept].notna().any()
        assert has == (w in EXISTS[concept]), (concept, w)


@needs_raw
def test_universes(pooled):
    assert pooled.bnpl_use.notna().all()
    users = pooled.bnpl_use == 1
    assert (pooled.bnpl_late.notna() == users).all()
    fee_waves = pooled.wave.isin(EXISTS["bnpl_late_fee"])
    assert (pooled.bnpl_late_fee.notna()[fee_waves] == (pooled.bnpl_late == 1)[fee_waves]).all()


@needs_raw
@pytest.mark.parametrize("wave", WAVES)
def test_weight_sums_to_sample_size(pooled, wave):
    # Codebook: "weight" is scaled to sample size.
    d = pooled[pooled.wave == wave]
    assert d.weight.notna().all() and (d.weight > 0).all()
    assert d.weight.sum() == pytest.approx(len(d), abs=0.5)


@needs_raw
def test_one_row_per_respondent_wave(pooled):
    assert not pooled.duplicated(["wave", "shedid"]).any()
