from __future__ import annotations
from pathlib import Path

STAGE3_DIR = Path(__file__).resolve().parent
PROJECT_DIR = STAGE3_DIR.parent

STAGE2_DIR = PROJECT_DIR / "Stage_02"
STAGE2_OUTPUT_DIR = STAGE2_DIR / "output"

CSV_GLOB_PATTERN = "stage2_hits_3y_batch_*.csv"

OUT_DIR = STAGE3_DIR / "output"

YEARS = 3

OUT_MONTHLY_COUNTS_CSV = OUT_DIR / "stage3_monthly_counts.csv"
OUT_COMMON_MONTHS_XLSX = OUT_DIR / "stage3_common_months.xlsx"
OUT_COMMON_MONTHS_CSV = OUT_DIR / "stage3_common_months.csv"
