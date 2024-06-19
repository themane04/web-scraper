## Purpose of the Script

The script is designed to extract data from various news websites and store it in a PostgreSQL database. It enables semi-automatic collection of article data, including title, text, publication date, and author.

## Goals and Requirements

* Semi-automatically (i.e., manually confirmed and executed) scrape news articles from various websites.
* Store the collected data in a PostgreSQL database.
* Implement robust error handling (no unexpected errors) and efficient data storage (no unused or unnecessary columns or file types).

## Approach

* Develop a Database class to manage the PostgreSQL database.
* Develop a Scraper class to retrieve and parse HTML content.
* Implement specific parsing methods for different news websites.
* Use a switch-case structure to select the appropriate scraper based on the URL.

## Diagrams and Video

### Video

You can find the video [here](/02_Marjan/webScraper.mp4).

### PAP / Flowchart / Structure Diagram

![Diagram](/01_Leonid/m122_lb2_diagram.drawio.png)

Description: The diagram shows the flow of the script from URL input through scraping and parsing of the data to storing it in the database.

### Test Case

![Test Case](/01_Leonid/m122_lb2_testcase.drawio.png)

Description: The diagram shows how the script reacts in various test cases, including successful and error scenarios.

### Use Case

![Use Case](/01_Leonid/m122_lb2_usecase.drawio.png)


Description: The three diagrams show the flow of the script in various normal scenarios, including input, scraping, and storing the data.

## Script/Program

### Technology

* Python
* PostgreSQL
* Libraries: requests, BeautifulSoup, psycopg2

### Input and Output

* Input: URLs of news websites via CLI or file
* Output: Stored article data in the PostgreSQL database, and in the CLI

### Control Structures

* try-except blocks for error handling in HTTP requests
* switch-case structure to select the appropriate scraper
* Loops to process multiple URLs

## Operation

### Installation

#### 1. Install the virtual environment (.venv):

```bash
python -m venv venv
```

#### 2. Activate the environment:

```bash
# Windows
.venv\Scripts\activate.ps1
```

```bash
# Linux
. venv/bin/activate
```

#### 3. Install the required libraries:

```bash
pip install -r requirements.txt
```

#### 4. Run the script:

```bash
python main.py
```

## Error-Handling

* Use try-except blocks to handle HTTP errors and database errors.
* Validate HTML content before processing.
* Ensure data integrity by using ON CONFLICT DO NOTHING when inserting into the database.

## Test Cases

* Successful scraping: Data is correctly extracted from the website and stored in the database.
* HTTP errors: Handling pages that cannot be loaded.
* Missing elements: Handling articles that lack title, publication date, or author.

### List of Main Test Cases or References to Test Documentation

* Test Case 1: Scraping a functioning website.
* Test Case 2: Handling an unreachable website.
* Test Case 3: Processing a website with missing article details.

## Integration and Security

### Implementation

* Integration of the scraper with a PostgreSQL database for storing collected data.
* Modular structure for easy extension to additional websites.

### Security

* Securing the database connection by safely storing credentials.
* Robustness against invalid or unexpected HTML content.

## Reflection

### Result

The script enables efficient and automatic collection of article data from various news websites and stores it in a PostgreSQL database.

### Collaboration

The development of the script involved continuous improvements and integration of feedback.

It was also helpful that we designed a clear process for the script from the beginning, meeting all criteria.

### Conclusion

It was an educational project where much was learned about databases and their application within scripts. Valuable insights were also gained regarding the OOP method. The collaboration was good, and it was enjoyable to work with such competent people.
