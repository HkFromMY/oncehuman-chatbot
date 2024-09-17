# OnceHuman Chatbot
Before running any of the projects, please create a virtual environment first. The steps for Windows OS is as follows (ensure that you're on the top-level directory):
1. `py -m venv venv`
2. `venv\Scripts\activate`
3. Run `deactivate` when want to quit venv

## Scrape Once Human Wiki
This operation is done one time (during the beginning of the project) or occassionally when there's a major update that affect the game's mechanic, storyline, or overall content. It's achieved using Scrapy whereas the installation steps are as follow:
1. `scrapy startproject oncehuman_wiki`
2. `scrapy crawl wiki -O data/<output-filename>.json` if want to start crawling the pages.
