import requests
from bs4 import BeautifulSoup
from typing import List
from stage01_step07_textExtractFromLink import text_extract
import certifi

def fetch_links(url: str) -> List[str]:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        ),
        "Accept-Language": "zh-CN,zh;q=0.9"
    }

    response = requests.get(url, headers=headers, timeout=15, verify=certifi.where())
    response.raise_for_status()
    response.encoding = response.apparent_encoding

    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    spans_list = soup.select("span.arc-title")
    links_list: List[str] = []

    for span in spans_list:
        a_tag = span.find("a")
        link = a_tag.get("href")
        links_list.append(link)

    return links_list

def fetch_articles(links: List[str]) -> List[str]:
    return [text_extract(link) for link in links]

if __name__ == "__main__":
    stock_url = "https://stock.10jqka.com.cn/gegugg_list/"
    article_links = fetch_links(stock_url)
    articles_list = fetch_articles(article_links)
    print("Number of articles: ", len(articles_list))
    print("Articles contents list:")
    print(articles_list)
