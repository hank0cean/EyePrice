from typing import Dict
import pymongo

class Database(object):
    URI = "mongodb://127.0.0.1:27017/pricing"
    DATABASE = pymongo.MongoClient(URI).get_database()

    @staticmethod
    def insert(collection: str, data: Dict):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find_one(collection: str, query: Dict) -> Dict:
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def find(collection: str, query: Dict) -> pymongo.cursor:
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def update(collection: str, query: Dict, data: Dict) -> None:
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection: str, query: Dict) -> Dict:
        return Database.DATABASE[collection].remove(query)

    @staticmethod
    def delete_one(collection: str, query: Dict) -> pymongo.cursor:
        return Database.DATABASE[collection].delete_one(query)

    @staticmethod
    def delete_many(collection: str, query: Dict) -> pymongo.cursor:
        return Database.DATABASE[collection].delete_many(query)
