import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

BASE_URL = "https://stock.10jqka.com.cn/gegugg_list/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    ),
    "Accept-Language": "zh-CN,zh;q=0.9"
}

MAX_PAGES = 20
MAX_PUBLISHING_DAYS = 7
MAX_LINKS_PER_PAGE = 25

_TIME_RE = re.compile(r"^\s*(\d{1,2})月(\d{1,2})日\s+(\d{1,2}):(\d{2})\s*$")

def scrap(url: str) -> BeautifulSoup:
    """
    Use BeautifulSoup to parse the given `url`.
    :param url: The target url to be parsed.
    :return: The html content after being parsed.
    """
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    # Use other encoding method to interpret Mandarin
    response.encoding = response.apparent_encoding

    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    return soup

def text_extract(url: str) -> str:
    """
    Extract the whole article content (of an announcement) given the `url` (of the announcement).
    :param url: The url (of the target announcement) to be extracted.
    :return: The whole article content.
    """
    # If url starts with "http", transfer it to "https" so that the access will not be denied by company's proxy.
    if url.startswith("http://"):
        url = "https://" + url[len("http://"):]

    soup = scrap(url)

    content_node = soup.select_one("div#contentApp")
    if not content_node:
        return ""

    raw_p_list = content_node.find_all("p")
    final_text_content = ""

    for p in raw_p_list:
        # Skip the graph
        classes = p.get("class")
        if classes and "acthq" in classes:
            continue

        final_text_content += p.get_text(strip=True)

    return final_text_content

def fetch_links(url: str) -> list[str]:
    """
    Fetch all links (of announcements) from current stock page given by `url` and filter announcements in a week.
    :param url: The url of the current stock page.
    :return: All links (of announcements) found (usually 25 in total).
    """
    soup = scrap(url)

    spans_list = soup.select("span.arc-title")
    links_list: list[str] = []

    for span in spans_list:
        s_tag = span.find("span")
        time = s_tag.text
        parsed_time = parse_time(time)
        if not is_publish_time_valid(parsed_time):
            break

        a_tag = span.find("a")
        link = a_tag.get("href")
        links_list.append(link)

    return links_list

def parse_time(time_string: str, time_now: datetime | None = None) -> datetime:
    """
    Parse a time string (such as "12月21日 22:09") to datetime.
    """
    time_now = time_now or datetime.now()

    match = _TIME_RE.match(time_string)
    if not match:
        raise ValueError(f"Unable to parse the time!")

    month, day, hour, minute = map(int, match.groups())
    time = datetime(time_now.year, month, day, hour, minute)

    if time > time_now:
        time = datetime(time_now.year - 1, month, day, hour, minute)

    return time

def is_publish_time_valid(publishing_time: datetime) -> bool:
    """
    Judge whether the publishing time of the announcement exceeds the limit.
    """
    cutoff = datetime.now() - timedelta(days=MAX_PUBLISHING_DAYS)

    if publishing_time < cutoff:
        return False
    else:
        return True

def fetch_target_stock(url: str) -> tuple[str, str, str]:
    """
    Fetch certain information about the target stock by searching the announcement.
    :param url: The url of the announcement.
    :return: Stock name, stock code and stock url.
    """
    if url.startswith("http://"):
        url = "https://" + url[len("http://"):]

    soup = scrap(url)

    content_node = soup.select_one("div#contentApp")
    if not content_node:
        return "", "", ""

    raw_p_list = content_node.find_all("p")

    stock_name = ""
    stock_code = ""
    stock_url = ""

    for p in raw_p_list:
        graph_class = p.get("class")
        if graph_class and "acthq" in graph_class:
            continue

        raw_a_list = p.find_all("a")

        for a in raw_a_list:
            curr_class = a.get("class")
            if "singleStock" in curr_class:
                stock_name = a.text
            elif "art_links" in curr_class:
                stock_code = a.text
                stock_url = a.get("href")

            if stock_name and stock_code and stock_url:
                break

    return stock_name, stock_code, stock_url

def build_page_url(page: int) -> str:
    """
    Build the url according to the `page`.
    """
    if page <= 1:
        return BASE_URL
    else:
        return f"{BASE_URL}index_{page}.shtml"

def filter_announcement_links() -> list[str]:
    """
    Filter all links of announcements that are in a week.
    :return: A list where each element is the link of an announcement.
    """
    earliest_time = datetime.now() - timedelta(days=7)
    filtered_links: list[str] = []

    for page in range(1, MAX_PAGES + 1):
        current_url = build_page_url(page)
        links = fetch_links(current_url)

        if len(links) != MAX_LINKS_PER_PAGE:
            break

        filtered_links.extend(links)

    return filtered_links

if __name__ == "__main__":
    links = filter_announcement_links()
    print(links)