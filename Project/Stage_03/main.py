from __future__ import annotations

from config import (
    CSV_GLOB_PATTERN,
    OUT_COMMON_MONTHS_CSV,
    OUT_COMMON_MONTHS_XLSX,
    OUT_DIR,
    OUT_MONTHLY_COUNTS_CSV,
    STAGE2_OUTPUT_DIR,
    YEARS
)
from io_stage2 import iter_stage2_csv_files, load_stage2_from_csv_batches
from analysis_monthly import monthly_up_counts, common_months_across_years
from export import export_csv, export_excel

def run_stage3() -> None:
    csv_files = iter_stage2_csv_files(STAGE2_OUTPUT_DIR, CSV_GLOB_PATTERN)
    if not csv_files:
        raise FileNotFoundError(f"CSV not found: {STAGE2_OUTPUT_DIR}/{CSV_GLOB_PATTERN}")

    print(f"[Stage3] Found {len(csv_files)} batch CSV files.")
    df_hits = load_stage2_from_csv_batches(csv_files)
    print(f"[Stage3] Loaded hits rows: {len(df_hits)}")

    # A) monthly count
    df_monthly = monthly_up_counts(df_hits)
    print(f"[Stage3] Monthly rows: {len(df_monthly)}")
    export_csv(df_monthly, str(OUT_MONTHLY_COUNTS_CSV))
    print(f"[Stage3] Exported monthly counts -> {OUT_MONTHLY_COUNTS_CSV}")

    # B) find a stock that always increase at the same month of the whole 3 years
    df_common = common_months_across_years(df_monthly, years=YEARS)
    print(f"[Stage3] Common-month rows: {len(df_common)}")

    export_csv(df_common, str(OUT_COMMON_MONTHS_CSV))
    export_excel(df_common, str(OUT_COMMON_MONTHS_XLSX), sheet_name="common_months")
    print(f"[Stage3] Exported common months -> {OUT_COMMON_MONTHS_XLSX}")
    print(f"[Stage3] Done. Output dir: {OUT_DIR}")

if __name__ == "__main__":
    run_stage3()
