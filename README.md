# OnceHuman Chatbot
Before running any of the projects, please create a virtual environment first. The steps for Windows OS is as follows (ensure that you're on the top-level directory):
1. `py -m venv venv`
2. `venv\Scripts\activate`
3. Run `deactivate` when want to quit venv

## Scrape Once Human Wiki
This operation is done one time (during the beginning of the project) or occassionally when there's a major update that affect the game's mechanic, storyline, or overall content. It's achieved using Scrapy whereas the installation steps are as follow:
1. `scrapy startproject oncehuman_wiki`
2. `scrapy crawl wiki -O data/<output-filename>.json` if want to start crawling the pages.

### Why use Scrapy?
- It offers comprehensive set of tools and interfaces that make the development of scraping spiders easier. 
- It provides enhanced speed and performance compared to alternatives like BeautifulSoup4 and Selenium through concurrent requests. 
- It has powerful scheduler that allows filtering duplicate requests to avoid wastage of resources. In our case, there are pages that has links that points to each other which may cause the scrapers to be in deadlock state (crawling loops). Scrapy can avoid this with their scheduler that is equipped with duplication filter.
