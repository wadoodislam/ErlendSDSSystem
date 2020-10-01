import scrapy
from scrapy.spiders import CrawlSpider
from datetime import datetime


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
        title = response.xpath('//div[contains(@data-langcode, "norwegian")]/span[contains(@class, "dl-item-title")]/text()').extract()
        url = response.xpath('//div[contains(@data-langcode, "norwegian")]/a/@href').extract()
        for t, u in zip(title, url):
            yield {
                'title': t.strip().replace('\r', '').replace('\n','').split('/', 1)[0],
                'url': url,
                'crawl_date': datetime.now().date().strftime('%d.%m.%Y')
            }
