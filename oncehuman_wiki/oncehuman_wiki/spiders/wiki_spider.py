import scrapy 
import os 
from oncehuman_wiki.items import OncehumanWikiItem
from markdownify import markdownify
from datetime import datetime

class WikiSpider(scrapy.Spider):
    name = "wiki"
    start_urls = ['https://once-human.fandom.com/wiki/Main_Page']

    def parse(self, response):
        """
        Parse the starting page and extract all links > follow links to extract content
        """
        title = response.css('title::text').get()

        # extract the main content of the page, convert to markdown, and eliminate extra newlines
        html_code = response.xpath('.//div[@class="fandom__main_page__left"]').extract()[0]
        markdown_text = markdownify(html_code)    
        markdown_text = os.linesep.join([s for s in markdown_text.splitlines() if s])

        # extract links (to follow)
        links_extracted = response.css("div#gallery-0 div.lightbox-caption a::attr(href)").getall()
        links_extracted = [response.urljoin(link) for link in links_extracted if not link.endswith('Mods')] # remove Mods page because it's Work in Progress
        background_story_link = response.xpath('.//a[contains(text(), "CONTINUE READING...")]//@href').get()
        background_story_link = response.urljoin(background_story_link)
        links_extracted.append(background_story_link)

        yield OncehumanWikiItem(
            date_scraped=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            title=title,
            source_url=response.url,
            text=markdown_text
        )
        
    def parse_individual_page(self):
        """
        Parse the followed pages
        """

        # content is in div.mw-parser-out
        pass 