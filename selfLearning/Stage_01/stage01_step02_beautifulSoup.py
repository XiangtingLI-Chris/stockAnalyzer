import requests
from bs4 import BeautifulSoup

url = "https://www.python.org/"
response = requests.get(url)
html = response.text

print("status_code: ", response.status_code)
print("Top 200 characters:\n", html[:200])

soup = BeautifulSoup(html, "html.parser")

onelink = soup.find("a")
print("onelink: ", onelink)
print("onelink.text: ", onelink.text)
print("onelink.get(\"href\")", onelink.get("href"))

links = soup.find_all("a")
for link in links:
    print(link.get("href"))
    print(link.text)