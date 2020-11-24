from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    email = models.EmailField('email address', unique=True, help_text='Required, Add a valid email address')
    phone_number = PhoneNumberField(help_text='Required, Add a valid phone number')
    hourly_rate_usd = models.IntegerField(null=True)
    url_to_contract = models.URLField(null=True)

    def __str__(self):
        return self.username
