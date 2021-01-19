import json

from django.db.models import Count
from django.shortcuts import render

from core.models import Provider


def dashboard_with_pivot(request):
    stats = {count_obj['name']: count_obj['count']
             for count_obj in Provider.objects.annotate(count=Count('product')).values('name', 'count')}

    return render(request, 'core/stats_dashboard.html', {'table': stats, 'labels': list(stats.keys()),
                                                         'data': list(stats.values())})
