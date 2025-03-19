import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json

START_URL = "https://app-staging.tick.com.au/"
results_dir = "results"
os.makedirs(results_dir, exist_ok=True)

# Define endpoints file
endpoints_file = os.path.join(results_dir, "endpoints.json")

# Load previous results if they exist
if os.path.exists(endpoints_file):
    with open(endpoints_file, "r") as f:
        try:
            valid_endpoints = set(json.load(f))  # Store in set to avoid duplicates
        except json.JSONDecodeError:
            valid_endpoints = set()
else:
    valid_endpoints = set()

visited = set(valid_endpoints)  # Prevent re-crawling previously found URLs

def crawl(url, session):
    if url in visited or urlparse(url).netloc != urlparse(START_URL).netloc:
        return
    visited.add(url)
    try:
        response = session.get(url, timeout=5)
        if response.status_code != 200:
            return
        valid_endpoints.add(url)  # Automatically prevents duplicates
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup.find_all("a", href=True):
            link = urljoin(url, tag["href"])
            crawl(link, session)
    except requests.RequestException as e:
        print(f"⚠️ Error fetching {url}: {e}")

# Use requests.Session() for efficient HTTP requests
with requests.Session() as session:
    crawl(START_URL, session)

# Save updated endpoints back to JSON
with open(endpoints_file, "w") as f:
    json.dump(sorted(valid_endpoints), f, indent=2)

print(f"✅ Discovered {len(valid_endpoints)} unique endpoints. Stored in {endpoints_file}")
