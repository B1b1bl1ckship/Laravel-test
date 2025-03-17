import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json

START_URL = "https://firstfocus.com"
visited = set()
valid_endpoints = []

def crawl(url):
    if url in visited or urlparse(url).netloc != urlparse(START_URL).netloc:
        return
    visited.add(url)
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return
        valid_endpoints.append(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup.find_all("a", href=True):
            link = urljoin(url, tag["href"])
            crawl(link)
    except:
        return

crawl(START_URL)

with open("results/endpoints.json", "w") as f:
    json.dump(valid_endpoints, f, indent=2)
print(f"Discovered {len(valid_endpoints)} valid endpoints.")
