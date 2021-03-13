import PyPDF2
import glob

from django.core.management import BaseCommand
from django.utils.text import slugify
from tqdm import tqdm

from core.models import Language, SDSURLImport


class Command(BaseCommand):
    help = 'Command to detect language of a pdf'
    path = "media/sds/manual"
    text = ""

    def handle(self, *args, **kwargs):
        # for file in glob.glob(self.path+'/*'):
        # language_of_SDSURLImport = Language.objects.get(name='ge')
        for manual_sds in tqdm(SDSURLImport.objects.filter(is_downloaded=True).all()):
            filename = slugify(manual_sds.domain + str(manual_sds.id))
            file_path = f"{self.path}/{slugify(manual_sds.domain)}/{filename}.pdf"
            pdfReader = PyPDF2.PdfFileReader(open(file_path, "rb"))


            for page_num in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(page_num)
                self.text = self.text + f'{pageObj.extractText()}'

            if 'SICHERHEITSDATENBLATT' in self.text:
                #ge German
                #language_of_SDSURLImport = Language.objects.get(name='ge')
                pass
            elif 'sikkerhetsdatablad' in self.text:
                #nb Norwegian
                #language_of_SDSURLImport = Language.objects.get(name='nb')
                pass
            elif 'safety data sheet' in self.text:
                #en English
                #language_of_SDSURLImport = Language.objects.get(name='en')
                pass
            elif 'Sikkerhedsdatablad' in self.text:
                #dk Danish
                #language_of_SDSURLImport = Language.objects.get(name='dk')
                pass
            elif 'Säkerhetsdatablad' in self.text:
                #se Swedish
                #language_of_SDSURLImport = Language.objects.get(name='se')
                pass
            elif 'FICHA DE DATOS DE SEGURIDAD' in self.text:
                #es Spanish
                #language_of_SDSURLImport = Language.objects.get(name='es')
                pass
            elif 'FICHA DE INFORMAÇÃO DE SEGURANÇA DE PRODUTO QUÍMICO' in self.text:
                #pt Portugese
                #language_of_SDSURLImport = Language.objects.get(name='pt')
                pass
            else:
                # not detected
                pass

            self.text = ''
