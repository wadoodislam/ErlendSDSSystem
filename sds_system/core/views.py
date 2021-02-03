import json
import requests

from django.db.models import Count
from django.shortcuts import render, redirect
from elasticsearch_dsl import Q

from core.documents import ProductDocument
from core.forms import MatchForm
from core.models import *


def dashboard_with_pivot(request):
    stats = {count_obj['name']: count_obj['count']
             for count_obj in Provider.objects.annotate(count=Count('product')).values('name', 'count')}

    return render(request, 'core/stats_dashboard.html', {'table': stats, 'labels': list(stats.keys()),
                                                         'data': list(stats.values())})


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


def match(request, id):
    wish = Wishlist.objects.get(id=id)

    if wish.trade_name and wish.supplier:
        query = Q("match", sds_product_name=wish.trade_name) & Q("match", sds_manufacture_name=wish.supplier)
    else:
        query = Q("match", sds_product_name=wish.trade_name) | Q("match", sds_manufacture_name=wish.supplier)
    matches = ProductDocument.search().query(query).to_queryset()
    products = matches.values('name', 'sds_product_name', 'sds_manufacture_name', 'link', "id")

    return render(request, 'core/match.html', {'products': products, "wishlist_id": id})


def pair(request, wishlist_id):
    product_id = request.POST['match']
    wishlist = Wishlist.objects.get(id=wishlist_id)
    requests.put(url=f'http://127.0.0.1:8080/core/api/wishlist/{wishlist_id}/',
                 data={"supplier": wishlist.supplier, "trade_name": wishlist.trade_name,
                       "language": wishlist.language, "matched": True, 'product': product_id})

    return redirect('../../../admin/')



