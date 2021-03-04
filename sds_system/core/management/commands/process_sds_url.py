from django.core.management import BaseCommand
import requests
from core.models import SDSURLImport, SDS_PDF, SDSHarvestSource
from core.utils import md5hash


class Command(BaseCommand):
    help = 'Command to process sds urls'
    path = "media/sds/manual"

    def handle(self, *args, **kwargs):
        """Downloading Manually imported SDS and Putting in model"""
        for manual_sds in SDSURLImport.objects.all():
            if not manual_sds.is_processed:
                myfile = requests.get(url=manual_sds.link_to_pdf, allow_redirects=True)
                open(f"{self.path}/file{manual_sds.id}.pdf", 'wb').write(myfile.content)

                pdf = SDS_PDF.objects.create(
                    name=f'file{manual_sds.id}',
                    sds_link=f"{self.path}file{manual_sds.id}.pdf",
                    sds_download_url=manual_sds.link_to_pdf,
                    from_primary=False,
                    manual=True,
                    sds_harvest_source=SDSHarvestSource.objects.get(name='Manually_imported_sds_urls'),
                    pdf_md5=md5hash(f'file{manual_sds.id}', SDSHarvestSource.objects.get(name='Manually_imported_sds_urls')))

                pdf.save()

                manual_sds.sds_pdf = pdf
                manual_sds.is_processed = True
                manual_sds.save()
