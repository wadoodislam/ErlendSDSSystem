import PyPDF2

from django.core.management import BaseCommand
from django.utils.text import slugify
from tqdm import tqdm

from core.models import Language, SDSURLImport


class Command(BaseCommand):
    help = 'Command to detect language of a pdf'
    path = "media/sds/manual"
    text = ""

    def handle(self, *args, **kwargs):
        for manual_sds in tqdm(SDSURLImport.objects.filter(is_downloaded=True).all()):
            try:
                filename = slugify(manual_sds.domain + str(manual_sds.id))
                file_path = f"{self.path}/{slugify(manual_sds.domain)}/{filename}.pdf"
                pdfReader = PyPDF2.PdfFileReader(open(file_path, "rb"))

                for page_num in range(pdfReader.numPages):
                    pageObj = pdfReader.getPage(page_num)
                    self.text = self.text + f'{pageObj.extractText()}'

                if 'SICHERHEITSDATENBLATT' in self.text:
                    language = 'ge'
                elif 'sikkerhetsdatablad' in self.text:
                    language = 'nb'
                elif 'safety data sheet' in self.text:
                    language = 'en'
                elif 'Sikkerhedsdatablad' in self.text:
                    language = 'dk'
                elif 'Säkerhetsdatablad' in self.text:
                    language = 'se'
                elif 'FICHA DE DATOS DE SEGURIDAD' in self.text:
                    language = 'es'
                elif 'FICHA DE INFORMAÇÃO DE SEGURANÇA DE PRODUTO QUÍMICO' in self.text:
                    language = 'pt'
                else:
                    language = False

                if language:
                    manual_sds.language = Language.objects.get(name=language)
                    manual_sds.save()

                self.text = ''

            except Exception as e:
                print("Error:", filename, e, sep=' | ')
