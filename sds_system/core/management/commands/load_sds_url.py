import csv
from urllib.parse import urlparse

from django.core.management import BaseCommand

from core.models import SDSURLImport
from tqdm import tqdm


class Command(BaseCommand):
    help = 'Command to load sds url import'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Path to sds url file, that need to be loaded')

    def handle(self, *args, **kwargs):
        """Reading CSV File and Putting in model"""
        with open(kwargs['path'], encoding="utf8") as csv_file:
            url_rows = list(csv.DictReader(csv_file, fieldnames=['url']))
            for row in tqdm(url_rows, total=len(url_rows)):
                url_import = SDSURLImport.objects.create(
                    link_to_pdf=row.get('url', row['url']), domain=urlparse(row.get('url', row['url'])).netloc
                )

                url_import.save()

        print('csv_file_path: ', kwargs['path'])



