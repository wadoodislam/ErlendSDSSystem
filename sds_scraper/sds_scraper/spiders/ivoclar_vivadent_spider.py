import os

from scrapy import Selector

from . import SDSBaseCrawlSpider
from ..items import SdsScraperItem


class Mixin:
    provider = 'ivoclar_vivadent'
    manufacturer = 'Ivoclar Vivadent AG'
    source = os.path.basename(__file__)
    start_urls = ['https://www.ivoclarvivadent.se/sv/skerhetsdatablad/']


class IvoclarVivadentCrawlSpider(Mixin, SDSBaseCrawlSpider):
    name = Mixin.provider + '_crawl'

    def parse_start_url(self, response, **kwargs):
        for items in response.css('div.text').getall():
            name = Selector(text=items).css('a::text').re(r'.*_NO')
            url = Selector(text=items).css('a::attr(href)').re(r'.*_NO')
            if name and url:
                sds_scraper_item = SdsScraperItem()
                sds_scraper_item['file_display_name'] = name[0] + '.pdf'
                sds_scraper_item['file_urls'] = [response.urljoin(url[0])]
                yield sds_scraper_item
