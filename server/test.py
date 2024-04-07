import requests

url = "http://localhost:8000/scrape"

response = requests.get(url)

print(response.json())
