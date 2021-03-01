import json
import os
import re

import scrapy
from scrapy import Selector

from . import SDSBaseCrawlSpider
from ..items import SdsScraperItem


class Mixin:
    provider = 'durr_dental'
    manufacturer = 'DÜRR DENTAL SE'
    language = 'nb'
    source = os.path.basename(__file__)
    start_urls = ['https://www.duerrdental.com/fileadmin/assets/apps/dlc/DlcProxy.php']
    base_url = 'https://www.duerrdental.com/en/services/download-centre/'

    DATE_REPLACE = False
    DATE_FORMATS = r'\d\d-\d\d-\d\d\d\d|\d\d\d\d-\d\d-\d\d|\d?\d\.\d?\d\.\d?\d?\d\d|\d\d\/\d\d\/\d\d\d\d|\d?\d [a-zA-Z]{3} \d?\d?\d\d'
    DATE_PATTERN = re.compile(DATE_FORMATS)

    PRODUCT_STRATEGY = {
        'activation': 'XOR',
        'procedures': [
            [
                ('SUB', re.compile(r'Trade name\s*:.*?\n|Handelsnavn.*?\n'), 'PRODUCT_NAME'),
                ('SUB', re.compile(r'Revision\s*:.*?\n|Redigert.*?\n'), ''),
                ('SUB', re.compile(r'Revision date\s*:.*?\n|Redigeringsdato.*?\n'), ''),
                ('SUB', re.compile(r'Print date\s*:.*?\n|Utskriftsdato.*?\n'), ''),
                ('SEARCH', re.compile(r'PRODUCT_NAME\n?\s*(.*?)\n'), 1),
            ]

        ]
    }

    MANUFACTURE_STRATEGIES = [
        {
            'activation': 'XOR',
            'procedures': [
                [
                    ('SUB', re.compile(r'Leverandør.*?\n|Supplier.*?\(.*\n.*\).*\n\s*'), 'COMPANY_NAME'),
                    ('SEARCH', re.compile(r'COMPANY_NAME(.*?)\n'), 1),
                ],

            ]
        }
    ]

    PRINT_STRATEGY = [
        {
            'activation': 'XOR',
            'procedures': [
                [
                    ('FINDALL', re.compile(rf'Utskriftsdato.*?({DATE_FORMATS})'), ' '),
                ],
                [
                    ('FINDALL', re.compile(rf'Print\sdate.*?({DATE_FORMATS})'), ' '),
                ],
            ]
        }
    ]

    REVISION_STRATEGY = [
        {
            'activation': 'XOR',
            'procedures': [
                [
                    ('FINDALL', re.compile(rf'Redigert :.*?({DATE_FORMATS})'), ' '),
                ],
                [
                    ('FINDALL', re.compile(rf'Revision :.*?({DATE_FORMATS})'), ' '),
                ]
            ]
        }
    ]


class DurDentalCrawlSpider(Mixin, SDSBaseCrawlSpider):
    name = Mixin.provider + '_crawl'

    def start_requests(self):
        headers = {
            "Connection": "keep-alive",
            "Accept": "text/html, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Mobile Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://www.duerrdental.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://www.duerrdental.com/en/services/download-centre/",
            "Accept-Language": "en-US,en;q=0.9"
        }
        cookies = {
            "cookie_optin": "essential:1|statistics:0|iframes:0"
        }
        body = 'dlc_url=https%3A%2F%2Fdlc.duerrdental.com%2Fajax_search.php&curr_lang=en&lang_codes=&action=document_type&curr_view=tile&pagination_step=all&direct_param_pagination_step=-1&curr_page=1&text_search=&is_mobile=true&business_unit=&product_family=&product=&document_type=Safety%2520data%2520sheet&sorting=download_count&sort_order=desc'
        yield scrapy.Request(
            url=self.start_urls[0],
            method='POST',
            dont_filter=True,
            cookies=cookies,
            headers=headers,
            body=body,
            callback=self.parse
        )

    def parse(self, response):
        content = json.loads(response.text)['content']
        for tile in Selector(text=content).css('div.tile'):
            if tile.css('h3.file_name a::text').get() is None:
                break
            lang_list = dict(zip(tile.css('div.languages select option::text').getall(),
                                 tile.css('div.languages select option::attr(value)').getall()))
            sds_scraper_item = SdsScraperItem()
            sds_scraper_item['name'] = (tile.css('h3.file_name a::text').get()).replace(os.sep,
                                                                                        '-') + '.pdf'
            sds_scraper_item['languages'] = lang_list
            if 'NO' in lang_list:
                sds_scraper_item['file_urls'] = [lang_list['NO']]
            else:
                sds_scraper_item['file_urls'] = [tile.css('h3.file_name a::attr(href)').get()]
            sds_scraper_item['date'] = '-'.join(reversed(tile.css('div.date::text').re(r' (\d\d?.\d\d?.\d\d?\d\d?)', 1)[0]))
            sds_scraper_item['document_type'] = tile.css('div.document_type::text').get()
            sds_scraper_item['url'] = self.base_url
            sds_scraper_item['file_type'] = tile.css('div.file_info span::text').get()
            yield sds_scraper_item
