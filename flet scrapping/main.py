import os
import requests
from bs4 import BeautifulSoup

url = "" # ... your URL here
apikey = os.meta.env.APIKEY
zenrows_api_base = "https://api.zenrows.com/v1/"

def extract_content(url, soup):
	# extracting logic goes here
	return {
		"url": url,
		"title": soup.title.string,
		"h1": soup.find("h1").text,
	}

response = requests.get(zenrows_api_base, params={
	"apikey": apikey,
	"url": url,
})
soup = BeautifulSoup(response.text, "html.parser")
content = extract_content(url, soup)

print(content)

