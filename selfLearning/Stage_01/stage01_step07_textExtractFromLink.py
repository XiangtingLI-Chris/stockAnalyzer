import requests
from bs4 import BeautifulSoup

def text_extract(url: str) -> str:
    # If url starts with "http", transfer it to "https" so that the access will not be denied by company's proxy.
    if url.startswith("http://"):
        url = "https://" + url[len("http://"):]

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

    # Use other encoding method to interpret Mandarin
    response.encoding = response.apparent_encoding

    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    content_node = soup.select_one("div#contentApp")
    if not content_node:
        return ""

    raw_p_list = content_node.find_all("p")
    final_text_content = ""

    for p in raw_p_list:
        # Skip the graph
        classes = p.get("class")
        if classes is None:
            classes = []
        if "acthq" in classes:
            continue

        final_text_content += p.get_text(strip=True)

    return final_text_content

if __name__ == "__main__":
    article_url = "https://stock.10jqka.com.cn/20251209/c673062866.shtml"
    text = text_extract(article_url)
    print("text:")
    print(text)