from dataclasses import dataclass, field
from typing import Dict
from uuid import uuid4
from models.model import Model
from models.item import Item

@dataclass(eq=False)
class Alert(Model):
    collection: str = field(default='alerts', init=False)
    price_limit: float
    item_id: str
    user_id: str
    _id: str = field(default_factory=lambda: uuid4().hex)

    def __post_init__(self):
        self.item = Item.get_by_id(self.item_id)

    def json(self) -> Dict:
        return {
            'price_limit': self.price_limit,
            'item_id': self.item_id,
            'user_id': self.user_id,
            '_id': self._id
        }

    def notify_price_reached(self):
        self.item.load_price()
        if self.item.price < self.price_limit:
            print(f"Item {self.item._id} has reached a price under {self.price_limit}. Latest price: {self.item.price}")
