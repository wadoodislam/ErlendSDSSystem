# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re
from datetime import datetime
# useful for handling different item types with a single interface
from io import StringIO

import PyPDF2
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from scrapy.http import Request
from scrapy.pipelines.files import FilesPipeline

from .config import Configuration


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


class SDSExtractorPipeline:
    DATE_REPLACE = False
    config = Configuration()
    FIND_MAX_LENGHT = 50
    Relevant_Splitter = re.compile(r'AVSNITT|SECTION')
    HAZARD_CODE_PATTERN = re.compile(r'(?:EUH|[H|P])\s?\d\d\d\w*(?:\+(?:EUH|[H|P])*\d\d\d\w*)*')
    DATE_FORMATS = r'\d\d-\d\d-\d\d\d\d|\d\d\d\d-\d\d-\d\d|\d?\d\.\d?\d\.\d?\d?\d\d|\d\d\/\d\d\/\d\d\d\d|\d?\d [a-zA-Z]{3} \d?\d?\d\d'
    DATE_PATTERN = re.compile(DATE_FORMATS)

    PRODUCT_STRATEGY = {
        'activation': 'XOR',
        'procedures': [
            [
                ('SUB', re.compile(r'Trade name\s*:.*?\n|Handelsnavn.*?\n'), 'PRODUCT_NAME'),
                ('SUB', re.compile(r'Revision\s*:.*?\n|Redigert.*?\n'), ''),
                ('SUB', re.compile(r'Revision date\s*:.*?\n|Redigeringsdato.*?\n'), ''),
                ('SUB', re.compile(r'Print date\s*:.*?\n|Utskriftsdato.*?\n'), ''),
                ('SEARCH', re.compile(r'PRODUCT_NAME\n?\s*(.*?)\n'), 1),
            ]
        ]
    }
    MANUFACTURE_STRATEGIES = [
        {
            'activation': 'XOR',
            'procedures': [
                [
                    ('SUB', re.compile(r'Leverandør.*?\n|Supplier.*?\(.*\n.*\).*\n\s*'), 'COMPANY_NAME'),
                    ('SEARCH', re.compile(r'COMPANY_NAME(.*?)\n'), 1),
                ],

            ]
        }
    ]
    REVISION_STRATEGY = [
        {
            'activation': 'XOR',
            'procedures': [
                [
                    ('FINDALL', re.compile(rf'Redigert :.*?({DATE_FORMATS})'), ' '),
                ]
            ]
        }
    ]
    PRINT_STRATEGY = [
        {
            'activation': 'XOR',
            'procedures': [
                [
                    ('FINDALL', re.compile(rf'Utskriftsdato.*?(?:{DATE_FORMATS})'), ' '),
                ],
            ]
        }
    ]

    def process_item(self, item, spider):
        path = item['files'][0]['path']
        item['raw_pdf_text'] = self.read_pdf(self.config.DATA_DIR + path)
        self.relevent_text(item, spider)
        self.process_data(item)
        return item

    def process_data(self, item):
        pdf_text = item['pdf_text']
        raw_dates = item['pdf_squashed']
        product_name = self.product_name(item)
        manufacturer = self.manufacture_name(item)
        hazard_codes = self.hazard_code(item)
        revision_date = self.revision_date(item)
        print_date = self.print_date(item)
        print('path', item['files'][0]['path'])
        print('product_name', product_name)
        print('hazard_codes', hazard_codes)
        print('manufacturer', manufacturer)
        print('revision_date', revision_date)
        print('print_date', print_date)
        pass

    def product_name(self, item):
        return self._apply_strategy(self.PRODUCT_STRATEGY, item['pdf_text'])

    def manufacture_name(self, item):
        raw_manfacturer = item['pdf_text']
        for strategy in self.MANUFACTURE_STRATEGIES:
            raw_manfacturer = self._apply_strategy(strategy, raw_manfacturer)
        return raw_manfacturer

    def hazard_code(self, item):
        raw_codes = self.hazard_section(item)
        raw_codes = '+'.join([part.strip() for part in raw_codes.split('+')])
        return ','.join(sorted(set(re.findall(self.HAZARD_CODE_PATTERN, raw_codes))))

    def hazard_section(self, item):
        return item['pdf_squashed'].split('AVSNITT' or 'SECTION')[2]

    def revision_date(self, item):
        return self._date_extractor(self.REVISION_STRATEGY, item)

    def print_date(self, item):
        return self._date_extractor(self.PRINT_STRATEGY, item)

    def replace_date(self, item):
        pass

    def _date_extractor(self, date_strategies, item):
        raw_dates = item['pdf_squashed']
        for strategy in date_strategies:
            raw_dates = self._apply_strategy(strategy, raw_dates)
        raw_dates = re.findall(self.DATE_PATTERN, raw_dates)
        date = set(self._date_formatter(date) for date in raw_dates)
        date = date.pop() if date else ''
        if self.DATE_REPLACE:
            item['pdf_squashed'] = item['pdf_squashed'].replace(date, '')
        return date

    def _date_formatter(self, date_str):
        # for date_format in self.DATE_FORMATS.split('|'):
        #     if re.match(date_format, date_str):
        #
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

    def relevent_text(self, item, spider):
        splitter = self.Relevant_Splitter
        relevant_text = 'AVSNITT'.join(re.split(splitter, item['raw_pdf_text'])[:3])
        item['pdf_text'] = pdf_text = '\n'.join([line for line in relevant_text.split('\n') if line.strip()])
        item['pdf_squashed'] = ' '.join(pdf_text.split('\n'))

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

    # def read_pdf2(self, path):
    #     output_string = ''
    #     with open(path, 'rb') as pdfFileObj:
    #         pdf_reader = PyPDF2.PdfFileReader(pdfFileObj)
    #         for page in pdf_reader.pages:
    #             output_string += page.extractText()
    #     return output_string

    def _apply_strategy(self, strategy, raw_text):
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
        # elif activation == 'AND':
        #     procedure_result = raw_text
        #     for procedure in strategy['procedures']:
        #         for step in procedure:
        #             procedure_result = self._apply_step(step, procedure_result)
        #     return procedure_result

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
