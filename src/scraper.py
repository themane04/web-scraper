import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style
from src.variables import BLICK_ARTICLE, BLICK_AUTOR, BLICK_TIME, BLICK_TITLE, BLICK_URL, MIN_ARTICLE, MIN_AUTOR, \
    MIN_PARAGRAPH, MIN_SUB_TITLE, MIN_TEXT, MIN_TIME, MIN_TITLE, MIN_UNWANTED_VON_ELEMENT, MIN_URL


class Scraper:
    """
    Scraper class to handle the scraping of the web pages and parsing the data
    """

    def __init__(self):
        self.session = requests.Session()

    def fetch_page(self, url):
        """
        Fetch the page content from the given URL using the requests library
        :param url: URL of the page to fetch
        :return: HTML content of the page
        """
        try:
            response = self.session.get(url)
        except requests.RequestException as e:
            raise Exception(Fore.RED + f"Failed to load page {url}" + Style.RESET_ALL)
        return response.content

    def parse_20min_ch(self, html_content):
        """
        Parse the HTML content from 20min.ch and extract the title, time, author, and text
        :param html_content: HTML content of the page
        :return: Parsed data
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = soup.select(MIN_ARTICLE)
        data = []

        for article in articles:
            title_elem = article.select_one(MIN_TITLE)
            title = title_elem.get_text(strip=True)

            time_elem = article.select_one(MIN_TIME)
            time = time_elem['datetime']

            # uncomment the following lines to pass the tests and comment the line above
            # time_string = time_elem['datetime']
            # time = datetime.fromisoformat(time_string[:-1])

            autor_elem = article.select_one(MIN_AUTOR)
            if autor_elem:
                for unwanted in autor_elem.find_all(class_=MIN_UNWANTED_VON_ELEMENT):
                    unwanted.decompose()
            autor = autor_elem.get_text(strip=True)

            text = ''
            current_tag = article.select_one(
                MIN_TEXT)

            while current_tag:
                if current_tag.name == 'div' and MIN_PARAGRAPH in current_tag.get('class', []):
                    text += current_tag.get_text(strip=True) + '\n'
                elif current_tag.name == 'div' and MIN_SUB_TITLE in current_tag.get('class', []):
                    text += f'\n{current_tag.get_text(strip=True)}\n'

                current_tag = current_tag.find_next()
                if current_tag and not article in current_tag.parents or current_tag is None:
                    break

            data.append((title, time, autor, text))

        return data

    @staticmethod
    def parse_datetime_from_string(time_string):
        """
        Parse the datetime from the given string in the format "dd.mm.yyyy um hh:mm Uhr" or "hh:mm Uhr"
        :param time_string: Time string to parse the datetime from
        :return: Parsed datetime
        """
        datetime_pattern = re.compile(r'(\d{2}\.\d{2}\.\d{4}) um (\d{2}:\d{2}) Uhr')
        time_pattern = re.compile(r'(\d{2}:\d{2}) Uhr')
        datetime_match = datetime_pattern.search(time_string)
        if datetime_match:
            date_str, time_str = datetime_match.groups()
            combined_datetime = datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M")
            return combined_datetime

        time_match = time_pattern.search(time_string)
        if time_match:
            time_str = time_match.group(1)
            hours, minutes = map(int, time_str.split(':'))
            current_date = datetime.today()
            combined_datetime = current_date.replace(hour=hours, minute=minutes, second=0, microsecond=0)
            return combined_datetime

        return None

    def parse_blick_ch(self, html_content):
        """
        Parse the HTML content from Blick.ch and extract the title, time, author, and text
        :param html_content: HTML content of the page
        :return: Parsed data
        """
        soup = BeautifulSoup(html_content, 'html.parser')

        title = soup.find('h2', class_=BLICK_TITLE).get_text(strip=True)
        time = soup.find('div', class_=BLICK_TIME).get_text(strip=True)

        time = self.parse_datetime_from_string(time)

        autor = soup.find('span', class_=BLICK_AUTOR).get_text(strip=True)

        article = soup.find('article', class_=BLICK_ARTICLE)

        current_tag = article.find()

        text = ''

        while True:
            if current_tag.name == 'p':
                text += current_tag.get_text(strip=True) + '\n'
            elif current_tag.name == 'h3':
                text += f'\n{current_tag.get_text(strip=True)}\n'

            current_tag = current_tag.find_next()

            if current_tag and not article in current_tag.parents or current_tag is None:
                break

        return title, time, autor, text

    def scrape(self, url):
        """
        Scrape the given URL and return the parsed data based on the URL pattern
        :param url: URL to scrape
        :return: Parsed data
        """
        html_content = self.fetch_page(url)
        match url:
            case url if MIN_URL in url:
                return self.parse_20min_ch(html_content)
            case url if BLICK_URL in url:
                return self.parse_blick_ch(html_content)
            case _:
                raise ValueError(f"URL not supported: {url}")
