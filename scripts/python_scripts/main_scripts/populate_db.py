import pandas as pd

from scripts.python_scripts.database.database import Database
from scripts.python_scripts.database.document import DocumentYoutube

class DBPopulator:
    def __init__(self, path : str):
        self.__dataframe = self.__decompress_path(path)
        #s
        dictionary = {
            '../database/csv_files/US_yt_data.csv':
                {'database': 'Youtube_Database', 'collection': 'youtube_data','type':'DocumentYoutube'},

            '../database/csv_files/NVIDIA_data.csv':
                {'database': 'Company_Database', 'collection': 'nvidia_data','type':'DocumentCompany'},

            '../database/csv_files/IBM_data.csv':
                {'database': 'Company_Database', 'collection': 'ibm_data', 'type': 'DocumentCompany'},

            '../database/csv_files/DELL_data.csv':
                {'database': 'Company_Database', 'collection': 'dell_data', 'type': 'DocumentCompany'},

            '../database/csv_files/INTC_data.csv':
                {'database': 'Company_Database', 'collection': 'intel_data', 'type': 'DocumentCompany'},

            '../database/csv_files/MSFT_data.csv':
                {'database': 'Company_Database', 'collection': 'microsoft_data', 'type': 'DocumentCompany'},

            '../database/csv_files/SONY_data.csv':
                {'database': 'Company_Database', 'collection': 'sony_data', 'type': 'DocumentCompany'},

        }
        self.__db_obj = Database()
        print(self.__dataframe.shape)
        self.__db_obj.populate_database( database_name = dictionary[path]["database"], collection_name = dictionary[path]["collection"],batch_percentage = 5,  dataframe = self.__dataframe, document_type = dictionary[path]["type"] )


    @staticmethod
    def __decompress_path(path: str) -> pd.DataFrame:
        df = pd.read_csv(path)
        return df


if __name__ == '__main__':
    path = '../database/csv_files/US_yt_data.csv'
    dbpopulator = DBPopulator(path)
