import os

from scrapy import Selector, Request

from . import SDSBaseCrawlSpider
from ..items import SdsScraperItem


class Mixin:
    provider = 'adda'
    manufacturer = 'Adda Byggkjemi A/S'
    source = os.path.basename(__file__)
    start_urls = ['https://www.adda.no/produkter/produktregister/']


class AddaCrawlSpider(Mixin, SDSBaseCrawlSpider):
    name = Mixin.provider + '_crawl'

    custom_settings = {
        'COOKIES_ENABLED': True,
    }

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        'sec-ch-ua-mobile': '?0',
        'Referer': 'https://www.adda.no/',
        'Accept-Language': 'en-US,en;q=0.9',
        # 'Cookie': 'AspxAutoDetectCookieSupport=1; ASP.NET_SessionId=apm0v24iepsltydsi5ronmzu; AspxAutoDetectCookieSupport=1; ASP.NET_SessionId=s1fchdspk55wisse2sh3ympy'
    }

    def start_requests(self):
        return [Request(self.start_urls[0], headers=self.headers)]

    def parse_start_url(self, response, **kwargs):
        name = ''
        for rows in response.css('tbody tr').getall():
            item = SdsScraperItem()
            for columns in Selector(text=rows).css('td').getall():
                if Selector(text=columns).css('a'):
                    if 'produkt=' in Selector(text=columns).css('a::attr(href)').get():
                        name = Selector(text=columns).css('a::text').get() + '.pdf'
                    if Selector(text=columns).css('a.download::text').get() == 'Sikkerhetsdatablad':
                        URL = Selector(text=columns).css('a.download::attr(href)').get()
                        item['file_urls'] = [URL.replace('safeuse.essenticon.com', 'app.safeuse.no')]
                        item['name'] = name
                        yield item
