import csv

from django.core.management import BaseCommand

from core.models import Wishlist


class Command(BaseCommand):
    help = 'Command to load wishlist'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Path to wishlist file, that need to be loaded')

    def handle(self, *args, **kwargs):
        """Reading CSV File and Putting in model"""
        with open(kwargs['path'], encoding="utf8") as csv_file:
            for row in csv.DictReader(csv_file):
                wish, created = Wishlist.objects.get_or_create(
                    supplier=row['SUPPLIER'], trade_name=row['TRADE_NAME'], language=row['LANGUAGE']
                )
                if created:
                    wish.save()

        print('csv_file_path: ', kwargs['path'])

