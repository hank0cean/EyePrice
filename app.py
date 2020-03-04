import re
import requests
from bs4 import BeautifulSoup

URL = "https://store.steampowered.com/app/653530/Return_of_the_Obra_Dinn/"
TAG = "div"
QUERY = {"class": "game_purchase_price price"}

response = requests.get("https://store.steampowered.com/app/653530/Return_of_the_Obra_Dinn/")
content = response.content
soup = BeautifulSoup(content, "html.parser")
element = soup.find(TAG, QUERY)
string_price = element.text.strip()

pattern = re.compile(r"(\d+\.\d\d)")
match = pattern.search(string_price)
found_price = match.group(1)
price = float(found_price)

print(price)
