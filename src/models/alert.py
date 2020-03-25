from dataclasses import dataclass, field
from typing import Dict
from uuid import uuid4
from models.model import Model
from models.item import Item

@dataclass(eq=False)
class Alert(Model):
    collection: str = field(default='alerts', init=False)
    item_id: str
    item_url: str
    price_limit: float
    recent_price: float = field(default=None)
    _id: str = field(default_factory=lambda: uuid4().hex)

    def load_item_price(self) -> float:
        self.recent_price = Item.get_by_id(self.item_id).load_price()

    def notify_price_reached(self):
        self.load_item_price()
        if self.recent_price < self.price_limit:
            print(f"Item {self.item_id} has reached a price under {self.price_limit}. Latest price: {self.recent_price}")

    def json(self) -> Dict:
        return {
            "item_id": self.item_id,
            "item_url": self.item_url,
            "price_limit": self.price_limit,
            "recent_price": self.recent_price,
            "_id": self._id
        }
