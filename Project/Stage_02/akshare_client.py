import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

def get_stock_list(limit: int | None = 50) -> pd.DataFrame:
    """
    Fetch top `limit` stocks and return a list
    """
    df = ak.stock_zh_a_spot_em()
    stock_df = df[["代码", "名称"]].copy()
    stock_df.columns = ["code", "name"]

    if limit is not None:
        stock_df = stock_df.head(limit)

    return stock_df

def get_date_range(year_range: int) -> tuple[str, str]:
    """
    Fetch start and end date of dates in `range`, which are in format of YYYYMMDD.
    :param year_range: time range (in years).
    :return: a tuple of (start date, end date).
    """
    day_range = year_range * 365

    raw_end_date = datetime.today()
    raw_start_date = raw_end_date - timedelta(days=day_range)

    starting_date = raw_start_date.strftime("%Y%m%d")
    ending_date = raw_end_date.strftime("%Y%m%d")

    return starting_date, ending_date

def get_stock_daily_hist(code: str, start_date: str, end_date: str, adjust: str = "") -> pd.DataFrame:
    """
    Fetch the history daily data of a single stock (to later filter increase percentage)
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