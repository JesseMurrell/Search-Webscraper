import html
import requests
from bs4 import BeautifulSoup

string = "https://www.google.com/search?q=Home+Broadband&num=1"

content = requests.get(string).text

soup = BeautifulSoup(content, "html.parser")

# can = soup.find_all("cite", {"class": "iUh30"})

can = soup.find("div", {"class": "g"})

cite = can.cite

print(cite.text)

