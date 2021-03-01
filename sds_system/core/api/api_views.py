from django.db.models import Count
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from .serializers import *

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class HarvestSourceViewSet(viewsets.ModelViewSet):
    queryset = SDSHarvestSource.objects.all()
    serializer_class = SDSHarvestSourceSerializer

    @action(methods=['GET'], detail=False)
    def stats(self, request):
        obj = [{'provider': count_obj['name'], 'products': count_obj['count']}
               for count_obj in SDSHarvestSource.objects.annotate(count=Count('sds_pdf')).values('name', 'count')]
        return JsonResponse(obj, safe=False)


class SDSPDFViewSet(viewsets.ModelViewSet):
    queryset = SDS_PDF.objects.all()
    serializer_class = SDSPDFSerializer

# python manage.py zip_importer ~/2020nov_primary/fishersci

# python manage.py zip_importer ~/2020nov_primary/shell_alpesh
# python manage.py zip_importer ~/2020nov_primary/corporate-evonik-com
# python manage.py zip_importer ~/2020nov_primary/abenaonline
# python manage.py zip_importer ~/2020nov_primary/crc_ambersil
# python manage.py zip_importer ~/2020nov_primary/talgo
# python manage.py zip_importer ~/2020nov_primary/hagerwerken
# python manage.py zip_importer ~/2020nov_primary/beckers
# python manage.py zip_importer ~/2020nov_primary/norenco
# python manage.py zip_importer ~/2020nov_primary/nogusra
# python manage.py zip_importer ~/2020nov_primary/akzonobel
# python manage.py zip_importer ~/2020nov_primary/okkjemi
# python manage.py zip_importer ~/2020nov_primary/gc_europe
# python manage.py zip_importer ~/2020nov_primary/AkzoNobelCoatingsNordsjo
# python manage.py zip_importer ~/2020nov_primary/crc_kontaktchemie
# python manage.py zip_importer ~/2020nov_primary/univarlubricants
# python manage.py zip_importer ~/2020nov_primary/robustnorge
# python manage.py zip_importer ~/2020nov_primary/nordexia_removed_non_nordexia_sds
# python manage.py zip_importer ~/2020nov_primary/bostik
# python manage.py zip_importer ~/2020nov_primary/eco_mailback_02
# python manage.py zip_importer ~/2020nov_primary/skf-maintenance
# python manage.py zip_importer ~/2020nov_primary/castolin
# python manage.py zip_importer ~/2020nov_primary/krepro
# python manage.py zip_importer ~/2020nov_primary/maxbo
# python manage.py zip_importer ~/2020nov_primary/crc_kf
# python manage.py zip_importer ~/2020nov_primary/3mnorge
# python manage.py zip_importer ~/2020nov_primary/motip
# python manage.py zip_importer ~/2020nov_primary/interflon-com
# python manage.py zip_importer ~/2020nov_primary/Relekta_ex_industriolje
# python manage.py zip_importer ~/2020nov_primary/permakem
# python manage.py zip_importer ~/2020nov_primary/boliden
# python manage.py zip_importer ~/2020nov_primary/sygenta_crop_protection
# python manage.py zip_importer ~/2020nov_primary/ingveege
# python manage.py zip_importer ~/2020nov_primary/multichemwallinco
# python manage.py zip_importer ~/2020nov_primary/terjan
# python manage.py zip_importer ~/2020nov_primary/kerrdendal-com
# python manage.py zip_importer ~/2020nov_primary/steinfix-no
# python manage.py zip_importer ~/2020nov_primary/PremiereProdukter
# python manage.py zip_importer ~/2020nov_primary/coltene
# python manage.py zip_importer ~/2020nov_primary/jula
# python manage.py zip_importer ~/2020nov_primary/chesterton
# python manage.py zip_importer ~/2020nov_primary/msdspds-castrol-com
# python manage.py zip_importer ~/2020nov_primary/pioneereclipse
# python manage.py zip_importer ~/2020nov_primary/ici_paints_akzonobel
# python manage.py zip_importer ~/2020nov_primary/ibmo
# python manage.py zip_importer ~/2020nov_primary/shell
# python manage.py zip_importer ~/2020nov_primary/icopal
# python manage.py zip_importer ~/2020nov_primary/essoenergi
# python manage.py zip_importer ~/2020nov_primary/BASF
# python manage.py zip_importer ~/2020nov_primary/olje-yx
# python manage.py zip_importer ~/2020nov_primary/staples
# python manage.py zip_importer ~/2020nov_primary/soudal
# python manage.py zip_importer ~/2020nov_primary/aromdecor
# python manage.py zip_importer ~/2020nov_primary/coop
# python manage.py zip_importer ~/2020nov_primary/exxonmobil
# python manage.py zip_importer ~/2020nov_primary/norebo
# python manage.py zip_importer ~/2020nov_primary/crc_europe
# python manage.py zip_importer ~/2020nov_primary/cropscience
# python manage.py zip_importer ~/2020nov_primary/nch_norge
# python manage.py zip_importer ~/2020nov_primary/carlroth
# python manage.py zip_importer ~/2020nov_primary/info_roundup
