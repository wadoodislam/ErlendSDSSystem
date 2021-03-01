import os
import re

from scrapy import Selector

from . import SDSBaseCrawlSpider
from ..items import SdsScraperItem


class Mixin:
    provider = 'ivoclar_vivadent'
    manufacturer = 'Ivoclar Vivadent AG'
    language = 'nb'
    source = os.path.basename(__file__)
    start_urls = ['https://www.ivoclarvivadent.se/sv/skerhetsdatablad/']

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


class IvoclarVivadentCrawlSpider(Mixin, SDSBaseCrawlSpider):
    name = Mixin.provider + '_crawl'

    def parse_start_url(self, response, **kwargs):
        for items in response.css('div.text').getall():
            name = Selector(text=items).css('a::text').re(r'.*_NO')
            url = Selector(text=items).css('a::attr(href)').re(r'.*_NO')
            if name and url:
                sds_scraper_item = SdsScraperItem()
                sds_scraper_item['name'] = name[0] + '.pdf'
                sds_scraper_item['file_urls'] = [response.urljoin(url[0])]
                yield sds_scraper_item
