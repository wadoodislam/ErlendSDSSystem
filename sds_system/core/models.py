from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CASCADE
import hashlib
from datetime import date

User = get_user_model()


class Provider(models.Model):
    name = models.CharField(max_length=100)
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
    language = models.ForeignKey(Language, on_delete=CASCADE)
    provider = models.ForeignKey(Provider, on_delete=CASCADE)
    sds_pdf_product_name = models.CharField(max_length=100, blank=True, null=True)
    sds_pdf_Hazards_identification = models.CharField(max_length=250, blank=True, null=True)
    sds_pdf_manufacture_name = models.CharField(max_length=100, blank=True, null=True)
    sds_pdf_print_date = models.DateField(default=date.today, blank=True, null=True)
    sds_pdf_revision_date = models.DateField(default=date.today, blank=True, null=True)
    sds_url = models.CharField(max_length=250, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        pk = str(self.provider) + '-' + str(self.sds_pdf_product_name)
        self.id = hashlib.md5(pk.encode()).hexdigest()
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProducerOfSDS(models.Model):
    name = models.CharField(max_length=30)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class SDS(models.Model):
    name = models.CharField(max_length=30)
    url = models.URLField()
    file = models.FileField(null=True, upload_to='pdf')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Wishlist(models.Model):
    supplier = models.CharField(max_length=100)
    trade_name = models.CharField(max_length=100)
    language = models.CharField(max_length=30)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
