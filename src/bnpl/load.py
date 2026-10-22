"""Read raw SHED waves. Raw files are read-only."""
import pandas as pd

from bnpl.paths import raw_csv


def read_wave(wave: int, usecols=None) -> pd.DataFrame:
    return pd.read_csv(raw_csv(wave), usecols=usecols, low_memory=False)


def main() -> None:
    """Phase 2 stub."""


if __name__ == "__main__":
    main()
