from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CASCADE

User = get_user_model()


class Provider(models.Model):
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    language = models.ForeignKey(Language, on_delete=CASCADE)
    provider = models.ForeignKey(Provider, on_delete=CASCADE)
    sds_pdf_product_name = models.CharField(max_length=100, blank=True, null=True)
    sds_pdf_Hazards_identification = models.CharField(max_length=250, blank=True, null=True)
    sds_pdf_manufacture_name = models.CharField(max_length=100, blank=True, null=True)
    sds_pdf_print_date = models.CharField(max_length=30, blank=True, null=True)
    sds_pdf_revision_date = models.CharField(max_length=30, blank=True, null=True)
    sds_url = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProducerOfSDS(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)


class SDS(models.Model):
    name = models.CharField(max_length=30)
    url = models.URLField()
    file = models.FileField(null=True, upload_to='pdf')
    created_at = models.DateTimeField(auto_now_add=True)