"""Read raw SHED waves. Raw files are read-only."""
import pandas as pd

from bnpl.paths import WAVES, raw_csv


def read_wave(wave: int, usecols=None, **kwargs) -> pd.DataFrame:
    return pd.read_csv(raw_csv(wave), usecols=usecols, low_memory=False, **kwargs)


def main() -> None:
    missing = [w for w in WAVES if not raw_csv(w).exists()]
    if missing:
        raise SystemExit(f"missing raw files for waves {missing}; see data/raw/MANIFEST.md")
    print(f"raw files present for waves {list(WAVES)}")


if __name__ == "__main__":
    main()
