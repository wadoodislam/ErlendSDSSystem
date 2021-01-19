from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Provider(models.Model):
    name = models.CharField(max_length=100)
    primary = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=30)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.CharField(primary_key=True, editable=False, null=False, max_length=32)
    name = models.CharField(max_length=100)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    link = models.URLField()

    sds_url = models.URLField()
    sds_product_name = models.CharField(max_length=100)
    sds_hazards_codes = models.CharField(max_length=250, blank=True, null=True)
    sds_manufacture_name = models.CharField(max_length=100)
    sds_print_date = models.DateField(blank=True, null=True)
    sds_published_date = models.DateField(blank=True, null=True)
    sds_revision_date = models.DateField(blank=True, null=True)
    sds_release_date = models.DateField(blank=True, null=True)

    crawled_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProducerOfSDS(models.Model):
    name = models.CharField(max_length=30)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Wishlist(models.Model):
    supplier = models.CharField(max_length=100)
    trade_name = models.CharField(max_length=100)
    language = models.CharField(max_length=30)
    matched = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

