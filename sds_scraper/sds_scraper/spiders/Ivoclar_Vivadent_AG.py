from datetime import datetime

import scrapy
from scrapy import Selector
from scrapy.spiders import CrawlSpider

from ..items import SdsScraperItem


class IvoclarVivadent(CrawlSpider):
    name = 'ivoclar_vivadent'
    base_url = 'https://www.ivoclarvivadent.se/'

    def start_requests(self):
        urls = ['https://www.ivoclarvivadent.se/sv/skerhetsdatablad/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        sds_scraper_item = SdsScraperItem()
        for items in response.css('div.text').getall():
            name = Selector(text=items).css('a::text').re(r'.*_NO')
            url = Selector(text=items).css('a::attr(href)').re(r'.*_NO')
            if name and url:
                sds_scraper_item['source'] = 'Ivoclar_Vivadent_AG.py'
                sds_scraper_item['manufacturer'] = 'Ivoclar Vivadent AG'
                sds_scraper_item['file_display_name'] = name[0]
                sds_scraper_item['file_urls'] = [self.base_url + url[0]]
                sds_scraper_item['crawl_date'] = datetime.now().date().strftime('%d.%m.%Y')
                yield sds_scraper_item

