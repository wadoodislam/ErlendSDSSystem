from rest_framework import viewsets

from .models import *
from .serializers import *

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProducerOfSDSViewSet(viewsets.ModelViewSet):
    queryset = ProducerOfSDS.objects.all()
    serializer_class = ProducerOfSDSSerializer


class SDSViewSet(viewsets.ModelViewSet):
    queryset = SDS.objects.all()
    serializer_class = SDSSerializer
