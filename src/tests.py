import unittest
from datetime import datetime
from unittest.mock import patch, Mock, MagicMock, call
from main import exit_app, check_file, scrape_data, main
import pytest
from requests import RequestException

from scraper import Scraper
from database import Database


class TestScraper(unittest.TestCase):
    """
    Test cases for the Scraper class in scraper.py
    """

    @staticmethod
    def test_parse_blick_ch():
        """
        Test the parse_blick_ch method of the Scraper class with a sample HTML content
        """
        scraper = Scraper()
        html_content_blick = """
           <h2 class="sc-42b0166d-0 htRjAb">Blick Test Title</h2>
           <div class="sc-bb3977dc-0 gsPNmc">12.06.2024 um 14:00 Uhr</div>
           <span class="sc-4e82f8ca-0 kyLqjh">Autor Name</span>
           <article class="sc-845e3996-0 gMfVCb">
               <p>First paragraph of the article.</p>
               <h3>Subheading</h3>
               <p>Second paragraph of the article.</p>
           </article>
           """
        data = scraper.parse_blick_ch(html_content_blick)
        expected_data = (
            'Blick Test Title',
            datetime(2024, 6, 12, 14, 0),
            'Autor Name',
            'First paragraph of the article.\n\nSubheading\nSecond paragraph of the article.\n'
        )
        assert data == expected_data

    @staticmethod
    def test_parse_20min_ch():
        """
        Test the parse_20min_ch method of the Scraper class with a sample HTML content
        """
        scraper = Scraper()
        html_content_20min = """
        <article class="Article_article__sV3bX Article_siteAreaNews__Frmfx">
            <header class="Article_header__ckSlm">
                <div class="Article_elementTitle__9QPjy">
                      <h2>20min Test Title</h2>
                </div>
                <div class="Article_elementPublishdate__qcso_">
                    <div class="sc-d721210-0 glCzFI">
                        <time datetime="2024-06-12T14:00:00.000">12.06.2024 um 14:00 Uhr</time>
                    </div>
                </div>
                <div class="Article_elementAuthors__LsHcz">
                    <section class="sc-edde8439-1 ghCqoI">
                        <div class="sc-edde8439-0 bokODS">
                            <dl class="sc-bea1a0f7-0 eGqAWD">
                                <div class="sc-bea1a0f7-3 gdDZBe">
                                    <a class="sc-bea1a0f7-6 iPEoXP">
                                        <dd class="sc-bea1a0f7-2 hOUMxP">
                                            Autor Name
                                        </dd>
                                    </a>
                                </div>
                            </dl>
                        </div>
                    </section>
                </div>
            </header>
            <section class="Article_body__60Liu">
                <div class="Article_elementTextblockarray__WNyan">
                    <p>
                        First paragraph of the article.
                    </p>
                </div>
                <div class="Article_elementCrosshead__b9pyw">
                    <h2>Subheading</h2>
                </div>
                <div class="Article_elementTextblockarray__WNyan">
                    <p>
                        Second paragraph of the article.
                    </p>
                </div>
            </section>
        </article>
                """
        data = scraper.parse_20min_ch(html_content_20min)
        print("Returned data: ", data)
        expected_data = (
            '20min Test Title',
            datetime(2024, 6, 12, 14, 0),
            'Autor Name',
            'First paragraph of the article.\n\nSubheading\nSecond paragraph of the article.\n'
        )
        print("Expected data: ", expected_data)
        assert data[0] == expected_data

    @staticmethod
    def test_parse_datetime_from_string():
        """
        Test the parse_datetime_from_string method of the Scraper class with a sample time string
        """
        scraper = Scraper()
        time_string = '12.06.2024 um 14:00 Uhr'
        data = scraper.parse_datetime_from_string(time_string)
        assert str(data) == '2024-06-12 14:00:00'

    @staticmethod
    @patch('webScraper.requests.Session.get')
    def test_fetch_page(mock_get):
        """
        Test the fetch_page method of the Scraper class with a sample URL and mock response
        :param mock_get: Mocked requests.get method
        """
        scraper = Scraper()

        # Define the mock response for a successful request
        mock_response = Mock()
        mock_response.content = b'<html>Test Page Content</html>'
        mock_get.return_value = mock_response

        # Test successful fetch
        url = 'https://example.com'
        response_content = scraper.fetch_page(url)
        assert response_content == b'<html>Test Page Content</html>'

        # Define the mock response for a failed request
        mock_get.side_effect = RequestException

        # Test failed fetch
        with pytest.raises(Exception, match="Failed to load page https://example.com"):
            scraper.fetch_page(url)


