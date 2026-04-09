import akshare as ak

def get_stock_price_info(stock_code: str) -> dict[str, float] | None:
    df = ak.stock_zh_a_hist(
        symbol=stock_code,
        period="daily",
        start_date="20250101",
        end_date="20251231",
        adjust=""
    )

    # print(df)
    # print("type(df): ", type(df))
    # print("df.shape: ", df.shape)
    # print("df.columns: ", df.columns)
    # print("df.dtypes: ", df.dtypes)
    # print("df.head(3): ", df.head(3))
    # print("df.tail(3): ", df.tail(3))

    if df.empty:
        return None

    return {
        "current_price": float(df.iloc[-1]["收盘"]),
        "year_high": float(df["最高"].max()),
        "year_low": float(df["最低"].min())
    }

if __name__ == "__main__":
    print(get_stock_price_info("000001"))