"""Apply config/variables.yaml and build the pooled file, one row per respondent-wave."""
import pandas as pd
import yaml

from bnpl.load import read_wave
from bnpl.paths import CONFIG, PROCESSED, WAVES

POOLED = PROCESSED / "pooled.csv"


def load_config() -> dict:
    return yaml.safe_load((CONFIG / "variables.yaml").read_text())


def recode(raw: pd.Series, mapping: dict, name: str, wave: int) -> pd.Series:
    """Map CSV value labels to harmonized values. Blank = not asked -> NaN."""
    labels = set(raw[raw != ""].unique())
    unknown = labels - set(mapping)
    if unknown:
        raise ValueError(f"{name} {wave}: labels not in recode map: {sorted(unknown)}")
    return raw.map(mapping).astype("Float64")


def harmonize_wave(wave: int, cfg: dict) -> pd.DataFrame:
    sources = [v["source"] for v in {**cfg["ids"], **cfg["weights"]}.values()]
    for c in cfg["concepts"].values():
        if wave in c["waves"]:
            src = c["waves"][wave]["source"]
            sources += [src, f"{src}_iflag"]
    raw = read_wave(wave, usecols=sources, dtype=str, keep_default_na=False)

    out = pd.DataFrame({"wave": wave}, index=raw.index)
    for name, spec in {**cfg["ids"], **cfg["weights"]}.items():
        col = raw[spec["source"]].replace("", None)
        out[name] = col if name == "shedid" else pd.to_numeric(col)
    for name, c in cfg["concepts"].items():
        if wave not in c["waves"]:
            out[name] = pd.NA
            out[f"{name}_imputed"] = pd.NA
            continue
        src = c["waves"][wave]["source"]
        out[name] = recode(raw[src], c["recode"], name, wave)
        out[f"{name}_imputed"] = (raw[f"{src}_iflag"] == "1").astype("Int8")
    return out


def build() -> pd.DataFrame:
    cfg = load_config()
    pooled = pd.concat([harmonize_wave(w, cfg) for w in WAVES], ignore_index=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    pooled.to_csv(POOLED, index=False)
    return pooled


def read_pooled() -> pd.DataFrame:
    return pd.read_csv(POOLED, dtype={"shedid": str})


def main() -> None:
    pooled = build()
    print(f"wrote {POOLED.relative_to(PROCESSED.parents[1])}: {len(pooled):,} rows")


if __name__ == "__main__":
    main()
