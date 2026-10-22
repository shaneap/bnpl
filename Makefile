PY ?= .venv/bin/python
export PYTHONPATH := src

.PHONY: all data models figures test manifest inventory clean

all: data models figures

data:
	$(PY) -m bnpl.load
	$(PY) -m bnpl.harmonize

# models.py and decompose.py are written by the author; skipped until they exist.
models: data
	@if [ -f src/bnpl/models.py ]; then $(PY) -m bnpl.models; else echo "models: src/bnpl/models.py not written yet, skipping"; fi
	@if [ -f src/bnpl/decompose.py ]; then $(PY) -m bnpl.decompose; else echo "models: src/bnpl/decompose.py not written yet, skipping"; fi

figures: data
	$(PY) -m bnpl.describe
	$(PY) -m bnpl.figures

test:
	$(PY) -m pytest

# Phase 1 helpers
manifest:
	$(PY) scripts/manifest.py

inventory:
	$(PY) scripts/phase1_checks.py

clean:
	find data/interim data/processed reports/tables reports/figures -type f ! -name .gitkeep -delete
