import json
import openai

API_KEY = "YOUR_OPENAI_API_KEY"
openai.api_key = API_KEY

def generate_test_cases(page_url):
    prompt = f"Generate structured test cases for this page: {page_url}"
    response = openai.Completion.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=200
    )
    return response.choices[0].text.strip()

with open("results/endpoints.json") as f:
    endpoints = json.load(f)

test_cases = {url: generate_test_cases(url) for url in endpoints}

with open("results/test_cases.json", "w") as f:
    json.dump(test_cases, f, indent=2)
