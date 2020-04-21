from dataclasses import dataclass, field
from typing import Dict
from uuid import uuid4

from models.model import Model
from models.item import Item
from models.user import User
from libs.mailgun import Mailgun 

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

    def notify_price_reached(self) -> None:
        self.item.load_price()
        if self.item.price < self.price_limit:
            Mailgun.send_email(
                user_email=User.get_by_id(self.user_id).email,
                subject=f"Sale for item: {self.item.name}",
                text=f"Your item '{self.item.name}' has reached a price below {self.price_limit}! Latest price is {self.item.price}. Click {self.item.url} to visit item page.",
                html=f"<p>Your alert {self.item.name} has triggered and the item is priced under: {self.price_limit}.</p><p>The latest price is {self.item.price}. Visit item page <a href={self.item.url}>here</a>.</p> ")
