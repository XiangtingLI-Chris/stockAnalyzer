import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def fetch_notices(url: str) -> List[Dict[str, str]]:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        ),
        "Accept-Language": "zh-CN,zh;q=0.9"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    notice_items = soup.select(".list-con li")

    result: List[Dict[str, str]] = []

    for item in notice_items:
        a_tag = item.select_one("a.news-link")
        title = a_tag.get("title")
        link = a_tag.get("href")

        time_span_tag = item.select_one("span.arc-title span")
        time = time_span_tag.get_text(strip=True)

        result.append({
            "Title": title,
            "Link": link,
            "Time:": time,
        })

    return result

if __name__ == "__main__":
    stock_url = "https://stock.10jqka.com.cn/gegugg_list/"
    notices = fetch_notices(stock_url)
    print(f"Total notices: {len(notices)}")