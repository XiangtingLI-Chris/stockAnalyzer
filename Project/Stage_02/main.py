import config
import akshare_client as client
from pipeline import run_pipeline

def main() -> None:
    df = run_pipeline(
        get_stock_list=client.get_stock_list,
        get_date_range=client.get_date_range,
        get_stock_daily_hist=client.get_stock_daily_hist,
        limit=config.TEST_LIMIT,
        years=config.YEARS,
        threshold_percent=config.THRESHOLD_PERCENT,
        adjust=config.ADJUST,
        out_dir=config.OUT_DIR,
        batch_size=config.BATCH_SIZE,
        print_progress=config.PRINT_PROGRESS
    )

    df.to_excel(config.OUTPUT_XLSX, index=False)
    print(f"\nExport successfully: {config.OUTPUT_XLSX}, totally {len(df)} lines.")

    # dup_cnt = df.duplicated(subset=["code", "trade_date"]).sum()
    # print("\ncheck 1: duplicated record count (same code + same trade date): ", int(dup_cnt))

    # top_hits = (
    #     df.groupby(["code", "name"])
    #       .size()
    #       .sort_values(ascending=False)
    #       .head(10)
    # )
    # print("\ncheck 2: top 10 stocks:")
    # print(top_hits)
    #
    # print("\ncheck 3: pct_chg description analysis:")
    # print(df["pct_chg"].describe())
    #
    # print("\ncheck 4: smallest increase rate (should >= 5): ", df["pct_chg"].min())
    # print("\ncheck 5: largest increase rate (might be very big): ", df["pct_chg"].max())

if __name__ == "__main__":
    main()