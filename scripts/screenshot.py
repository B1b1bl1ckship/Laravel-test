from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import os

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

with open("results/endpoints.json") as f:
    valid_endpoints = json.load(f)

os.makedirs("results/screenshots", exist_ok=True)

for url in valid_endpoints:
    try:
        driver.get(url)
        filename = os.path.join("results/screenshots", url.replace("https://", "").replace("/", "_") + ".png")
        driver.save_screenshot(filename)
        print(f"Saved screenshot: {filename}")
    except:
        print(f"Failed to capture: {url}")

driver.quit()
