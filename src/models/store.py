from abc import ABC
from typing import Dict
from uuid import uuid4
import re

from models.model import Model

class Store(Model):
    collection = 'stores'

    def __init__(self, name: str, url_prefix: str, tag_name: str, query: Dict, _id: str = None):
        super().__init__()
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self._id = _id or uuid4().hex

    def __repr__(self):
        return f'<Store {self.url_prefix}>'

    def json(self) -> Dict:
        return {
            'name': self.name,
            'url_prefix': self.url_prefix,
            'tag_name': self.tag_name,
            'query': self.query,
            '_id': self._id
        }

    @classmethod
    def get_by_name(cls, store_name: str) -> "Store":
        return cls.find_one_by('name', store_name)

    @classmethod
    def get_by_url_prefix(cls, url_prefix: str) -> "Store":
        url_regex = {"$regex": "^{}".format(url_prefix)}
        return cls.find_one_by('url_prefix', url_regex)

    @classmethod
    def find_by_url(cls, url: str) -> "Store":
        """
        Return Store object for the given url. Ex) "https://store.steampowered.com/app/1241700/"
        :param url:     The item's url
        :return:        a Store object
        """
        pattern = re.compile(r"(https?://.*?/)")
        match = pattern.search(url)
        url_prefix = match.group(1)
        return cls.get_by_url_prefix(url_prefix)
