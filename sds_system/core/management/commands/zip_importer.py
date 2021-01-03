import csv
import hashlib
import os
from datetime import datetime, timezone

from django.core.management import BaseCommand
from pyunpack import Archive

from core.models import Product, Language, Provider


class Helper:
    SDS_PATH = f'sds'

    def hash(self, name, provider):
        hashed = name + '-' + provider
        return hashlib.md5(hashed.encode()).hexdigest()

    def make_products(self, csv_file_path, provider):
        with open(csv_file_path) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                prov, _ = Provider.objects.get_or_create(name=provider)
                lang, _ = Language.objects.get_or_create(name=row['sds_language'])
                product, _ = Product.objects.update_or_create(
                    id=self.hash(row['sds_pdf_product_name'], provider),
                    defaults={
                        'name': os.path.split(row['sds_pdf_filename_in_zip'])[1],
                        'language': lang, 'provider': prov,
                        'sds_product_name': row['sds_pdf_product_name'],
                        'sds_hazards_codes': row['sds_pdf_Hazards_identification'],
                        'sds_manufacture_name': row['sds_pdf_manufacture_name'],
                        'crawled_at': datetime.strptime(row['crawl_date'], '%d.%m.%Y').replace(tzinfo=timezone.utc),
                        'sds_published_date': datetime.strptime(row['sds_pdf_published_date'],
                                                                '%d.%m.%Y').replace(tzinfo=timezone.utc),
                        'sds_revision_date': datetime.strptime(row['sds_pdf_revision_date'],
                                                               '%d.%m.%Y').replace(tzinfo=timezone.utc),
                        'sds_url': row['product_url'],
                        'sds_path': f"sds/{provider}{row['sds_pdf_filename_in_zip']}"
                    }
                )
                product.save()


class Command(BaseCommand, Helper):
    help = 'Command to extract CSV'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Path to csv zip files, that need to be extracted')
        parser.add_argument('provider', type=str, help='Provider Name')

    def handle(self, *args, **kwargs):

        """Extracting Target File"""
        compressed_path = kwargs['path']
        provider = kwargs['provider']
        target_folder = self.SDS_PATH
        Archive(compressed_path).extractall(target_folder)

        """Reading CSV File and Putting in model"""
        csv_file_path = os.path.join(target_folder, f"{provider}/{provider}.csv")
        print('csv_file_path: ', csv_file_path)
        self.make_products(csv_file_path, provider)
