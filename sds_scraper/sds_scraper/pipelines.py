# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import requests


class KulzerScraperPipeline:

    def process_item(self, item, spider):
        requests.post(url="http://127.0.0.1:8000/api/sds/",
                      files={'file': open("H:/PyCharm Projects/ErlendExtra/downloads/"+item['files'][0]['path'], 'rb')},
                      data={'name': item['name'], 'url': item['file_urls']})
        return item
