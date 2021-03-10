import os

import requests
from django.conf import settings
from django.core.management import BaseCommand
from django.utils.text import slugify
from tqdm import tqdm

from core.models import SDSURLImport, IgnoreDomain


class Command(BaseCommand):
    help = 'Command to process sds urls'
    path = f"{settings.BASE_DIR}/media/sds/manual"

    def handle(self, *args, **kwargs):
        """Downloading Manually imported SDS and Putting in model"""
        ignored_domains = IgnoreDomain.objects.values_list('domain', flat=True)
        for manual_sds in tqdm(SDSURLImport.objects.filter(is_downloaded=False, download_failed=False
                                                           ).exclude(domain__in=ignored_domains).all()):
            try:
                myfile = requests.get(url=manual_sds.link_to_pdf.replace('\ufeff', ''),
                                      allow_redirects=True,
                                      # headers={'Accept': '*/*', 'Host': manual_sds.domain}
                                      timeout=15
                                      )

                filename = slugify(manual_sds.domain+str(manual_sds.id))
                path = f"{self.path}/{slugify(manual_sds.domain)}"
                os.makedirs(path, exist_ok=True)

                with open(f"{path}/{filename}.pdf", 'wb') as pdf:
                    pdf.write(myfile.content)

                # manual_sds.path = '/media/sds/manual'
                manual_sds.is_downloaded = True
                manual_sds.save()
            except Exception as e:
                print("Error:")
                print(manual_sds.id, manual_sds.domain, e, sep=' | ')
                print(manual_sds.link_to_pdf)
                manual_sds.download_failed = True

            manual_sds.save()
