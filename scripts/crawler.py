import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json

START_URL = "https://firstfocus.com"
visited = set()
valid_endpoints = []

results_dir = "results"
os.makedirs(results_dir, exist_ok=True)

# Define endpoints file
endpoints_file = os.path.join(results_dir, "endpoints.json")

# Load previous results if they exist
if os.path.exists(endpoints_file):
    with open(endpoints_file, "r") as f:
        try:
            valid_endpoints = json.load(f)
            visited = set(valid_endpoints)  # Prevent re-crawling same URLs
        except json.JSONDecodeError:
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
print(f"✅ Discovered {len(valid_endpoints)} valid endpoints. Stored in {endpoints_file}")
