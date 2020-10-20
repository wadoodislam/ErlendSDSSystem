# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime

from scrapy.http import Request
from scrapy.pipelines.files import FilesPipeline


class BoilerplatePipeline:

    def process_item(self, item, spider):
        item['provider'] = spider.provider
        item['manufacturer'] = spider.manufacturer
        item['source'] = spider.source
        item['crawl_date'] = datetime.now().strftime('%d.%m.%Y')
        return item


class FileDownloadPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        return f"{info.spider.provider}/" + request.meta['item']['file_display_name']

    def get_media_requests(self, item, info):
        yield Request(url=item['file_urls'][0], meta={'item': item})

# class PDFReaderPipeline:
#
#     def process_item(self, item, spider):
#         spitter = getattr(spider, 'relevant_splitter', None) or
#         file = item['files'][0]
#         item['raw_pdf_text'] = self.read_pdf(file)
