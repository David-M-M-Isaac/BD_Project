from scripts.python_scripts.database.database import Database
import datetime

class ReportGenerator:
    def __init__(self):
        self.db_obj = Database()
        self.db = self.db_obj.get_database('Relatorio')

    def generate_report(self, c : list[str], date_interval : tuple[datetime, datetime]):
        try:
            companies = [company.lower() for company in c]
            start_date = date_interval[0]
            end_date = date_interval[1]

            for company in companies:
                collection = self.db[company]
                query = {"day": {"$gte": start_date, "$lte": end_date}}

                documents = collection.find(query)
                for document in documents:
                    self.print_report(document)

        except Exception as e:
            print('Error generating report.')
        finally:
            self.db_obj.close()

    def print_report(self, document):
        print('-'*30)
        print(f'---- Company {document["company"].capitalize()} ----')
        print(f'Day {document["day"]}')
        print(f'---- YouTube Views ----')
        print(f'Total Views: {document["total_views"]}')
        print(f'Total Likes: {document["total_likes"]}')
        print(f'Total Dislikes: {document["total_dislikes"]}')
        print(f'Total Comments: {document["total_coments"]}')
        print(f'Top Video: {document["top_video"]}')
        print(f'Highest Stock Value: {document["stock_high"]}')
        print(f'Lowest Stock Value: {document["stock_low"]}')
        print(f'Volume: {document["volume"]}')
        print(f'Last Stock Value: {document["final_stocks"]}')
        print(f'Adjusted Closing Price: {document["stocks_movement"]}')
        print('-' * 30)

if __name__ == '__main__':
    report_generator = ReportGenerator()

    companies = ['Dell', 'Sony']
    start_date = datetime.datetime(2020, 8, 11)
    end_date = datetime.datetime(2021, 8, 11)
    date_interval = (start_date, end_date)
    report_generator.generate_report(companies, date_interval)