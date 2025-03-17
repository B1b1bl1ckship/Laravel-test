import json

with open("results/endpoints.json") as f:
    endpoints = json.load(f)

with open("results/test_cases.json") as f:
    test_cases = json.load(f)

html_report = "<html><body><h1>Test Report</h1><ul>"

for url in endpoints:
    screenshot = url.replace("https://", "").replace("/", "_") + ".png"
    test_case_list = "<ul>" + "".join(f"<li>{tc}</li>" for tc in test_cases.get(url, [])) + "</ul>"
    html_report += f"<li><a href='{url}'>{url}</a><br><img src='screenshots/{screenshot}' width='300'><br>{test_case_list}</li>"

html_report += "</ul></body></html>"

with open("results/report.html", "w") as f:
    f.write(html_report)
