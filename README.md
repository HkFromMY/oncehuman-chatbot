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

## EDA on Scraped Wiki Data
### Findings
1. The data is nicely scraped as it is converted directly from HTML to markdown which is great for LLM to understand the dataset compared to normal text as markdown provides richer features and information.
2. The text length of each page differs, but the information contained is important for the model to understand more about the game. 
3. Thus, no additional pre-processing techniques are applied since the data is ready to be fed into the model. 

## Setting up Airflow (extending Images for additional PyPi packages)
1. Edit `Dockerfile` and `docker-compose.yaml` to add additional directories like `data`, changing the build from pre-built image to extended image.
2. Run `docker compose build` to refresh the changes in `Dockerfile` and `docker-compose.yaml`.
3. Run `docker compose up airflow-init` to initialize the database
4. `docker compose up` to start the containers.
5. Can run `docker compose down --volumes --rmi all` to remove everything for cleaning up.
6. If the docker still occupying memory after shutting down all the containers, can run `wsl --shutdown` to avoid eating up computational resources.
