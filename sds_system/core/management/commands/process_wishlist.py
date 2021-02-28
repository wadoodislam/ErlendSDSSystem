from django.core.management import BaseCommand
from elasticsearch_dsl import Q

from core.documents import SDSDocument
from core.models import Wishlist


class Command(BaseCommand):
    help = 'Command to process wishlist'

    def handle(self, *args, **kwargs):
        """Reading CSV File and Putting in model"""
        for wish in Wishlist.objects.all():
            query = Q("term", sds_product_name=wish.trade_name) & Q("term", sds_manufacture_name=wish.supplier)
            matches = SDSDocument.search().query(query).to_queryset()
            if matches.exists():
                wish.product = matches.first()
                wish.save()
