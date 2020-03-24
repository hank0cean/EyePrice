from typing import Dict
from uuid import uuid4
from models.item import Item
from models.model import Model


class Alert(Model):
    collection = 'alerts'

    def __init__(self, item_id: str, price_limit: float, _id: str = None):
        super().__init__()
        self.item_id = item_id
        self.item = Item.get_by_id(item_id)
        self.price_limit = price_limit
        self.recent_price = None
        self._id = _id or uuid4().hex

    def __repr__(self):
        return f"<Alert {self.item_id}>"

    def load_item_price(self) -> float:
        self.item.load_price()
        self.recent_price = self.item.item_price

    def notify_price_reached(self):
        if self.item.price < self.price_limit:
            print(f"Item {self.item} has reached a price under {self.price_limit}. Latest price: {self.item.price}")

    def json(self) -> Dict:
        return {
            "item_id": self.item_id,
            "price_limit": self.price_limit,
            "_id": self._id
        }
