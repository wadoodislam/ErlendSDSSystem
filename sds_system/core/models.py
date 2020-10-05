from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CASCADE

User = get_user_model()


class Manufacturer(models.Model):
    name = models.CharField(max_length=20)
    created_date = models.DateTimeField(auto_now_add=True)


class Language(models.Model):
    name = models.CharField(max_length=30)


class Product(models.Model):
    name = models.CharField(max_length=30)
    language = models.ForeignKey(Language, on_delete=CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)


class ProducerOfSDS(models.Model):
    name = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)




