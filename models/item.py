import re
from typing import Dict
import requests
import uuid
from bs4 import BeautifulSoup
from common.database import Database

class Item(object):
    def __init__(self, url, tag_name, query, _id: str = None):
        self.url = url
        self.item_name = url.split('/')[5].replace('_', ' ')
        self.tag_name = tag_name
        self.query = query
        self.price = None
        self.collection = "items"
        self._id = _id or uuid.uuid4().hex

    def __repr__(self):
        return f"<Item {self.url}>"

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

    def json(self) -> Dict:
        return {
            '_id': self._id,
            'url': self.url,
            'item_name': self.item_name,
            'tag_name': self.tag_name,
            'query': self.query,
            'price': self.price,
        }

    def save_to_mongo(self):
        Database.insert(collection='items',
                        data=self.json())

    @classmethod
    def all(cls):
        items = Database.find(collection='items',
                              query={})

        return items


    """
    @classmethod
    def find_by_item_name(cls, item_name):
        
        return Database.find(collection='items',
                             query={'item_name': item_name})
    """
