import glob
import os

from django.core.management import BaseCommand
from pyunpack import Archive

from core.management.commands.zip_importer import Helper


class Command(BaseCommand, Helper):
    help = 'Command to extract CSV'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Path to csv zip files, that need to be extracted')
        parser.add_argument('--secondary', dest='is_primary', default=True, action='store_false')

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        files_providers = [(os.path.basename(path)[:-4], path) for path in glob.glob(path+'/*.*')]
        errors = []

        for provider, file in files_providers:
            target_folder = self.SDS_PATH
            try:
                Archive(file).extractall(target_folder)
                if '.' in provider:
                    provider = provider.split('.')[0]
                """Reading CSV File and Putting in model"""
                csv_file_path = os.path.join(target_folder, f"{provider}/{provider}.csv")
                self.make_products(csv_file_path, provider, kwargs['is_primary'])
                print(f'provider: {provider}')
            except Exception as e:
                errors.append(provider)
                print(f'{provider}: {e}')
