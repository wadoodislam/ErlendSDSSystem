# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SdsScraperItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
    source = scrapy.Field()
    manufacturer = scrapy.Field()
    file_display_name = scrapy.Field()
    languages = scrapy.Field()
    date = scrapy.Field()
    document_type = scrapy.Field()
    file_type = scrapy.Field()
    crawl_date = scrapy.Field()
    provider = scrapy.Field()
