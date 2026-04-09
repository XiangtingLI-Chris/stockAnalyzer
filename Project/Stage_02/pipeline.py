import pandas as pd
import os

def filter_stock_percent_change(
        df_hist: pd.DataFrame,
        code: str,
        name: str,
        threshold_percent: float = 5.0,
) -> pd.DataFrame:
    """
    Filter single stock by checking comparing the percentage change of the stock with `threshold_percent`.
    """
    if df_hist is None or df_hist.empty:
        return pd.DataFrame(columns=["trade_date", "code", "open", "pct_chg"])

    df = df_hist.copy()

    max_abs = df["pct_chg"].abs().max()
    if pd.notna(max_abs) and max_abs <= 1.5:
        df["pct_chg"] = df["pct_chg"] * 100

    hit = df[df["pct_chg"] >= threshold_percent].copy()

    if hit.empty:
        return pd.DataFrame(columns=["trade_date", "code", "name", "open", "pct_chg"])

    hit["code"] = code
    hit["name"] = name

    hit = hit[["trade_date", "code", "name", "open", "pct_chg"]].sort_values("trade_date")

    return hit

def run_pipeline(
        *,
        get_stock_list,
        get_date_range,
        get_stock_daily_hist,
        limit: int | None,
        years: int,
        threshold_percent: float = 5.0,
        adjust: str = "",
        out_dir: str = "output",
        batch_size: int = 200,
        print_progress: bool = True
) -> pd.DataFrame:
    """
    Run end-to-end pipeline (full-market, multiple-year)
    Fetches multiple-year daily date for A-share stocks, filters trading days with pct_chg >= `threshold_percent`, saves per-batch CSV files.
    """
    os.makedirs(out_dir, exist_ok=True)

    stock_df = get_stock_list(limit=limit)
    start_date, end_date = get_date_range(year_range=years)

    total = len(stock_df)
    batch_files: list[str] = []

    for batch_start in range(0, total, batch_size):
        batch_end = min(batch_start + batch_size, total)
        batch_idx = batch_start // batch_size + 1
        batch_path = os.path.join(out_dir, f"stage2_hits_{years}y_batch_{batch_idx}.csv")

        if os.path.exists(batch_path):
            if print_progress:
                print(f"[batch {batch_idx}] exists, skip -> {batch_path}")
            batch_files.append(batch_path)
            continue

        if print_progress:
            print(f"\n=== batch {batch_idx}: stocks {batch_start + 1}-{batch_end} / {total} ===")

        results: list[pd.DataFrame] = []
        error_rows: list[dict] = []

        batch_df = stock_df.iloc[batch_start: batch_end]

        for i, (_, row) in enumerate(batch_df.iterrows(), start=batch_start + 1):
            code = row["code"]
            name = row["name"]

            if print_progress:
                print(f"[{i}/{total}] {code} {name}")

            try:
                df_hist = get_stock_daily_hist(
                    code=code,
                    start_date=start_date,
                    end_date=end_date,
                    adjust=adjust
                )

                if df_hist is None or df_hist.empty:
                    continue

                required_columns = {"trade_date", "open", "pct_chg"}
                if not required_columns.issubset(df_hist.columns):
                    raise ValueError(f"missing columns: {required_columns - set(df_hist.columns)}, actual column={list(df_hist.columns)}")

                hit = filter_stock_percent_change(df_hist, code=code, name=name, threshold_percent=threshold_percent)
                if not hit.empty:
                    results.append(hit)

            except Exception as e:
                error_rows.append({"code": code, "name": name, "error": str(e)})

        if results:
            batch_out = pd.concat(results, ignore_index=True).sort_values(["trade_date", "code"])
        else:
            batch_out = pd.DataFrame(columns=["trade_date", "code", "name", "open", "pct_chg"])

        batch_out.to_csv(batch_path, index=False, encoding="utf-8-sig")
        batch_files.append(batch_path)

        if print_progress:
            print(f"[batch {batch_idx}] saved: {batch_path}, rows={len(batch_out)}")
            if error_rows:
                print(f"[batch {batch_idx}] errors={len(error_rows)} (skipped)")

    final_df = pd.concat([pd.read_csv(p) for p in batch_files], ignore_index=True)
    final_df["trade_date"] = pd.to_datetime(final_df["trade_date"], errors="coerce")
    final_df = final_df.sort_values(["trade_date", "code"]).reset_index(drop=True)

    return final_df

    # for i, (_, row) in enumerate(stock_list.iterrows(), start=1):
    #     code = row["code"]
    #     name = row["name"]
    #
    #     if print_progress:
    #         print(f"[{i}/{total}] {code} {name}")
    #
    #     try:
    #         df_hist = get_stock_daily_hist(
    #             code=code,
    #             start_date=start_date,
    #             end_date=end_date,
    #             adjust=adjust
    #         )
    #
    #         required_columns = {"trade_date", "open", "pct_chg"}
    #         if df_hist is None or df_hist.empty:
    #             continue
    #         if not required_columns.issubset(df_hist.columns):
    #             raise ValueError(f"missing {required_columns - set(df_hist.columns)}, actual column={list(df_hist.columns)}")
    #
    #         hit = filter_stock_percent_change(df_hist, code=code, name=name, threshold_percent=threshold_percent)
    #         if not hit.empty:
    #             results.append(hit)
    #
    #     except Exception as e:
    #         error_rows.append({"code": code, "name": name, "error": str(e)})
    #
    # if results:
    #     final_df = pd.concat(results, ignore_index=True)
    #     final_df = final_df.sort_values(["trade_date", "code"]).reset_index(drop=True)
    # else:
    #     final_df = pd.DataFrame(columns=["trade_date", "code", "name", "open", "pct_chg"])
    #
    # return final_df
