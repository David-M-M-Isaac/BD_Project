from bson import ObjectId
import pandas as pd


class Document:
    def __init__(self):
        """ Abstract class document """
        self.__doc = {'_id': ObjectId()}

    def get_document(self) -> dict:
        return self.__doc


class DocumentCompany(Document):
    def __init__(self, data : dict) -> None:
        """ Creates a document for a Company. \n
        Receives a dictionary and converts to an object. \n
        ++Input Data format:++ {'a': 1, 'b': 2, 'c': 3} \n
        ++DocumentCompany format:** \n

        {'date': data, \n
        'open_price': float, \n
        'highest_price': float, \n
        'lowest_price': float, \n
        'close_price': float, \n'
        'adj_close_price': float, \n'
        'shares': int,}

        """

        super().__init__()
        self.__doc = self.get_document()

        for key, value in data.items():
            self.__doc[key] = value

    def __repr__(self) -> str:
        return self.__doc['video_id']

class DocumentYoutube(Document):
    def __init__(self, data : dict) -> None:
        """ Creates a document for YouTube.\n
        Receives pandas series and converts to a dictionary.\n
        **Input Data format:** {'a': 1, 'b': 2, 'c': 3} \n
        **DocumentYoutube format:** \n

         {'video_id': str,\n
         'title': str,\n
         'publishedAt': datetime,\n
         'channelId': str,\n
         'channelTitle': str,\n
         'categoryId': str,\n
         'trending_date': datetime,\n
         'tags': list,\n
         'view_count': int,\n
         'likes': int,\n
         'dislikes': int,\n
         'comment_count': int,\n
         'thumbnail_link': str,\n
         'comments_disabled': bool,\n
         'ratings_disabled': bool,\n
         'description': str,}

         """
        super().__init__()
        self.__doc = self.get_document()

        for key, value in data.items():
            self.__doc[key] = value


    def __repr__(self) -> str:
        return self.__doc['video_id']

