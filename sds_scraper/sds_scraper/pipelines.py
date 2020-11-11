import re
from datetime import datetime
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from scrapy.http import Request
from scrapy.pipelines.files import FilesPipeline
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class FileDownloadPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None):
        return f"{info.spider.provider}/" + request.meta['item']['file_display_name']

    def get_media_requests(self, item, info):
        yield Request(url=item['file_urls'][0], meta={'item': item})


class BoilerplatePipeline:

    def process_item(self, item, spider):
        item['provider'] = spider.provider
        item['manufacturer_name'] = spider.manufacturer
        item['source'] = spider.source
        item['crawl_date'] = datetime.now().strftime('%d.%m.%Y')
        item['sds_status'] = item['files'][0]['status']
        item['sds_url'] = item['files'][0]['url']
        return item


class SDSTextExtractorPipeline:

    def process_item(self, item, spider):
        path = item['files'][0]['path']
        item['raw_pdf_text'] = self.read_pdf(settings.get('FILES_STORE') + path)
        return item

    def read_pdf(self, path):
        output_string = StringIO()
        with open(path, 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)
        return output_string.getvalue()


class SDSRelevantTextExtractorPipeline:
    Relevant_Splitter = re.compile(r'AVSNITT|SECTION|Avsnitt')

    def process_item(self, item, spider):
        splitter = getattr(spider, 'Relevant_Splitter', self.Relevant_Splitter)
        relevant_text = 'AVSNITT'.join(re.split(splitter, item['raw_pdf_text'])[:3])
        item['pdf_text'] = pdf_text = '\n'.join([line for line in relevant_text.split('\n') if line.strip()])
        item['pdf_squashed'] = ' '.join(pdf_text.split('\n'))
        return item


class SDSHazardCodeExtractorPipeline:
    HAZARD_CODE_PATTERN = re.compile(r'(?:EUH|[H|P])\s?\d\d\d\w*(?:\+(?:EUH|[H|P])*\d\d\d\w*)*')

    def process_item(self, item, spider):
        self.HAZARD_CODE_PATTERN = getattr(spider, 'HAZARD_CODE_PATTERN', self.HAZARD_CODE_PATTERN)
        raw_codes = self.__hazard_section(item)
        raw_codes = '+'.join([part.strip() for part in raw_codes.split('+')])
        item['sds_pdf_Hazards_identification'] = ','.join(sorted(set(re.findall(self.HAZARD_CODE_PATTERN, raw_codes))))
        return item

    def __hazard_section(self, item):
        return item['pdf_squashed'].split('AVSNITT' or 'SECTION' or 'Avsnitt')[2]


class SDSProductNameExtractorPipeline:
    PRODUCT_STRATEGY = {}

    def process_item(self, item, spider):
        self.PRODUCT_STRATEGY = getattr(spider, 'PRODUCT_STRATEGY')
        item['sds_pdf_product_name'] = Strategies().apply_strategy(self.PRODUCT_STRATEGY, item['pdf_text'])
        return item


class SDSManufactureExtractorPipeline:
    # MANUFACTURE_STRATEGIES = [
    #     {
    #         'activation': 'XOR',
    #         'procedures': [
    #             [
    #                 ('SUB', re.compile(r'Leverandør.*?\n|Supplier.*?\(.*\n.*\).*\n\s*'), 'COMPANY_NAME'),
    #                 ('SEARCH', re.compile(r'COMPANY_NAME(.*?)\n'), 1),
    #             ],
    #
    #         ]
    #     }
    # ]

    def process_item(self, item, spider):
        self.MANUFACTURE_STRATEGIES = getattr(spider, 'MANUFACTURE_STRATEGIES')
        raw_manfacturer = item['pdf_text']
        for strategy in self.MANUFACTURE_STRATEGIES:
            raw_manfacturer = Strategies().apply_strategy(strategy, raw_manfacturer)
        item['sds_pdf_manufacture_name'] = raw_manfacturer
        return item


class SDSPrintDateExtractorPipeline:
    # DATE_REPLACE = False
    # DATE_FORMATS = r'\d\d-\d\d-\d\d\d\d|\d\d\d\d-\d\d-\d\d|\d?\d\.\d?\d\.\d?\d?\d\d|\d\d\/\d\d\/\d\d\d\d|\d?\d [a-zA-Z]{3} \d?\d?\d\d'
    # DATE_PATTERN = re.compile(DATE_FORMATS)
    # PRINT_STRATEGY = [
    #     {
    #         'activation': 'XOR',
    #         'procedures': [
    #             [
    #                 ('FINDALL', re.compile(rf'Utskriftsdato.*?({DATE_FORMATS})'), ' '),
    #             ],
    #             [
    #                 ('FINDALL', re.compile(rf'Print\sdate.*?({DATE_FORMATS})'), ' '),
    #             ],
    #         ]
    #     }
    # ]

    def process_item(self, item, spider):
        self.PRINT_STRATEGY = getattr(spider, 'PRINT_STRATEGY')
        self.DATE_PATTERN = getattr(spider, 'DATE_PATTERN')
        self.DATE_REPLACE = getattr(spider, 'DATE_REPLACE')
        item['sds_pdf_print_date'] = Strategies().date_extractor(self.PRINT_STRATEGY, item, self.DATE_PATTERN,
                                                                 self.DATE_REPLACE)
        return item


