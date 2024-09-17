# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class OncehumanWikiItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date_scraped = Field()
    title = Field() 
    source_url = Field()
    text = Field()

