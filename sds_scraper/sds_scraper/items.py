# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SdsScraperItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
    source = scrapy.Field()
    manufacturer_name = scrapy.Field()
    file_display_name = scrapy.Field()
    languages = scrapy.Field()
    date = scrapy.Field()
    document_type = scrapy.Field()
    file_type = scrapy.Field()
    crawl_date = scrapy.Field()
    provider = scrapy.Field()

    sds_pdf_Hazards_identification = scrapy.Field()
    sds_pdf_product_name = scrapy.Field()
    sds_pdf_manufacture_name = scrapy.Field()
    sds_pdf_print_date = scrapy.Field()
    sds_pdf_revision_date = scrapy.Field()
    sds_status = scrapy.Field()
    sds_url = scrapy.Field()

    raw_pdf_text = scrapy.Field()
    pdf_squashed = scrapy.Field()
    pdf_text = scrapy.Field()
