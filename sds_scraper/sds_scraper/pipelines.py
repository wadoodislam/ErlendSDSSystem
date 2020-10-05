# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exceptions import NotConfigured
from scrapy.http import Request
from scrapy.pipelines.files import FilesPipeline


class FileDownloadPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        # original_path = super(FileDownloadPipeline, self).file_path(request, response=None, info=None)
        # sha1_and_extension = original_path.split('/')[1]  # delete 'full/' from the path
        return request.meta.get('manufacturer', '') + "/" + request.meta.get('filename', '').strip() + ".pdf"

    def get_media_requests(self, item, info):
        file_url = item['file_urls'][0]
        meta = {'filename': item['file_display_name'], 'manufacturer': item['manufacturer']}
        yield Request(url=file_url, meta=meta)
