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


# class ProviderViewSet(viewsets.ModelViewSet):
#     queryset = Provider.objects.all()
#     serializer_class = ProviderSerializer
#
#     @action(methods=['GET'], detail=False)
#     def stats(self, request):
#         obj = [{'provider': count_obj['name'], 'products': count_obj['count']}
#                for count_obj in Provider.objects.annotate(count=Count('product')).values('name', 'count')]
#         return JsonResponse(obj, safe=False)
