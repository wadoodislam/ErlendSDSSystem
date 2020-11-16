import os
import re

from scrapy import FormRequest

from . import SDSBaseParseSpider, SDSBaseCrawlSpider
from ..items import SdsScraperItem


class Mixin:
    provider = 'ultradent'
    manufacturer = 'Ultradent Products, Inc'
    source = os.path.basename(__file__)
    start_urls = ['https://www.ultradent.com/resources/safety-data-sheets']

    Relevant_Splitter = re.compile(r'\n\d\s[A-Z]')

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
            item['name'] = pdf_css.css('a::text').get() + '.pdf'
            yield item
