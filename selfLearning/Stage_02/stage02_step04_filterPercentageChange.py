import pandas as pd
from stage02_step01_stockList import get_stock_list
from stage02_step02_dateRange import get_date_range
from stage02_step03_hist import get_stock_daily_hist

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

# def normalize_percent(s: pd.Series) -> pd.Series:
#     s = pd.to_numeric(s, errors="coerce")
#     max_abs = s.abs().max()
#
#     if pd.notna(max_abs) and max_abs <= 1:
#         return s * 100
#     return s



if __name__ == "__main__":
    stock_list = get_stock_list(limit=50)
    start_date, end_date = get_date_range(365)

    code = stock_list.iloc[0]["code"]
    name = stock_list.iloc[0]["name"]

    df_hist = get_stock_daily_hist(code, start_date, end_date, adjust="")
    df_hit = filter_stock_percent_change(df_hist, code, name, threshold_percent=5.0)

    print(df_hit.head(10))
    print("rows =", len(df_hit))

# def inspect(stock_list, start, end):
#     for idx, row in stock_list.iterrows():
#         code = row["code"]
#         name = row["name"]
#
#         try:
#             df_hist = get_stock_daily_hist(
#                 code=code,
#                 start_date=start,
#                 end_date=end,
#                 adjust=""
#             )
#
#             if df_hist.empty:
#                 print(f"[{code} {name}] no historical data")
#                 continue
#
#             print(f"\n[{code} {name}] pct_chg primary data example: ")
#             print(df_hist["pct_chg"].head(5).tolist())
#             print("max_abs =", df_hist["pct_chg"].abs().max())
#
#         except Exception as e:
#             print("error")
#
# if __name__ == "__main__":
#     stock_list = get_stock_list(limit=50)
#     start, end = get_date_range(365)
#     inspect(stock_list=stock_list, start=start, end=end)
