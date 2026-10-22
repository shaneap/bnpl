import importlib

import pytest

MODULES = ["bnpl.load", "bnpl.harmonize", "bnpl.indicators", "bnpl.describe", "bnpl.figures"]


@pytest.mark.parametrize("name", MODULES)
def test_module_imports(name):
    assert hasattr(importlib.import_module(name), "main")


def test_paths_point_into_repo():
    from bnpl.paths import RAW, ROOT

    assert (ROOT / "docs" / "SPEC.md").exists()
    assert RAW == ROOT / "data" / "raw"
