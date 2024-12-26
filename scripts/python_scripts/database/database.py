import os

import pymongo
from dotenv import load_dotenv
from pymongo import MongoClient, collection

class Database:
    def __init__(self):
        """
        Loads cluster from database
        """
        load_dotenv()
        self.__cluster = MongoClient(os.getenv("MONGODB_KEY"))

    def get_database(self, database_name : str):
        return self.__cluster[database_name]

    def populate_database(self, database_name : str, collection_name : str, documents : list[dict]) -> None:
        pass

    @staticmethod
    def reset_collection(c : pymongo.collection.Collection) -> None:
        c.delete_many({})


