from __future__ import annotations

import glob
import os
from typing import Iterable
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = ["trade_date", "code", "name", "open", "pct_chg"]

def iter_stage2_csv_files(stage2_output_dir: str, pattern: str) -> list[str]:
    """
    Find stage 2 CSV files and sort them by batch number.
    """
    files = glob.glob(str(Path(stage2_output_dir) / pattern))

    def _extract_batch_no(path: str) -> int:
        # stage2_hits_3y_batch_12.csv -> 12
        base = os.path.basename(path)
        try:
            num_str = base.split("_batch_")[-1].split(".")[0]
            return int(num_str)
        except Exception:
            return 10 ** 9

    files.sort(key=_extract_batch_no)

    return files

def load_stage2_from_csv_batches(csv_files: Iterable[str]) -> pd.DataFrame:
    """
    Read several batch CSV files and merge to a single DataFrame.
    - `code` reads as string to avoid the missing 0s in the front.
    - `trade_date` parsed as datetime.
    """
    dfs: list[pd.DataFrame] = []

    for fp in csv_files:
        df = pd.read_csv(
            fp,
            dtype={"code": "string"},
            parse_dates=["trade_date"]
        )

        missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            raise ValueError(f"File {fp} missing column {missing}, actual column {list(df.columns)}")

        # only keep necessary columns
        df = df[REQUIRED_COLUMNS].copy()

        # ensure types correct
        df["code"] = df["code"].astype("string")
        df["name"] = df["name"].astype("string")
        df["open"] = pd.to_numeric(df["open"], errors="coerce")
        df["pct_chg"] = pd.to_numeric(df["pct_chg"], errors="coerce")

        dfs.append(df)

    if not dfs:
        return pd.DataFrame(columns=REQUIRED_COLUMNS)

    out = pd.concat(dfs, ignore_index=True)

    # get rid of unnecessary lines
    out = out.dropna(subset=["trade_date", "code", "name"])

    # clean `code`: get rid of space and fill to 6 chars
    out["code"] = out["code"].str.strip()
    out["code"] = out["code"].str.zfill(6)

    return out