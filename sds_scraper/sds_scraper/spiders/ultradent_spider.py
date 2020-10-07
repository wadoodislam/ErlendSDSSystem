import os

from scrapy import FormRequest

from . import SDSBaseParseSpider, SDSBaseCrawlSpider
from ..items import SdsScraperItem


class Mixin:
    provider = 'ultradent'
    manufacturer = 'Ultradent Products, Inc'
    source = os.path.basename(__file__)
    start_urls = ['https://www.ultradent.com/resources/safety-data-sheets']


class UltradentParseSpider(SDSBaseParseSpider):
    name = Mixin.provider + '_parse'


class UltradentCrawlSpider(Mixin, SDSBaseCrawlSpider):
    name = Mixin.provider + '_crawl'

    def start_requests(self):
        return [FormRequest(url=self.start_urls[0], formdata={'Language': 'Norwegian'}, callback=self.parse)]

    def parse(self, response, **kwargs):
        for pdf_css in response.css('.linkList li'):
            item = SdsScraperItem()
            item['file_urls'] = [response.urljoin(pdf_css.css('::attr(href)').get())]
            item['file_display_name'] = pdf_css.css('a::text').get() + '.pdf'
            yield item
