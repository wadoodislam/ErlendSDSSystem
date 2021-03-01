import os
import re

from scrapy import FormRequest

from . import SDSBaseParseSpider, SDSBaseCrawlSpider
from ..items import SdsScraperItem


class Mixin:
    provider = 'ultradent'
    manufacturer = 'Ultradent Products, Inc'
    language = 'nb'
    source = os.path.basename(__file__)
    start_urls = ['https://www.ultradent.com/resources/safety-data-sheets']

    Relevant_Splitter = re.compile(r'\n\d\s[A-Z]|KAPITTEL')

    DATE_REPLACE = False
    DATE_FORMATS = r'\d\d-\d\d-\d\d\d\d|\d\d\d\d-\d\d-\d\d|\d?\d\.\d?\d\.\d?\d?\d\d|\d\d?\/\d\d?\/\d\d?\d\d?|\d?\d [a-zA-Z]{3} \d?\d?\d\d'
    DATE_PATTERN = re.compile(DATE_FORMATS)

    PRODUCT_STRATEGY = {
        'activation': 'XOR',
        'procedures': [
            [
                ('SUB', re.compile(r'Produktnavn.*?\nProduktbeskrivelse.*?\n:.*?\n'), 'PRODUCT_NAME'),
                # ('SUB', re.compile(r'Produktbeskrivelse.*?\n'), ''),
                # ('SUB', re.compile(r':.*?\n'), ''),
                ('SEARCH', re.compile(r'PRODUCT_NAME: \n?(.*?)\n'), 1),
            ],
            [
                ('SEARCH', re.compile(r'Handelsnavn: \n?\s*(.*?)\n'), 1),
            ],

        ]
    }

    MANUFACTURE_STRATEGIES = [
        {
            'activation': 'XOR',
            'procedures': [
                [
                    ('SUB', re.compile(r'Produsent.*?\n'), 'COMPANY_NAME'),
                    ('SEARCH', re.compile(r'COMPANY_NAME\n?(.*?)\n'), 1),
                ],
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
                ],
            ]
        }
    ]

    REVISION_STRATEGY = [
        {
            'activation': 'XOR',
            'procedures': [
                [
                    ('FINDALL', re.compile(rf'revidert.*?({DATE_FORMATS})'), ' '),
                ], [
                    ('FINDALL', re.compile(rf'Revidert.*?({DATE_FORMATS})'), ' '),
                ],[
                    ('FINDALL', re.compile(rf'Revisjonsdato.*?({DATE_FORMATS})'), ' '),
                ],
            ]
        }
    ]


class UltradentParseSpider(SDSBaseParseSpider):
    name = Mixin.provider + '_parse'


class UltradentCrawlSpider(Mixin, SDSBaseCrawlSpider):
    name = Mixin.provider + '_crawl'

    def start_requests(self):
        self.logger.info(f"run_id: {self.run_id}")
        return [FormRequest(url=self.start_urls[0], formdata={'Language': 'Norwegian'}, callback=self.parse)]

    def parse(self, response, **kwargs):
        for pdf_css in response.css('.linkList li'):
            item = SdsScraperItem()
            item['file_urls'] = [response.urljoin(pdf_css.css('::attr(href)').get())]
            item['name'] = pdf_css.css('a::text').get() + '.pdf'
            yield item
