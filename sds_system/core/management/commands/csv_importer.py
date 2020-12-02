import csv
import os

from django.core.management import BaseCommand
from pyunpack import Archive

from core.models import Product, Language, Provider



class Command(BaseCommand):
    help = 'Command to extract CSV'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Path to csv zip files, that need to be extracted')
        parser.add_argument('provider_name', type=str, help='Provider Name')

    def handle(self, *args, **kwargs):
        # extract zip file
        # read CSVs and feed in Product Model

        """Extracting Target File"""
        compressed_path = kwargs['path']
        provider_name = kwargs['provider_name']
        file_name = os.path.split(compressed_path)[1]
        directory = os.path.split(compressed_path)[0]
        Archive(compressed_path).extractall(directory)

        """Reading CSV File and Putting in model"""
        csv_file_path = os.path.join(directory, os.path.join(file_name.split('.')[0], file_name.split('.')[0] + ".csv"))
        print('csv_file_path: ', csv_file_path)
        with open(csv_file_path) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                # name = row['product_name']
                # source = row['source']
                # if "_spider" not in source.split('.')[0]:
                #     source = f'{source.split(".")[0]}_spider.py'
                # language = row['sds_language']
                # provider = provider_name
                # sds_pdf_product_name = row['sds_pdf_product_name']
                # sds_pdf_Hazards_identification = row['sds_pdf_Hazards_identification']
                # sds_pdf_manufacture_name = row['sds_pdf_manufacture_name']
                # sds_pdf_print_date = row['sds_pdf_published_date']
                # sds_pdf_revision_date = row['sds_pdf_revision_date']
                # sds_url = row['product_url']

                # Product Model
                prov = Provider.objects.get(name=provider_name)
                lang = Language.objects.get(name=row['sds_language'])
                product_model = Product(name=row['product_name'],
                                        language=lang,
                                        provider=prov,
                                        sds_pdf_product_name=row['sds_pdf_product_name'],
                                        sds_pdf_Hazards_identification=row['sds_pdf_Hazards_identification'],
                                        sds_pdf_manufacture_name=row['sds_pdf_manufacture_name'],
                                        sds_pdf_print_date=row['sds_pdf_published_date'],
                                        sds_pdf_revision_date=row['sds_pdf_revision_date'],
                                        sds_url=row['product_url'])
                product_model.save()
