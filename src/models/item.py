from typing import Dict
from uuid import uuid4
import requests
import re
from bs4 import BeautifulSoup
from models.model import Model

class Item(Model):
    collection = 'items'

    def __init__(self, url, tag_name, query, _id: str = None):
        super().__init__()
        self.url = url
        self.tag_name = tag_name
        self.query = query
        self.price = None
        self._id = _id or uuid4().hex

    def __repr__(self):
        return f"<Item {self.url}>"

    def json(self) -> Dict:
        return {
            '_id': self._id,
            'url': self.url,
            'tag_name': self.tag_name,
            'query': self.query,
        }

    def load_price(self) -> float:
        response = requests.get(self.url)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()
        pattern = re.compile(r"(\d+,?\d+\.\d\d)")
        match = pattern.search(string_price)
        found_price = match.group(1)
        self.price = float(found_price)
        return self.price

    """
    @staticmethod
    def validate(url, tag_name, query):

    def item_name(self) -> str:
        return self.url.split('/')[3].replace('_', ' ')

    @classmethod
    def find_by_item_name(cls, item_name):
        
        return Database.find(collection='items',
                             query={'item_name': item_name})
    """
