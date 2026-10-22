"""Phase 1 skip-logic facts the inventory relies on. Skipped when raw data is absent."""
import pandas as pd
import pytest

from bnpl.paths import WAVES, raw_csv

pytestmark = pytest.mark.skipif(not all(raw_csv(w).exists() for w in WAVES), reason="raw SHED files not present")

COLS = ["shedid", "panel_weight", "BNPL1", "BNPL3", "BNPL3A", "BNPL1A", "BK2_f", "weight"]


@pytest.fixture(scope="module")
def waves():
    out = {}
    for w in WAVES:
        cols = pd.read_csv(raw_csv(w), nrows=0).columns
        out[w] = pd.read_csv(raw_csv(w), usecols=[c for c in COLS if c in cols], dtype=str, keep_default_na=False)
    return out


@pytest.mark.parametrize("wave", WAVES)
def test_late_payment_asked_of_all_bnpl_users(waves, wave):
    d = waves[wave]
    assert ((d.BNPL3 != "") == (d.BNPL1 == "Yes")).all()
    assert set(d.BNPL3) <= {"", "Yes", "No"}


@pytest.mark.parametrize("wave", [2022, 2023, 2024, 2025])
def test_late_fee_asked_of_late_payers(waves, wave):
    d = waves[wave]
    assert ((d.BNPL3A != "") == (d.BNPL3 == "Yes")).all()


def test_overdraft_item_asked_of_users_who_paid_overdraft_fee(waves):
    d = waves[2025]
    assert ((d.BNPL1A != "") == ((d.BNPL1 == "Yes") & (d.BK2_f == "Yes"))).all()


@pytest.mark.parametrize("wave", WAVES)
def test_every_row_has_cross_section_weight(waves, wave):
    assert (waves[wave].weight != "").all()


def test_2025_recontacts_link_to_2024_by_shedid(waves):
    p = waves[2025][waves[2025].panel_weight != ""]
    assert len(p) > 0
    assert p.shedid.isin(waves[2024].shedid).all()
    assert waves[2025].shedid.is_unique and waves[2024].shedid.is_unique
