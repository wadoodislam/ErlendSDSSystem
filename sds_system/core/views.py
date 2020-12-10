import json

from django.db.models import Count
from rest_framework import viewsets
from django.http import JsonResponse
from django.shortcuts import render
from .models import *
from .serializers import *
from django.core import serializers

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
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


def dashboard_with_pivot(request):
    labels = []
    data = []
    for table_data in provider_stats(request):
        provider_dict = json.loads(table_data)
    for chart in provider_dict:
        labels.append(chart['provider'])
        data.append(chart['products'])

    return render(request, 'core/stats_dashboard.html', {'table': provider_dict, 'labels': labels, 'data': data})


def provider_stats(request):
    obj = [{'provider': count_obj['name'], 'products': count_obj['count']}
           for count_obj in Provider.objects.annotate(count=Count('product')).values('name', 'count')]
    return JsonResponse(obj, safe=False)

