# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from markdownify import markdownify
import os 

class OncehumanWikiPipeline:
    """
        Do some post-processing after extraction and validation checks to ensure data quality
        Validtion:
            1. Check for duplicate items
            2. Check for empty text

        Post-processing:
            1. Convert HTML to markdown
            2. Remove extra newlines in the markdown text
    """
    def __init__(self):
        self.title_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['title'] in self.title_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        
        elif adapter['text'] == '':
            raise DropItem(f"Empty text found: {item!r}")
        
        else:
            # processing
            html_code = adapter.get('text')
            markdown_text = markdownify(html_code)
            markdown_text = os.linesep.join([s for s in markdown_text.splitlines() if s])
            adapter['text'] = markdown_text

            self.title_seen.add(adapter['title'])
            return item
