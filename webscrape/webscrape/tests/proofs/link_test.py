import html
import requests
from bs4 import BeautifulSoup
from utils import utils

links = requests.get("https://www.google.com/search?q=Anderson+Paak&num=5")

print(links)

soup = BeautifulSoup(links.text, "html.parser")

results = soup.find_all("div", {"class": "g"})

query_links = []

for link in results:
    the_link = link.find("a", href=True)["href"]
    print(the_link)
    query_links.append(utils.get_link_info(the_link))

print(query_links)


