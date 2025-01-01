import os

import pandas as pd
import pymongo
from dotenv import load_dotenv
from pymongo import MongoClient, collection
from scripts.python_scripts.database.document import DocumentCompany, DocumentYoutube


class Database:
    def __init__(self):
        """
        Loads cluster from database
        """
        load_dotenv()
        self.__cluster = MongoClient(os.getenv("MONGODB_KEY"))

    def get_database(self, database_name : str):
        return self.__cluster[database_name]

    @staticmethod
    def build_documents(document_type : str, dataframe : pd.DataFrame) -> list[dict]:
        df_dict: list[dict] = dataframe.to_dict(orient='records')
        if document_type == "DocumentCompany":
            return [DocumentCompany(document).get_document() for document in df_dict]
        elif document_type == "DocumentYoutube":
            return [DocumentYoutube(document).get_document() for document in df_dict]

    def populate_database(self, database_name : str, collection_name : str, batch_percentage : int, dataframe : pd.DataFrame, document_type : str) -> None:
        """
                :param batch_percentage: must be between 1 and 100
                :return:
                """

        if not (1 <= batch_percentage <= 100):
            raise ValueError("batch_percentage must be between 1 and 100")

        db = self.get_database(database_name)
        collection = db[collection_name]

        self.reset_collection(collection)

        documents = self.build_documents(document_type, dataframe)

        # BATCH PROCESS
        batch_size = max(1, int(dataframe.shape[0] * (batch_percentage / 100)))  # de forma a nao existir floats e a divisão ocorrer sem problemas

        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            try:
                collection.insert_many(batch, ordered=False)
                print(f"Inserted batch {i // batch_size + 1} with {len(batch)} documents.")
            except Exception as e:
                print(f"Error inserting batch {i // batch_size + 1}: {e}")

    @staticmethod
    def reset_collection(c : pymongo.collection.Collection) -> None:
        c.delete_many({})


