import scrapy
from scrapy.spiders import CrawlSpider
from ..items import KulzerScraperItem


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
        item = KulzerScraperItem()
        title = response.xpath('//div[contains(@data-langcode, "norwegian")]/span[contains(@class, "dl-item-title")]/text()').extract()
        url = response.xpath('//div[contains(@data-langcode, "norwegian")]/a/@href').extract()
        for t, u in zip(title, url):
            item['name'] = t.strip().replace('\r', '').replace('\n','').split('/', 1)[0]
            item['file_urls'] = u.split()
            yield item
