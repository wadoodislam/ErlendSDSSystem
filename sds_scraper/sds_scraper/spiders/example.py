from scrapy.spiders import CrawlSpider


class ExampleSpider(CrawlSpider):
    name = 'example'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    def parse(self, response):
        pass
