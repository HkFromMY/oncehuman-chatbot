import scrapy 
import os 
from oncehuman_wiki.items import OncehumanWikiItem
from datetime import datetime

def keep_only_wiki_links(link: str) -> bool:
    return (
        link.startswith('/wiki/') and 
        "edit" not in link and 
        "section" not in link
    )

class WikiSpider(scrapy.Spider):
    name = "wiki"
    start_urls = ['https://once-human.fandom.com/wiki/Main_Page']

    def parse(self, response):
        """
        Parse the starting page and extract all links > follow links to extract content
        """
        date_scraped = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        title = response.css('title::text').get()

        # extract the main content of the page, convert to markdown, and eliminate extra newlines
        text = response.xpath('.//div[@class="fandom__main_page__left"]').extract()[0]

        # extract links (to follow)
        links_extracted = response.css("div#gallery-0 div.lightbox-caption a::attr(href)").getall()
        links_extracted = [response.urljoin(link) for link in links_extracted if not link.endswith('Mods')] # remove Mods page because it's Work in Progress
        background_story_link = response.xpath('.//a[contains(text(), "CONTINUE READING...")]//@href').get()
        background_story_link = response.urljoin(background_story_link)
        links_extracted.append(background_story_link)

        yield OncehumanWikiItem(
            date_scraped=date_scraped,
            title=title,
            source_url=response.url,
            text=text,
        )

        for link_extracted in links_extracted:
            yield scrapy.Request(
                url=link_extracted,
                callback=self.parse_individual_page
            )
        
    def parse_individual_page(self, response):
        """
        Parse the followed pages (individual pages gotten from main)
        """

        # content is in div.mw-parser-out
        main_content_area = response.xpath('.//div[@class="mw-parser-output"]')
        links_extracted = main_content_area.css('a::attr(href)').getall()
        links_extracted = list(filter(keep_only_wiki_links, links_extracted)) # ensure only crawl within once human wiki domain
        links_extracted = [response.urljoin(link) for link in links_extracted]

        # extract content
        text = main_content_area.extract()
        if len(text) == 0:
            text = '' # will be dropped in the pipeline

        else:
            text = text[0]

        title = response.css('title::text').get()
        date_scraped = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        yield OncehumanWikiItem(
            date_scraped=date_scraped,
            title=title,
            source_url=response.url,
            text=text,
        )

        if len(links_extracted) > 0:
            for link_extracted in links_extracted:
                yield scrapy.Request(
                    url=link_extracted,
                    callback=self.parse_individual_page
                )


