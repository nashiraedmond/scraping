from requests_html import HTMLSession
from bs4 import BeautifulSoup

s = HTMLSession()
urls = ""

def get_html(url):
	r = s.get(url)
	html = BeautifulSoup(r.content, 'html.parser')
	return html

def main():
	pass

if __name__ == '__main__':
	main()
