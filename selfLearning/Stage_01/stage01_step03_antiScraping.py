import requests
from bs4 import BeautifulSoup

url = "https://stock.10jqka.com.cn/gegugg_list/"
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 1; Win64; x64) ")
}

# Some websites do not want to be scrapped, so we pretend we are from a real chrome
response = requests.get(url, headers=headers)

html = response.text
soup = BeautifulSoup(html, "html.parser")

links = soup.find_all("a")
for link in links:
    print(link.get("href"))