import os
import re

from scrapy import FormRequest

from . import SDSBaseCrawlSpider
from ..items import SdsScraperItem


class Mixin:
    provider = 'kulzer'
    manufacturer = 'Kulzer'
    language = 'nb'
    source = os.path.basename(__file__)
    start_urls = ['https://www.kulzer.com/en/int/downloads_5/downloads.aspx']

    DATE_REPLACE = False
    DATE_FORMATS = r'\d?\d\.\d?\d\.\d?\d?\d\d'
    DATE_PATTERN = re.compile(DATE_FORMATS)

    PRODUCT_STRATEGY = {
        'activation': 'XOR',
        'procedures': [
            [
                ('SEARCH', re.compile(r'Handelsnavn: \n?\s*(.*?)\n'), 1),
            ]
        ]
    }

    MANUFACTURE_STRATEGIES = [
        {
            'activation': 'XOR',
            'procedures': [
                [
                    ('SUB', re.compile(r'Produsent\/leverandør.*?\n'), 'COMPANY_NAME'),
                    ('SEARCH', re.compile(r'COMPANY_NAME\n?(.*?)\n'), 1),
                ],

            ]
        }
    ]

    PRINT_STRATEGY = [
        {
            'activation': 'XOR',
            'procedures': [
                [
                    ('FINDALL', re.compile(rf'Trykkdato.*?({DATE_FORMATS})'), ' '),
                ]
            ]
        }
    ]

    REVISION_STRATEGY = [
        {
            'activation': 'XOR',
            'procedures': [
                [
                    ('FINDALL', re.compile(rf'revidert.*?({DATE_FORMATS})'), ' '),
                ]
            ]
        }
    ]


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
            sds_scraper_item['name'] = (t.strip().replace('\r', '').replace('\n', '').split('/', 1)[0]).strip() + '.pdf'
            yield sds_scraper_item
