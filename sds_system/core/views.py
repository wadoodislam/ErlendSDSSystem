from datetime import datetime

import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect
from elasticsearch_dsl import Q

from core.documents import SDSDocument, ManufacturerDocument
from core.forms import MatchForm
from core.models import *


def dashboard_with_pivot(request):
    stats = {count_obj['name']: count_obj['count']
             for count_obj in SDSHarvestSource.objects.annotate(count=Count('sds_pdf')).values('name', 'count')}

    return render(request, 'core/stats_dashboard.html', {'table': stats, 'labels': list(stats.keys()),
                                                         'data': list(stats.values())})


def match(request, id):
    wish = Wishlist.objects.filter(id=id).values("id", 'supplier', 'trade_name', 'language')[0]

    form = MatchForm(request.POST) if request.method == 'POST' else MatchForm(wish)

    if form.is_valid():
        supplier = form.cleaned_data['supplier']
        trade_name = form.cleaned_data['trade_name']

    query = {}

    if supplier:
        q_set = ManufacturerDocument.search().query(Q("match", name=supplier))
        # query['manufacturer.id'] = list(map(lambda x:str(x), q_set.to_queryset().values_list('id', flat=True)))
        # matches = matches.filter(manufacturer__name__contains=supplier)

    if trade_name:
        query['sds_product_name'] = trade_name

    matches = SDSDocument.search().query(Q("match", **query)).to_queryset()

    products = matches.values('name', 'sds_product_name', 'manufacturer__name', 'sds_link', "pdf_md5")
    return render(request, 'core/match.html', {'products': products, "wish": wish, 'form': form})


@login_required
def run_harvest(request, id):
    harvest = SDSHarvestSource.objects.get(id=id)
    run = SDSHarvestRun.objects.create(sds_harvest_source=harvest, run_by=request.user, started_at=datetime.now())
    harvest.last_run_at = run.created_at
    run.save()
    harvest.save()
    data = {
        'spider': f'{harvest.id}_crawl', 'project': 'sds-scraper', 'run_id': run.id
    }
    resp = requests.post(f'{settings.MACHINE_URL}:6800/schedule.json', data)
    if resp.status_code == 200:
        run.save()
        harvest.save()

    return render(request, 'core/run_harvest.html', {'harvest': harvest, "run": run})


def pair(request, wishlist_id):
    product_id = request.POST['match']
    wishlist = Wishlist.objects.get(id=wishlist_id)
    wishlist.sds_pdf = SDS_PDF.objects.get(pdf_md5=product_id)
    wishlist.matched = True
    wishlist.save()
    return redirect('/admin/core/wishlist/')