class TestDatabase(unittest.TestCase):
    """
    Test cases for the Database class in scraper.py
    """

    def setUp(self):
        self.db_params = {
            'host': 'localhost',
            'database': 'test_db',
            'user': 'test_user',
            'password': 'test_password'
        }

    @patch('psycopg2.connect')
    def test_create_table(self, mock_connect):
        """
        Test the create_table method of the Database class with a mock connection and cursor
        :param mock_connect: Mocked psycopg2.connect method
        """
        # Create a mock connection and cursor
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_conn.cursor.return_value = mock_cur
        mock_connect.return_value = mock_conn

        # Create a Database instance
        db = Database(self.db_params)

        # Test that the create_table method is called
        db.create_table()
        calls = [
            call(
                '\n            CREATE TABLE IF NOT EXISTS lb2_m122 (\n                id SERIAL PRIMARY KEY,'
                '\n                title varchar(255) UNIQUE NOT NULL,\n                time TIMESTAMP NOT NULL,'
                '\n                autor varchar(255) NOT NULL,\n                text text NOT NULL\n            );\n '
                '           '),
            call(
                '\n            CREATE TABLE IF NOT EXISTS lb2_m122 (\n                id SERIAL PRIMARY KEY,'
                '\n                title varchar(255) UNIQUE NOT NULL,\n                time TIMESTAMP NOT NULL,'
                '\n                autor varchar(255) NOT NULL,\n                text text NOT NULL\n            );\n '
                '           '),
        ]
        mock_cur.execute.assert_has_calls(calls)

    @patch('psycopg2.connect')
    def test_display(self, mock_connect):
        """
        Test the display method of the Database class with a mock connection and cursor
        :param mock_connect: Mocked psycopg2.connect method
        """
        # Create a mock connection and cursor
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_conn.cursor.return_value = mock_cur
        mock_connect.return_value = mock_conn

        # Create a Database instance
        db = Database(self.db_params)

        # Test that the display method is called
        db.display(1)
        mock_cur.execute.assert_called_with('SELECT * FROM lb2_m122 WHERE id = 1;')

    @patch('psycopg2.connect')
    def test_count_rows(self, mock_connect):
        """
        Test the count_rows method of the Database class with a mock connection and cursor
        :param mock_connect: Mocked psycopg2.connect method
        """
        # Create a mock connection and cursor
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_conn.cursor.return_value = mock_cur
        mock_connect.return_value = mock_conn

        # Create a Database instance
        db = Database(self.db_params)

        # Create the table (this will call execute once)
        db.create_table()

        # Test that the count_rows method is called
        db.count_rows()
        mock_cur.execute.assert_called_with('SELECT COUNT(*) FROM lb2_m122;')

    @patch('psycopg2.connect')
    def test_store_data(self, mock_connect):
        """
        Test the store_data method of the Database class with a mock connection and cursor
        :param mock_connect: Mocked psycopg2.connect method
        """
        # Create a mock connection and cursor
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_conn.cursor.return_value = mock_cur
        mock_connect.return_value = mock_conn

        # Create a Database instance
        db = Database(self.db_params)

        # Test that the store_data method is called
        data = ('Test Title', '2022-01-01 00:00:00', 'Test Author', 'Test Text')
        db.store_data(data, 'https://example.com')
        mock_cur.execute.assert_called_with(
            '\n            INSERT INTO lb2_m122 (title, time, autor, text)\n            VALUES (%s, %s, %s, %s)\n            ON CONFLICT (title) DO NOTHING;\n        ',
            ('Test Title', '2022-01-01 00:00:00', 'Test Author', 'Test Text'))

    @patch('psycopg2.connect')
    def test_close(self, mock_connect):
        """
        Test the close method of the Database class with a mock connection and cursor
        :param mock_connect: Mocked psycopg2.connect method
        """
        # Create a mock connection and cursor
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_conn.cursor.return_value = mock_cur
        mock_connect.return_value = mock_conn

        # Create a Database instance
        db = Database(self.db_params)

        # Test that the close method is called
        db.close()
        mock_cur.close.assert_called_once()
        mock_conn.close.assert_called_once()


class TestMain(unittest.TestCase):
    """
    Test cases for the main functions in main.py and scraper.py
    """

    @patch('sys.exit')
    def test_exit_app(self, mock_exit):
        """
        Test the exit_app function in main.py with a mock exit
        :param mock_exit: Mocked sys.exit method
        """
        exit_app()
        mock_exit.assert_called_once_with()

    @staticmethod
    @patch('builtins.input', side_effect=['exit'])
    @patch('builtins.print')
    def test_exit_app_username(mock_print, mock_input):
        """
        Test the exit_app function in main.py with a mock exit and input
        :param mock_print: Mocked print method
        :param mock_input: Mocked input method
        """
        with pytest.raises(SystemExit):
            main()
        mock_print.assert_called()
        mock_input.assert_called_with("Username: ")

    def test_check_file_valid(self):
        """
        Test the check_file function in main.py with a valid file path
        """
        with open('test_file.txt', 'w') as f:
            f.write('https://example.com\nhttps://example.org')
        self.assertEqual(check_file('test_file.txt'), ['https://example.com', 'https://example.org'])
        import os
        os.remove('test_file.txt')

    def test_check_file_invalid(self):
        """
        Test the check_file function in main.py with an invalid file path
        """
        self.assertIsNone(check_file('invalid_file.txt'))

    @patch('webScraper.Database')
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['y'])
    @patch('webScraper.Scraper.scrape', return_value=[('title', 'time', 'author', 'text')])
    def test_scrape_data_yes(self, mock_scraper, mock_input, mock_print, mock_database):
        """
        Test the scrape_data function in main.py with a mock database and input
        :param mock_scraper: Mocked Scraper.scrape method
        :param mock_input: Mocked input method
        :param mock_print: Mocked print method
        :param mock_database: Mocked Database class
        """
        scraper = Scraper()
        database = mock_database.return_value
        scrape_data('https://example.com', scraper, database)
        mock_print.assert_called_with(*[('title', 'time', 'author', 'text')])
        database.store_data.assert_called_once_with([('title', 'time', 'author', 'text')], 'https://example.com')

    @patch('webScraper.Database')
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['n'])
    @patch('webScraper.Scraper.scrape', return_value=[('title', 'time', 'author', 'text')])
    def test_scrape_data_no(self, mock_scraper, mock_input, mock_print, mock_database):
        """
        Test the scrape_data function in main.py with a mock database and input
        :param mock_scraper: Mocked Scraper.scrape method
        :param mock_input: Mocked input method
        :param mock_print: Mocked print method
        :param mock_database: Mocked Database class
        """
        scraper = Scraper()
        database = mock_database.return_value
        scrape_data('https://example.com', scraper, database)
        mock_print.assert_called_with(*[('title', 'time', 'author', 'text')])
        database.store_data.assert_not_called()


if __name__ == '__main__':
    unittest.main()
