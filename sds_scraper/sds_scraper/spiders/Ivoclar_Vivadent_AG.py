from datetime import datetime

import scrapy
from scrapy import Selector
from scrapy.spiders import CrawlSpider


class IvoclarVivadent(CrawlSpider):
    name = 'ivoclar_vivadent'
    base_url = 'https://www.ivoclarvivadent.se/'

    def start_requests(self):
        url = 'https://www.ivoclarvivadent.se/sv/skerhetsdatablad/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 1769 files
        for items in response.css('div.text').getall():
            name = Selector(text=items).css('a::text').re(r'.*_NO')
            url = Selector(text=items).css('a::attr(href)').re(r'.*_NO')
            if name and url:
                yield {
                    'source': 'Ivoclar_Vivadent_AG.py',
                    'manufacturer': 'Ivoclar Vivadent AG',
                    'file_display_name': name,
                    'url': self.base_url + url[0],
                    'crawl_date': datetime.now().date().strftime('%d.%m.%Y')
                }
