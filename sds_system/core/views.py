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


def match(request, id):
    wish = Wishlist.objects.filter(id=id).values("id", 'supplier', 'trade_name', 'language')[0]

    form = MatchForm(request.POST) if request.method == 'POST' else MatchForm(wish)

    if form.is_valid():
        supplier = form.cleaned_data['supplier']
        trade_name = form.cleaned_data['trade_name']

    if trade_name and supplier:
        query = Q("match", sds_product_name=trade_name) & Q("match", sds_manufacture_name=supplier)
    else:
        query = Q("match", sds_product_name=trade_name) | Q("match", sds_manufacture_name=supplier)
    matches = ProductDocument.search().query(query).to_queryset()
    products = matches.values('name', 'sds_product_name', 'sds_manufacture_name', 'link', "id")
    return render(request, 'core/match.html', {'products': products, "wish": wish, 'form': form})


def pair(request, wishlist_id):
    product_id = request.POST['match']
    wishlist = Wishlist.objects.get(id=wishlist_id)
    wishlist.product = Product.objects.get(id=product_id)
    wishlist.matched = True
    wishlist.save()
    return redirect('/admin/core/wishlist/')
