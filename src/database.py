import psycopg2
from colorama import Fore, Style

from src.variables import MIN_URL


class Database:
    """
    Database class to handle the database connection and operations for the web scraper
    """

    def __init__(self, db_params):
        self.table_name = 'lb2_m122'
        self.db_params = db_params
        self.conn = psycopg2.connect(**self.db_params)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """
        Create the table if it doesn't exist in the database
        :return: None
        """
        self.cur.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id SERIAL PRIMARY KEY,
                title varchar(255) UNIQUE NOT NULL,
                time TIMESTAMP NOT NULL,
                autor varchar(255) NOT NULL,
                text text NOT NULL
            );
            """
        )
        self.conn.commit()

    def display(self, index):
        """
        Display the record with the given index from the database
        :param index: Index(ID) of the record to display
        :return: None
        """
        try:
            self.cur.execute(f"SELECT * FROM {self.table_name} WHERE id = {index};")
            result = self.cur.fetchone()
            if result:
                print(result[1], result[4], '\n', result[2], '\n', result[3])
            else:
                print(
                    Fore.RED + f"Warning: No record found with the ID {index}."
                               f" Please ensure you're entering a valid ID that exists in the database."
                    + Style.RESET_ALL)
                return None
        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}" + Style.RESET_ALL)
            return None

    def count_rows(self):
        """
        Count the total number of records in the database table
        :return: Total number of records
        """
        count_query = f"SELECT COUNT(*) FROM {self.table_name};"
        self.cur.execute(count_query)
        count = self.cur.fetchone()[0]
        return count

    def store_data(self, data, url):
        """
        Store the scraped data in the database table if it doesn't already exist
        :param data: Data to store in the database
        :param url: URL of the page from which the data was scraped
        :return: None
        """
        insert_query = f"""
            INSERT INTO {self.table_name} (title, time, autor, text)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (title) DO NOTHING;
        """
        try:
            if MIN_URL in url:
                data_to_insert = data[0]
            else:
                data_to_insert = data

            self.cur.execute(insert_query, data_to_insert)
            self.conn.commit()
        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}" + Style.RESET_ALL)

    def close(self):
        """
        Close the database connection
        :return: None
        """
        self.cur.close()
        self.conn.close()
