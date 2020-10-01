from datetime import datetime

import scrapy
from scrapy.spiders import CrawlSpider


class TonneDental(CrawlSpider):
    name = "tonne_dental"

    def start_requests(self):
        url = 'https://www.tonnedental.no/datablader/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # items = response.css('p').re(r'</strong>?<br>\n?(.*)\n?<a|<br>\n?</strong>?\n?(.*)\n?<a', 1)
        for url in response.css('p a::attr(href)').getall():
            yield {
                'source': 'tonne_dental.py',
                'manufacturer': 'W&H Nordic AB',
                'url': url,
                'crawl_date': datetime.now().date().strftime('%d.%m.%Y')
            }
        pass
