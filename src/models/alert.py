from typing import Dict, List
from uuid import uuid4
from common.database import Database
from models.item import Item
from models.model import Model


class Alert(Model):
    collection = 'alerts'

    def __init__(self, item_id: str, price_limit: float, _id: str = None):
        super().__init__()
        self.item_id = item_id
        self.item = Item.get_by_id(item_id)
        self.price_limit = price_limit
        self._id = _id or uuid4().hex

    def load_item_price(self) -> float:
        self.item.load_price()
        return self.item.price

    def notify_price_reached(self):
        if self.item.price < self.price_limit:
            print(f"Item {self.item} has reached a price under {self.price_limit}. Latest price: {self.item.price}")

    def json(self) -> Dict:
        return {
            "item_id": self.item_id,
            "price_limit": self.price_limit,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.insert(collection=self.collection,
                        query=self.json())

    @classmethod
    def all(cls) -> List:
        alerts_from_db = Database.find(collection=cls.collection,
                                       query={})
        return [cls(**alert) for alert in alerts_from_db]
