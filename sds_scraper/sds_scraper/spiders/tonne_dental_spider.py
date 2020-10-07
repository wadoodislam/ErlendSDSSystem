import os

from . import SDSBaseCrawlSpider
from ..items import SdsScraperItem


class Mixin:
    provider = 'tonne_dental'
    manufacturer = 'Tonne Dental'
    source = os.path.basename(__file__)
    start_urls = ['https://www.tonnedental.no/datablader/']


class TonneDentalCrawlSpider(Mixin, SDSBaseCrawlSpider):
    name = Mixin.provider + '_crawl'

    def parse_start_url(self, response, **kwargs):
        for url in response.css('p a::attr(href)').getall():
            sds_scraper_item = SdsScraperItem()
            sds_scraper_item['file_urls'] = [url]
            sds_scraper_item['file_display_name'] = url.split('/')[-1].replace('_' or '-', ' ').split('.')[0] + ".pdf"
            yield sds_scraper_item
