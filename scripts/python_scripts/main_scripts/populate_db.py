import pandas as pd

from scripts.python_scripts.database.database import Database
from scripts.python_scripts.database.document import DocumentYoutube

class DBPopulator:
    def __init__(self, path : str):
        self.__dataframe = self.__decompress_path(path)
        self.__db_obj = Database()
        print(self.__dataframe.shape)

    def get_database(self, database_name):
        return self.client[database_name]

    @staticmethod
    def __decompress_path(path: str) -> pd.DataFrame:
        df = pd.read_csv(path)
        return df

    def __transform_into_document(self) -> list[dict]:
        self.__dataframe['tags'] = self.__dataframe['tags'].apply(lambda s: s.strip().split('|'))
        df_dict : list[dict] = self.__dataframe.to_dict(orient='records')
        documents : list[dict] = [DocumentYoutube(document).get_document() for document in df_dict]
        return documents

    def populate_db(self, batch_percentage : float) -> None:
        """
        :param batch_percentage: must be between 1 and 100
        :return:
        """

        if not (1 <= batch_percentage <= 100):
            raise ValueError("batch_percentage must be between 1 and 100")

        db = self.__db_obj.get_database(database_name='Project_Database')
        collection_youtube = db['youtube_data']

        documents: list[dict] = self.__transform_into_document()

        self.__db_obj.reset_collection(collection_youtube)

        # BATCH PROCESS
        batch_size = max(1, int(self.__dataframe.shape[0] * (batch_percentage / 100))) #de forma a nao existir floats e a divisão ocorrer sem problemas

        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            try:
                collection_youtube.insert_many(batch, ordered=False)
                print(f"Inserted batch {i // batch_size + 1} with {len(batch)} documents.")
            except Exception as e:
                print(f"Error inserting batch {i // batch_size + 1}: {e}")


if __name__ == '__main__':
    path = '../database/csv_files/US_yt_data.csv'
    dbpopulator = DBPopulator(path)
    dbpopulator.populate_db(batch_percentage=5)
