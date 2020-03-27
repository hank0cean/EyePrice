from dataclasses import dataclass, field
from typing import Dict
from uuid import uuid4
import requests
import re
from bs4 import BeautifulSoup
from models.model import Model

@dataclass(eq=False)
class Item(Model):
    collection: str = field(default='items', init=False)
    url: str
    tag_name: str
    query: Dict
    name: str = field(default=None)
    price: float = field(default=None)
    _id: str = field(default_factory=lambda: uuid4().hex)

    def json(self) -> Dict:
        return {
            'url': self.url,
            'tag_name': self.tag_name,
            'query': self.query,
            'name': self.name,
            'price': self.price,
            '_id': self._id
        }

    def load_price(self) -> float:
        content = requests.get(self.url).content
        soup = BeautifulSoup(content, "html.parser")
        price_elem = soup.find(self.tag_name, self.query)
        if price_elem is not None:
            price_string = price_elem.text.strip()
            pattern = re.compile(r"(\d+,?\d+\.\d\d)")
            match = pattern.search(price_string)
            found_price = match.group(1)
            self.price = float(found_price)
        return self.price
