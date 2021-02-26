import csv
import hashlib
import os
from datetime import datetime, timezone
from tqdm import tqdm
from django.conf import settings
from django.core.management import BaseCommand
from pyunpack import Archive

from core.models import *


class Helper:
    SDS_PATH = f'media/sds'

    def hash(self, name, provider):
        hashed = name + '-' + provider
        return hashlib.md5(hashed.encode()).hexdigest()

    def make_products(self, csv_file_path, harvest, is_primary=True):
        langs = []
        harvests = []
        manufacturers = []
        product_set = set()
        pdfs = []
        products = []
        with open(csv_file_path) as csv_file:
            csv_reader = list(csv.DictReader(csv_file))
            for row in tqdm(csv_reader, total=len(csv_reader)):
                harvest_obj, _ = SDSHarvestSource.objects.update_or_create(
                    id=harvest.lower(),
                    defaults={
                        'name': harvest,
                        'primary': is_primary,
                    }
                )
                harvests.append(harvest_obj)
                lang, _ = Language.objects.get_or_create(name=row['sds_language'])
                if _:
                    langs.append(lang)
                manufacturer, _ = Manufacturer.objects.get_or_create(name=row['sds_pdf_manufacture_name'])
                if _:
                    manufacturers.append(manufacturer)

                phash = self.hash(row['sds_pdf_product_name'], harvest_obj.id)
                pdf, _ = SDS_PDF.objects.update_or_create(
                    pdf_md5=phash,
                    defaults={
                        'name': os.path.split(row['sds_pdf_filename_in_zip'])[1],
                        'sds_harvest_source': harvest_obj,
                        'from_primary': is_primary,
                        'language': lang,
                        'manufacturer': manufacturer,
                        'sds_link': row['product_url'],
                        'sds_download_url': f"{settings.MACHINE_URL}:8080/media/sds/{harvest}{row['sds_pdf_filename_in_zip']}".replace(' ', '%20'),
                        'sds_product_name': row['sds_pdf_product_name'],
                        'sds_hazards_codes': row['sds_pdf_Hazards_identification'],
                        'sds_published_date': datetime.strptime(row['sds_pdf_published_date'],
                                                                '%d.%m.%Y').replace(tzinfo=timezone.utc),
                        'sds_revision_date': datetime.strptime(row['sds_pdf_revision_date'],
                                                               '%d.%m.%Y').replace(tzinfo=timezone.utc)
                    }
                )
                if _ and phash not in product_set:
                    pdfs.append(pdf)
                    product_set.add(phash)

                product, _ = Product.objects.get_or_create(
                        name=row['sds_pdf_product_name'],
                        language=lang,
                        sds_pdf=pdf
                )
                if _:
                    products.append(product)

        SDS_PDF.objects.bulk_create(pdfs)
        Product.objects.bulk_create(products)


class Command(BaseCommand, Helper):
    help = 'Command to extract CSV'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Path to csv zip files, that need to be extracted')
        parser.add_argument('harvest', type=str, help='Harvest Name')
        parser.add_argument('--secondary', dest='is_primary', default=True, action='store_false')

    def handle(self, *args, **kwargs):

        """Extracting Target File"""
        compressed_path = kwargs['path']
        harvest = kwargs['harvest']
        target_folder = self.SDS_PATH
        Archive(compressed_path).extractall(target_folder)

        """Reading CSV File and Putting in model"""
        csv_file_path = os.path.join(target_folder, f"{harvest}/{harvest}.csv")
        print('csv_file_path: ', csv_file_path)
        self.make_products(csv_file_path, harvest, kwargs['is_primary'])
