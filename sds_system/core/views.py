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
    return render(request, 'core/stats_dashboard.html', {})


def pivot_data(request):
    dataset = Product.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)
