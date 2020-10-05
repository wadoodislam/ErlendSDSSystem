from datetime import datetime

import scrapy
from scrapy import Selector
from scrapy.spiders import CrawlSpider

from ..items import SdsScraperItem


class UltradentSpider(CrawlSpider):
    name = "ultradent"
    base_url = 'https://www.ultradent.com'

    def start_requests(self):
        urls = ['https://www.ultradent.com/resources/safety-data-sheets']
        for url in urls:
            yield scrapy.FormRequest(url=url,
                                     method='POST',
                                     formdata={'Language': 'Norwegian'},
                                     callback=self.parse)

    def parse(self, response, **kwargs):
        for data in response.css('ul.linkList li').getall():
            name = Selector(text=data).css('a::text').get()
            url = Selector(text=data).css('a::attr(href)').get()
            item = SdsScraperItem()
            item['source'] = 'ultradent.py'
            item['manufacturer'] = 'Ultradent Products, Inc'
            item['file_urls'] = [self.base_url + url]
            item['file_display_name'] = name
            item['crawl_date'] = datetime.now().date().strftime('%d.%m.%Y')

            yield scrapy.Request(
                url=response.urljoin(url),
                callback=self.parse_pdf,
                meta={'item': item}
            )

    def parse_pdf(self, response):
        item = response.meta.get('item', '')
        yield item
