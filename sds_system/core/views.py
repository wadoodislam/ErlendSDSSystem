import json
from rest_framework.views import APIView


from django.db.models import Count
from django.shortcuts import render
from elasticsearch_dsl import Q

from .documents import ProductDocument
from .forms import MatchForm
from .models import Provider





def search(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            supplier = form.cleaned_data['supplier']
            trade_name = form.cleaned_data['trade_name']
            if trade_name and supplier:
                query = Q("match", sds_product_name=trade_name) & Q("match", sds_manufacture_name=supplier)
            else:
                query = Q("match", sds_product_name=trade_name) | Q("match", sds_manufacture_name=supplier)
            matches = ProductDocument.search().query(query).to_queryset()
            products = matches.values('name', 'sds_product_name', 'sds_manufacture_name', 'link')

            return render(request, 'core/search.html', {'products': products, 'form': form})

    return render(request, 'core/search.html', {'form': MatchForm()})
