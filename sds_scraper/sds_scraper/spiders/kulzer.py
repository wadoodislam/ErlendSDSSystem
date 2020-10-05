from datetime import datetime

import scrapy
from scrapy.spiders import CrawlSpider

from ..items import SdsScraperItem


class KulzerScraperSpider(CrawlSpider):
    name = 'kulzer_scraper'

    def start_requests(self):
        url = 'https://www.kulzer.com/en/int/downloads_5/downloads.aspx'
        data = {
            'AjaxAction': 'GetDownloads',
            'types': '143552',
            'brands': '',
            'products': '',
            'text': ''
        }

        yield scrapy.FormRequest(url=url, callback=self.parse_item, formdata=data)

    def parse_item(self, response):
        title = response.xpath(
            '//div[contains(@data-langcode, "norwegian")]/span[contains(@class, "dl-item-title")]/text()').extract()
        url = response.xpath('//div[contains(@data-langcode, "norwegian")]/a/@href').extract()
        for t, u in zip(title, url):
            sds_scraper_item = SdsScraperItem()
            sds_scraper_item['file_urls'] = [u]
            sds_scraper_item['source'] = 'kulzer.py'
            sds_scraper_item['file_display_name'] = t.strip().replace('\r', '').replace('\n', '').split('/', 1)[0]
            sds_scraper_item['manufacturer'] = 'Kulzer'
            sds_scraper_item['crawl_date'] = datetime.now().date().strftime('%d.%m.%Y')

            yield scrapy.Request(
                url=response.urljoin(u),
                callback=self.parse_pdf,
                meta={'item': sds_scraper_item}
            )

    def parse_pdf(self, response):
        item = response.meta.get('item', '')
        yield item
