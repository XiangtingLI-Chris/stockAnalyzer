import akshare as ak
import pandas as pd

def get_stock_list(limit: int = 50) -> pd.DataFrame:
    """
    Fetch top `limit` stocks and return a list
    """
    df = ak.stock_zh_a_spot_em()
    stock_df = df[["代码", "名称"]].copy()
    stock_df.columns = ["code", "name"]
    stock_df = stock_df.head(limit)
    return stock_df

if __name__ == "__main__":
    stock_list = get_stock_list()
    print(stock_list)