"""Phase 3 acceptance: weighted estimates match published Fed figures to within rounding."""
import pytest

from bnpl import describe, harmonize
from bnpl.paths import WAVES, raw_csv

pytestmark = pytest.mark.skipif(not all(raw_csv(w).exists() for w in WAVES), reason="raw SHED files not present")


@pytest.fixture(scope="module")
def replication():
    rep, _ = describe.replication(describe.shares(harmonize.build()))
    return rep


def test_all_targets_have_estimates(replication):
    assert replication.pct.notna().all()


def test_estimates_match_published_to_within_rounding(replication):
    bad = replication[~replication.match]
    assert bad.empty, bad[["stat", "wave", "pct", "published_pct"]].to_string()


def test_weighted_share_simple_case():
    import pandas as pd

    assert describe.weighted_share(pd.Series([1, 0]), pd.Series([3, 1])) == 0.75
