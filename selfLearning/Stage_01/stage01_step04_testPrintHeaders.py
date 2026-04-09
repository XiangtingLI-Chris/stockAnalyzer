import requests

url = "https://httpbin.org/headers"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    ),
    "Accept-Language": "zh-CN,zh;q=0.9"
}

try:
    response = requests.get(url, headers=headers)
    html = response.text
    print("Header:")
    print(html)
except requests.exceptions.RequestException as e:
    print("Internet access error:")
    print(e)
