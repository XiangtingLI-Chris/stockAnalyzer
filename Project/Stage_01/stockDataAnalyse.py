import akshare as ak

def get_stock_information(stock_code: str) -> dict[str, float] | None:
    df = ak.stock_zh_a_hist(
        symbol=stock_code,
        period="daily",
        start_date="20250101",
        end_date="20251231",
        adjust=""
    )

    if df.empty:
        return None

    return {
        "current_price": float(df.iloc[-1]["收盘"]),
        "year_high": float(df["最高"].max()),
        "year_low": float(df["最低"].min())
    }