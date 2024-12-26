import pandas as pd

from scripts.python_scripts.database.database import Database
from scripts.python_scripts.database.document import DocumentYoutube

class DBPopulator:
    def __init__(self, path : str):
        self.__dataframe = self.__decompress_path(path)
        self.__db_obj = Database()

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

        db = self.__db_obj.get_database(database_name='Project_Database')
        collection_youtube = db['youtube_data']

        documents: list[dict] = self.__transform_into_document()

        self.__db_obj.reset_collection(collection_youtube) # Empties collection_youtube

        # BATCH PROCESS

        batch_size = self.__dataframe.shape[0] // batch_percentage

        collection_youtube.insert_many(documents, ordered=False)

if __name__ == '__main__':
    path = '../../../database/csv_files/US_yt_data.csv'
    dbpopulator = DBPopulator(path)
    dbpopulator.populate_db()