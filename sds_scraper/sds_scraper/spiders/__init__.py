# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from scrapy.spiders import CrawlSpider, Spider


class SDSBaseParseSpider(Spider):
    pass


class SDSBaseCrawlSpider(CrawlSpider):

    def __init__(self, run_id=None, *args, **kwargs):
        super(SDSBaseCrawlSpider, self).__init__(*args, **kwargs)
        self.run_id = run_id
