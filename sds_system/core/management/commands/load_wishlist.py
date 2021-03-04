import csv

from django.core.management import BaseCommand
from tqdm import tqdm

from core.models import Wishlist


class Command(BaseCommand):
    help = 'Command to load wishlist'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Path to wishlist file, that need to be loaded')

    def handle(self, *args, **kwargs):
        """Reading CSV File and Putting in model"""
        wishes = []
        with open(kwargs['path'], encoding="utf8") as csv_file:
            wish_rows = list(csv.DictReader(csv_file))
            for row in tqdm(wish_rows, total=len(wish_rows)):
                wish = Wishlist.objects.create(
                    supplier=row.get('SUPPLIER', row['SUPPLIER']), trade_name=row['TRADE_NAME'], language=row['LANGUAGE']
                )
                # if created:
                wishes.append(wish)

        Wishlist.objects.bulk_create(wishes)
        print('csv_file_path: ', kwargs['path'])

