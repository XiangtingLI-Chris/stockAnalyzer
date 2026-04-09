from pipeline import run_stock_pipeline
from typing import Union
from pprint import pprint

if __name__ == "__main__":
    # url = "https://stock.10jqka.com.cn/gegugg_list/"
    result = run_stock_pipeline()
    positive_result: list[dict[str, Union[str, float]]] = []
    for r in result:
        stock_name, stock_code, current_price, year_high, year_low, analyse_result, stock_url, link = r

        if analyse_result == "利好":
            temp_dict = {
                "公司股票名": stock_name,
                "股票代码": stock_code,
                "当前股价": current_price,
                "今年最高股价": year_high,
                "今年最低股价": year_low,
                "日K线链接": stock_url,
                "公告链接": link
            }
            positive_result.append(temp_dict)

    pprint(positive_result, sort_dicts=False)
