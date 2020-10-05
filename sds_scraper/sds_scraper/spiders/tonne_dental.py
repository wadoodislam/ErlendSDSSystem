import os
from datetime import datetime

import scrapy
from scrapy.spiders import CrawlSpider

from ..items import SdsScraperItem


class TonneDental(CrawlSpider):
    name = "tonne_dental"
    FILES_STORE = '/Users/junaidikhlaq/PycharmProjects/ErlendSDSSystem/sds_scraper/sds_scraper/sds_data/Tonne Dental'

    def start_requests(self):
        urls = ['https://www.tonnedental.no/datablader/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):

        for url in response.css('p a::attr(href)').getall():
            name = url.split('/')[-1].replace('_' or '-', ' ').split('.')[0]
            sds_scraper_item = SdsScraperItem()
            sds_scraper_item['file_urls'] = [url]
            sds_scraper_item['source'] = 'tonne_dental.py'
            sds_scraper_item['file_display_name'] = name
            sds_scraper_item['manufacturer'] = 'Tonne Dental'
            sds_scraper_item['crawl_date'] = datetime.now().date().strftime('%d.%m.%Y')
            if not os.path.isdir(self.FILES_STORE):
                os.mkdir(self.FILES_STORE)
            yield scrapy.Request(
                url=response.urljoin(url),
                callback=self.parse_pdf,
                meta={'item': sds_scraper_item}
            )

    def parse_pdf(self, response):
        item = response.meta.get('item', '')
        path = item['file_display_name']
        complete_name = os.path.join(self.FILES_STORE, path + ".pdf")
        self.logger.info('Saving PDF %s', complete_name)
        with open(complete_name, 'wb') as f:
            f.write(response.body)
        yield item
