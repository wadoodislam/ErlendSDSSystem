import csv
import glob
import os
import datetime

from django.core.management import BaseCommand
from pyunpack import Archive

from core.models import Product, Language, Provider


class Command(BaseCommand):
    help = 'Command to extract CSV'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Path to csv zip files, that need to be extracted')

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        files_providers = [(os.path.basename(path)[:-4], path) for path in glob.glob(path+'/*.*')]
        errors = []

        for provider, file in files_providers:
            target_folder = f'../sds_scraper/sds_scraper/sds_data/'
            try:
                Archive(file).extractall(target_folder)
                if '.' in provider:
                    provider = provider.split('.')[0]

                """Reading CSV File and Putting in model"""
                csv_file_path = os.path.join(target_folder, f"{provider}/{provider}.csv")

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
                print(f'provider: {provider}')
            except Exception as e:
                errors.append(provider)
                print(f'{provider}: {e}')
