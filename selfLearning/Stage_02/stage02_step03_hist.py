import akshare as ak
import pandas as pd

def get_stock_daily_hist(code: str, start_date: str, end_date: str, adjust: str = "") -> pd.DataFrame:
    """
    Fetch the history daily data of a single stock (to filter increase percentage)
    :param code: stock code (such as 000001) to represent a stock
    :param start_date: the start date in format of "YYYYMMDD"
    :param end_date: the end date in format of "YYYYMMDD"
    :param adjust: adjusted prices (default is "")
    :return: DataFrame, includes at least trade_date, open, pct_chg
    """
    df = ak.stock_zh_a_hist(
        symbol=code,
        period="daily",
        start_date=start_date,
        end_date=end_date,
        adjust=adjust
    )

    if df is None or df.empty:
        return pd.DataFrame(columns=["trade_date", "open", "pct_chg"])

    column_map = {}
    if "日期" in df.columns:
        column_map["日期"] = "trade_date"
    if "开盘" in df.columns:
        column_map["开盘"] = "open"
    if "涨跌幅" in df.columns:
        column_map["涨跌幅"] = "pct_chg"

    df = df.rename(columns=column_map)

    needed = ["trade_date", "open", "pct_chg"]
    missing = [c for c in needed if c not in df.columns]
    if missing:
        raise ValueError(f"The daily data is missing: {missing}, the real column is: {list(df.columns)}")

    out = df[needed].copy()

    out["trade_date"] = pd.to_datetime(out["trade_date"])
    out["open"] = pd.to_numeric(out["open"], errors="coerce")
    out["pct_chg"] = pd.to_numeric(out["pct_chg"], errors="coerce")

    return out.dropna(subset=["trade_date", "open", "pct_chg"])

if __name__ == "__main__":
    start_date = "20241225"
    end_date = "20251225"
    test_code = "000001"

    df_hist = get_stock_daily_hist(test_code, start_date, end_date, adjust="")

    print(df_hist.head())
    print("rows =", len(df_hist))