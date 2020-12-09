import csv
import os
import datetime
import shutil

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
        extracted_temp_folder = 'extracted_temp'

        """Extracting Target File"""
        compressed_path = kwargs['path']
        provider_name = kwargs['provider_name']
        file_name = os.path.split(compressed_path)[1]
        Archive(compressed_path).extractall(extracted_temp_folder)

        """Reading CSV File and Putting in model"""
        csv_file_path = os.path.join(extracted_temp_folder,
                                     os.path.join(file_name.split('.')[0], file_name.split('.')[0] + ".csv"))
        with open(csv_file_path) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                prov, provider_created = Provider.objects.get_or_create(name=provider_name)
                if provider_created:
                    prov.save()
                lang, language_created = Language.objects.get_or_create(name=row['sds_language'])
                if language_created:
                    lang.save()

                product_model = Product(
                    name=os.path.split(row['sds_pdf_filename_in_zip'])[1],
                    language=lang,
                    provider=prov,
                    sds_pdf_product_name=row['sds_pdf_product_name'],
                    sds_pdf_Hazards_identification=row['sds_pdf_Hazards_identification'],
                    sds_pdf_manufacture_name=row['sds_pdf_manufacture_name'],
                    sds_pdf_print_date=datetime.datetime.strptime(row['sds_pdf_published_date'], '%d.%m.%Y')
                        .replace(tzinfo=datetime.timezone.utc),
                    sds_pdf_revision_date=datetime.datetime.strptime(row['sds_pdf_revision_date'], '%d.%m.%Y')
                        .replace(tzinfo=datetime.timezone.utc),
                    sds_url=row['product_url'])
                product_model.save()

        """Delete folder content"""
        for filename in os.listdir(extracted_temp_folder):
            file_path = os.path.join(extracted_temp_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
