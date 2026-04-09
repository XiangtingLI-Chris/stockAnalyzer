from typing import NamedTuple
from contentScrap import filter_announcement_links, text_extract, fetch_target_stock
from articleAnalyse import analyse_article
from stockDataAnalyse import get_stock_information

class StockAnalyseResult(NamedTuple):
    stock_name: str
    stock_code: str
    stock_url: str
    current_price: float
    year_high: float
    year_low: float
    sentiment: str
    announcement_url: str

def run_stock_pipeline() -> list[StockAnalyseResult]:
    """
    Analyse a stock announcement page.
    :return: A list of analysis results, one per announcement.
    """
    links = filter_announcement_links()
    result = []

    for link in links:
        article = text_extract(link)
        analyse_result = analyse_article(article)

        stock_name, stock_code, stock_url = fetch_target_stock(link)
        stock_info = get_stock_information(stock_code)

        if not stock_info:
            continue

        current_price = stock_info["current_price"]
        year_high = stock_info["year_high"]
        year_low = stock_info["year_low"]

        result.append((stock_name, stock_code, current_price, year_high, year_low, analyse_result, stock_url, link))

    return result
