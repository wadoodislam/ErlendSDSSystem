import csv
import os
import datetime

from django.core.management import BaseCommand
from pyunpack import Archive

from core.models import Product, Language, Provider


class Command(BaseCommand):
    help = 'Command to extract CSV'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Path to csv zip files, that need to be extracted')
        parser.add_argument('provider', type=str, help='Provider Name')

    def handle(self, *args, **kwargs):
        # extract zip file
        # read CSVs and feed in Product Model

        """Extracting Target File"""
        compressed_path = kwargs['path']
        provider = kwargs['provider']
        target_folder = f'../sds_scraper/sds_scraper/sds_data/'
        Archive(compressed_path).extractall(target_folder)

        """Reading CSV File and Putting in model"""
        csv_file_path = os.path.join(target_folder, f"{provider}/{provider}.csv")
        print('csv_file_path: ', csv_file_path)

        with open(csv_file_path) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                prov, _ = Provider.objects.get_or_create(name=provider)
                lang, _ = Language.objects.get_or_create(name=row['sds_language'])
                product_model = Product(name=os.path.split(row['sds_pdf_filename_in_zip'])[1],
                                        language=lang,
                                        provider=prov,
                                        sds_pdf_product_name=row['sds_pdf_product_name'],
                                        sds_pdf_Hazards_identification=row['sds_pdf_Hazards_identification'],
                                        sds_pdf_manufacture_name=row['sds_pdf_manufacture_name'],
                                        sds_pdf_print_date=datetime.datetime.strptime(row['sds_pdf_published_date'],
                                                                                      '%d.%m.%Y').replace(tzinfo=datetime.timezone.utc),
                                        sds_pdf_revision_date=datetime.datetime.strptime(row['sds_pdf_revision_date'],
                                                                                         '%d.%m.%Y').replace(tzinfo=datetime.timezone.utc),
                                        sds_url=row['product_url'])
                product_model.save()
