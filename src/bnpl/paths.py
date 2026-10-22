"""Repository paths."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
INTERIM = ROOT / "data" / "interim"
PROCESSED = ROOT / "data" / "processed"
CONFIG = ROOT / "config"
TABLES = ROOT / "reports" / "tables"
FIGURES = ROOT / "reports" / "figures"

WAVES = (2021, 2022, 2023, 2024, 2025)


def raw_csv(wave: int) -> Path:
    return RAW / f"public{wave}.csv"


def codebook_pdf(wave: int) -> Path:
    return RAW / f"SHED_{wave}codebook.pdf"
