import re
import sys
from getpass import getpass

from src.database import Database
from src.scraper import Scraper, BLICK_URL, MIN_URL
from colorama import init, Fore, Style

# Initialize colorama
init()

# URLS to scrape
URLS = [BLICK_URL, MIN_URL]

# URL regex pattern to validate a wide range of URLs
url_pattern = re.compile(
    r'^(https?://)?'                                # optional http or https
    r'([\w-]+\.)+'                                  # subdomain or domain
    r'([a-z.]{2,6})(:[0-9]{1,5})?'                  # domain extension and optional port
    r'(/[\w.,@?^=%&:;/~+#-]*[\w@?^=%&;/~+#-])?$'    # path
)

# Database connection parameters
db_params = {
    'dbname': 'web_scraper',
    'host': 'localhost',
    'port': '5432'
}


def exit_app():
    """
    Exit the application and print a message to the user before exiting
    :return: None
    """
    print(Fore.GREEN + "Exiting...")
    sys.exit()


def check_file(path):
    """
    Check if the file exists and read the file content if it exists
    :param path: File path to read
    :return: List of URLs from the file
    """
    allowed_extensions = ['.txt', '.csv']
    if not any(path.endswith(ext) for ext in allowed_extensions):
        print(
            Fore.RED + f"Invalid file extension. Allowed extensions are: {', '.join(allowed_extensions)}" + Style.RESET_ALL)
        return None

    try:
        with open(path, 'r') as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(Fore.RED + "File not found." + Style.RESET_ALL)
        return None


def check_direcotry(file):
    """
    Check if the file path is valid for both Linux and Windows
    :param file: File path to check for validity
    :return: True if the file path is valid, False otherwise
    """
    return re.match(r'^(/[a-zA-Z0-9_\-./]+)+$', file) or re.match(
        r'^[a-zA-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*$', file)


def scrape_data(url, scraper, database):
    """
    Scrape data from the URL and save it to the database
    :param url: URL to scrape
    :param scraper: Scraper object
    :param database: Database object
    :return: None
    """
    data = scraper.scrape(url)
    print(*data)
    while True:
        save = input("Do you want to save this data? (y/n): ")
        if save in ['y', 'Y', 'yes', 'Yes', 'n', 'N', 'no', 'No']:
            break
        print(Fore.RED + "Invalid input." + Style.RESET_ALL)
    if save in ['y', 'Y', 'yes', 'Yes']:
        database.store_data(data, url)


def main():
    """
    Main function to run the application and interact with the user
    :return: None
    """
    print("Welcome to the web scraper!\n")
    # Check DB Login
    while True:
        print("Please enter your database credentials. Or type 'exit' to exit the application.")
        username = input("Username: ")
        if username == 'exit':
            exit_app()
        password = getpass("Password: ")
        if password == 'exit':
            exit_app()
        db_params['user'] = username
        db_params['password'] = password
        try:
            database = Database(db_params)
            print(Fore.GREEN + "Successfully connected to the database." + Style.RESET_ALL)
            break
        except:
            print(Fore.RED + "Invalid credentials. Please try again." + Style.RESET_ALL)

    # Create scraper object
    scraper = Scraper()

    while True:
        # Command line interface
        print("""
                    Choose one of the following commands:
                    - exit: Exit the application.
                    - display: Display a record from the database.
                    - path: Enter a file path to scrape multiple URLs.
                    - url: Enter a URL to scrape.
            """)

        command = input("\nChoice: ")

        if re.match(r'exit', command) or re.match(r'e', command):
            database.close()
            exit_app()
        elif re.match(r'display', command):
            print(f"Total records in the database: {database.count_rows()}")
            index = input("Enter the ID of the record you want to display: ")
            database.display(index)
        elif re.match(r'path', command):
            urls = input("Enter the file path: ")
            if check_direcotry(urls):
                urls = check_file(urls)
                if not urls:
                    print(Fore.RED + "No URLs found or error reading file." + Style.RESET_ALL)
                    continue
                for url in urls:
                    scrape_data(url, scraper, database)
            else:
                print(Fore.RED + "Invalid file path format. Please enter a correct path." + Style.RESET_ALL)
        elif re.match(r'url', command, re.IGNORECASE):
            command = input("Enter the URL you want to scrape: ")
            if not url_pattern.match(command):
                print(Fore.RED + "Invalid URL. Please enter a valid URL." + Style.RESET_ALL)
                continue
            scrape_data(command, scraper, database)
        else:
            print(Fore.RED + "Invalid command." + Style.RESET_ALL)

    # Close database connection
    database.close()


if __name__ == '__main__':
    main()
    exit()
