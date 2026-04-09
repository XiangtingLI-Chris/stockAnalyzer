import requests
from bs4 import BeautifulSoup

url = "https://stock.10jqka.com.cn/gegugg_list/"
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    ),
    "Accept-Language": "zh-CN,zh;q=0.9"
}

response = requests.get(url, headers=headers)

# If status code is not 200, this function will throw error
response.raise_for_status()

html = response.text
soup = BeautifulSoup(html, "html.parser")

# Find every `li` (Each `li` is a notice)
notice_items = soup.select(".list-con li")
print("Number of items found: ", len(notice_items))
print("")

for item in notice_items:
    # Find title link inside `li`: <a class="news-link" ...>
    a_tag = item.select_one("a.news-link")

    if a_tag is None:
        continue

    title = a_tag.get_text(strip=True)
    link = a_tag.get("href")

    # Fine time inside `span`: <span class="arc-title">
    time_span = item.select_one("span.arc-title span")
    time = time_span.get_text(strip=True)

    print("Title: ", title)
    print("Link: ", link)
    print("Time: ", time)
    print("")
