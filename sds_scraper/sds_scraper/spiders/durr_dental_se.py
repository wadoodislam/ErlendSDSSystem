import json

import scrapy
from scrapy import Selector
from scrapy.spiders import CrawlSpider
from datetime import datetime


class DurDentalSpider(CrawlSpider):
    name = 'dur_dental'

    def start_requests(self):
        url = 'https://www.duerrdental.com/fileadmin/assets/apps/dlc/DlcProxy.php'

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
            url=url,
            method='POST',
            dont_filter=True,
            cookies=cookies,
            headers=headers,
            body=body,
            callback=self.parse
        )

    def parse(self, response):
        content = json.loads(response.text)['content']
        for tile in Selector(text=content).css('div.tile').getall():
            file_display_name = Selector(text=tile).xpath('//*[@class="file_name"]/a/text()').get()
            lang_list = dict(zip(Selector(text=tile).css('div.languages select option').xpath('text()').getall(),
                                 Selector(text=tile).css('div.languages select option::attr(value)').getall()))
            date = Selector(text=tile).css('div.date::text').re(r'\d\d?.\d\d?.\d\d?\d\d?')[0]
            document_type = Selector(text=tile).css('div.document_type::text').get()
            file_type = Selector(text=tile).css('div.file_info span::text').get()
            url = Selector(text=tile).css('h3.file_name a::attr(href)').get()

            yield {
                'source': 'durr_dental_se.py',
                'manufacturer': 'DÜRR DENTAL SE',
                'file_display_name': file_display_name,
                'url': url,
                'languages': lang_list,
                'date': date,
                'document_type': document_type,
                'file_type': file_type,
                'crawl_date': datetime.now().date().strftime('%d.%m.%Y')
            }
