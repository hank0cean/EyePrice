import re
from typing import Dict, List
import requests
import uuid
from bs4 import BeautifulSoup
from common.database import Database

class Item(object):
    def __init__(self, url, tag_name, query, _id: str = None):
        super().__init__()
        self.url = url
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

    def item_name(self) -> str:
        return self.url.split('/')[5].replace('_', ' ')

    def json(self) -> Dict:
        return {
            '_id': self._id,
            'url': self.url,
            'tag_name': self.tag_name,
            'query': self.query,
        }

    def save_to_mongo(self):
        Database.insert(collection='items',
                        data=self.json())

    @classmethod
    def get_by_id(cls, _id):
        item_json = Database.find_one(collection='items',
                                      query={'_id': _id})
        return cls(**item_json)

    @classmethod
    def all(cls) -> List:
        items_from_db = Database.find(collection='items',
                                      query={})
        return [cls(**item) for item in items_from_db]

    """
    @classmethod
    def find_by_item_name(cls, item_name):
        
        return Database.find(collection='items',
                             query={'item_name': item_name})
    """
