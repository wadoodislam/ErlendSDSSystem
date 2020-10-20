import os

from scrapy import FormRequest

from . import SDSBaseCrawlSpider
from ..items import SdsScraperItem


class Mixin:
    provider = 'kulzer'
    manufacturer = 'Kulzer'
    source = os.path.basename(__file__)
    start_urls = ['https://www.kulzer.com/en/int/downloads_5/downloads.aspx']


class KulzerCrawlSpider(Mixin, SDSBaseCrawlSpider):
    name = Mixin.provider + '_crawl'

    def start_requests(self):
        yield FormRequest(url=self.start_urls[0], callback=self.parse,
                          formdata={'AjaxAction': 'GetDownloads', 'types': '143552', 'brands': '', 'products': '',
                                    'text': ''})

    def parse(self, response):
        title = response.xpath(
            '//div[contains(@data-langcode, "norwegian")]/span[contains(@class, "dl-item-title")]/text()').extract()
        url = response.xpath('//div[contains(@data-langcode, "norwegian")]/a/@href').extract()
        for t, u in zip(title, url):
            sds_scraper_item = SdsScraperItem()
            sds_scraper_item['file_urls'] = [u]
            sds_scraper_item['file_display_name'] = (t.strip().replace('\r', '').replace('\n', '').split('/', 1)[0]).strip() + '.pdf'
            yield sds_scraper_item
