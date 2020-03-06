__author__ = 'chansen'

import pymongo
from typing import Dict

class Database(object):
    URI = "mongodb://127.0.0.1:27017/pricing"
    DATABASE = pymongo.MongoClient(URI).get_database()

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['eye-price-fullstack']

    @staticmethod
    def insert(collection: str, data: Dict):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find_one(collection: str, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def find(collection: str, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def delete_one(collection: str, query):
        return Database.DATABASE[collection].delete_one(query)

    @staticmethod
    def delete_many(collection: str, query):
        return Database.DATABASE[collection].delete_many(query)
