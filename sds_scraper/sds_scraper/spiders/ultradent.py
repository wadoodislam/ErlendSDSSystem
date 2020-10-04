import os
from datetime import datetime

import scrapy
from scrapy import Selector
from scrapy.spiders import CrawlSpider

from ..items import SdsScraperItem


class UltradentSpider(CrawlSpider):
    name = "ultradent"
    base_url = 'https://www.ultradent.com'
    FILES_STORE = '/Users/junaidikhlaq/PycharmProjects/ErlendSDSSystem/sds_scraper/sds_scraper/sds_data/Ultradent'

    def start_requests(self):
        urls = ['https://www.ultradent.com/resources/safety-data-sheets', ]
        for url in urls:
            yield scrapy.FormRequest(url=url,
                                     method='POST',
                                     formdata={'Language': 'Norwegian'},
                                     callback=self.parse)

    def parse(self, response, **kwargs):
        item = SdsScraperItem()
        for data in response.css('ul.linkList li').getall():
            name = Selector(text=data).css('a::text').get()
            url = Selector(text=data).css('a::attr(href)').get()

            if not os.path.isdir(self.FILES_STORE):
                os.mkdir(self.FILES_STORE)
            yield scrapy.Request(
                url=response.urljoin(url),
                callback=self.save_pdf
            )

            # item['source'] = 'ultradent.py'
            # item['manufacturer'] = 'Ultradent Products, Inc'
            # item['file_urls'] = self.base_url + url
            # item['file_display_name'] = name
            # item['crawl_date'] = datetime.now().date().strftime('%d.%m.%Y')
            #
            # yield item

    def save_pdf(self, response):
        path = response.url.split('/')[-1]
        complete_name = os.path.join(self.FILES_STORE, path)
        self.logger.info('Saving PDF %s', complete_name)
        with open(complete_name, 'wb') as f:
            f.write(response.body)