class SDSRevisionDateExtractorPipeline:
    # DATE_REPLACE = False
    # DATE_FORMATS = r'\d\d-\d\d-\d\d\d\d|\d\d\d\d-\d\d-\d\d|\d?\d\.\d?\d\.\d?\d?\d\d|\d\d\/\d\d\/\d\d\d\d|\d?\d [a-zA-Z]{3} \d?\d?\d\d'
    # DATE_PATTERN = re.compile(DATE_FORMATS)
    # REVISION_STRATEGY = [
    #     {
    #         'activation': 'XOR',
    #         'procedures': [
    #             [
    #                 ('FINDALL', re.compile(rf'Redigert :.*?({DATE_FORMATS})'), ' '),
    #             ],
    #             [
    #                 ('FINDALL', re.compile(rf'Revision :.*?({DATE_FORMATS})'), ' '),
    #             ]
    #         ]
    #     }
    # ]

    def process_item(self, item, spider):
        self.REVISION_STRATEGY = getattr(spider, 'REVISION_STRATEGY')
        self.DATE_PATTERN = getattr(spider, 'DATE_PATTERN')
        self.DATE_REPLACE = getattr(spider, 'DATE_REPLACE')
        item['sds_pdf_revision_date'] = Strategies().date_extractor(self.REVISION_STRATEGY, item, self.DATE_PATTERN,
                                                                    self.DATE_REPLACE)
        return item


class SDSExtractorPipeline:

    def process_item(self, item, spider):
        # print('path: ', item['files'][0]['path'])
        # print('product_name: ', item['sds_pdf_product_name'])
        # print('hazard_codes: ', item['sds_pdf_Hazards_identification'])
        # print('manufacturer: ', item['sds_pdf_manufacture_name'])
        # print('print_date: ', item['sds_pdf_print_date'])
        # print('revision_date: ', item['sds_pdf_revision_date'])
        item.pop('pdf_text')
        item.pop('raw_pdf_text')
        item.pop('pdf_squashed')
        item.pop('files')
        return item


class SDSDatabasePipeline:

    def process_item(self, item, spider):
        settings.get('SERVER_ADDRESS')+'/'

class Strategies:
    FIND_MAX_LENGHT = 50

    def date_extractor(self, date_strategies, item, date_pattern, date_replace):
        raw_dates = item['pdf_squashed']
        for strategy in date_strategies:
            raw_dates = self.apply_strategy(strategy, raw_dates)
        raw_dates = re.findall(date_pattern, raw_dates)
        date = set(self._date_formatter(date) for date in raw_dates)
        date = date.pop() if date else ''
        if date_replace:
            item['pdf_squashed'] = item['pdf_squashed'].replace(date, '')
        return date

    def _date_formatter(self, date_str):
        if '/' in date_str:
            return datetime.strptime(date_str, '%d/%m/%Y').strftime('%d.%m.%Y')
        elif '-' in date_str:
            try:
                return datetime.strptime(date_str, '%Y-%m-%d').strftime('%d.%m.%Y')
            except:
                return datetime.strptime(date_str, '%d-%m-%Y').strftime('%d.%m.%Y')
        elif '.' in date_str:
            if re.match(r'\d?\d\.\d?\d\.\d\d\d\d', date_str):
                return datetime.strptime(date_str, '%d.%m.%Y').strftime('%d.%m.%Y')
            elif re.match(r'\d?\d\.\d?\d\.\d\d', date_str):
                return datetime.strptime(date_str, '%d.%m.%y').strftime('%d.%m.%Y')
        elif re.match(r'\d?\d [a-zA-Z]{3} \d\d\d\d', date_str):
            return datetime.strptime(date_str, '%d %b %Y').strftime('%d.%m.%Y')

    def apply_strategy(self, strategy, raw_text):
        activation = strategy['activation']
        if activation == 'XOR':
            for procedure in strategy['procedures']:
                procedure_result = raw_text
                for step in procedure:
                    procedure_result = self._apply_step(step, procedure_result)
                result = procedure_result.strip()
                if result:
                    return result
            return result

    def _apply_step(self, step, raw_text):
        func = step[0]
        if func == 'SUB':
            return re.sub(step[1], step[2], raw_text)
        elif func == 'SEARCH':
            result = re.search(step[1], raw_text)
            return result.group(step[2]) if result else ''
        elif func == 'FINDALL':
            results = re.findall(step[1], raw_text)
            results = step[2].join([result for result in results if len(result) < self.FIND_MAX_LENGHT])
            return results if results else ''
        elif func == 'SPLIT':
            results = re.split(step[1], raw_text)[step[2]]
            return results if results else ''
