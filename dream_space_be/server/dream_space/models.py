from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    telegram_alias = models.CharField(max_length=255, null=True, blank=True)
    settings = models.TextField(null=True, blank=True)
    shops = models.ManyToManyField("Shop")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]


class Shop(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True)
    address = models.CharField(max_length=500, null=True)
    logo = models.ImageField(null=True)


