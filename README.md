# OnceHuman Chatbot
Before running any of the projects, please create a virtual environment first. The steps for Windows OS is as follows (ensure that you're on the top-level directory):
1. `py -m venv venv`
2. `venv\Scripts\activate`
3. Run `deactivate` when want to quit venv

## Key Highlights
1. Scrapy is used to crawl the webpages in [Once Human Wiki](https://once-human.fandom.com/wiki/Main_Page) to ensure performant scraping of large number of web pages.
2. `Airflow` is used to automate and orchestrate the daily extraction of data from Reddit so that the LLM can keep up to date with the game information and events.
3. `Pinecone` vector database is used to power the quick and efficient document retrieval process to ensure smooth chat experience with the LLM.
4. `llama-3.1-70b-versatile` from [Chat Groq](https://console.groq.com/docs/models) is used to power the AI Chatbot as it provides huge large context window (128k tokens) and maximum token output length (8k tokens).
5. Front-end is powered by `Streamlit` which the repository can be found in [Streamlit frontend project for Once Human chatbot](https://github.com/HkFromMY/oncehuman-frontend).

## Data Architecture
![Screenshot](https://github.com/HkFromMY/oncehuman-chatbot/blob/main/asset/data_architecture.png)

## Structure of the Repo
- `asset`: For images of the data architecture.
- `notebooks`: Directory to store the notebooks used to find insights or experimenting with the external API.
- `oncehuman_wiki`: The `scrapy` directory to scrape the data from Once Human wiki website.
- `reddit_airflow`: The directory for all `airflow` related files like DAGs, ETL tasks, and pipelines.

## Schedules of the data extracts
- For data from Once Human wiki website, the data is scraped one time during the beginning of the project as the websites only updates after major updates.
- Reddit posts are scraped and extracted on a daily basis. 

# Technical Notes & Findings
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

### How to connect Airflow with GCS?
1. Create service account on IAM by assigning the right permission (following least-privilege principle).
2. Export the key in JSON format.
3. Place the desired JSON key in Airflow directory.
4. Make sure the filepath is correctly configured in `docker-compose.yaml` with the following lines:
```
    GOOGLE_APPLICATION_CREDENTIALS: /opt/airflow/gcs_service_account.json
    AIRFLOW_CONN_GOOGLE_CLOUD_DEFAULT: 'google-cloud-platform://?extra__google_cloud_platform__key_path=/opt/airflow/gcs_service_account.json'
```
5. Also ensure that the key is in the docker container by configuring `volumes` key.

## Some useful PostgresSQL commands
- `\l` to list all databases
- `\c <DATABASE-NAME>` to connect to that database (equivalent to `USE DATABASE <DATABASE-NAME>` in SQL Server)
- `\dt` to list all tables in the database connected.

## Loading data to PostgresSQL
- Refer to `sql/` folder in `dags/` directory for table definition.
- Data is loaded using `to_sql()` method provided by `pandas`, `chunksize` is configured to load data efficient bit by bit to avoid clumping the database with a lot of data at once.
- Better alternative would be using BigQuery as data lake used is GCS, not only that, but the data type supported is also rich like `ARRAY` which can help querying faster.

## Problems with Reddit
- The time filter can only works for current `day`, `week`, and `month`. This means that it is impossible to filter by a date period which can cause problems because usually a post can take time to grow engagement.
- Thus, a workaround is proposed which is to create another pipeline that does the same thing but on a monthly basis. In this pipeline, it will update the existing posts in the database and add new items/comments. 

## Embedding Model References:
- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
- [all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2)
- [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)

## Challenges Faced
- The airflow project consumes too much RAM memory because initially `HuggingFaceEmbeddings` was used which downloads the embedding and run the model locally. This can cause latency to the system and does not follow best practice as Airflow is an orchestrator. 
- Switching to embedding endpoint also leads to `500: Internal Server Error` by `HuggingFaceEndpointEmbeddings` because there are too many number of documents to be embed at once, so the model timeout. 

## Solutions
- Embed the documents by batches to avoid overwhelming the model and cause errors.
