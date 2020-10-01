from datetime import datetime

import scrapy
from scrapy import Selector
from scrapy.spiders import CrawlSpider


class UltradentSpider(CrawlSpider):
    name = "ultradent"
    base_url = 'https://www.ultradent.com'

    def start_requests(self):
        url = 'https://www.ultradent.com/resources/safety-data-sheets'

        yield scrapy.FormRequest(url=url,
                                 method='POST',
                                 formdata={'Language': 'Norwegian'},
                                 callback=self.parse)

    def parse(self, response):
        test = response.css('ul.linkList li').getall()
        for data in response.css('ul.linkList li').getall():
            name = Selector(text=data).css('a::text').get()
            url = Selector(text=data).css('a::attr(href)').get()
            yield {
                    'source': 'ultradent.py',
                    'manufacturer': 'Ultradent Products, Inc',
                    'file_display_name': name,
                    'url': self.base_url + url,
                    'crawl_date': datetime.now().date().strftime('%d.%m.%Y')
            }
