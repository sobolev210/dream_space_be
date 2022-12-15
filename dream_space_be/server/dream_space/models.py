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
    favorites = models.ManyToManyField("Product")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]


class Shop(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True)
    address = models.CharField(max_length=500, null=True)
    logo = models.ImageField(null=True)
    contact = models.CharField(max_length=255, null=False)


class Product(models.Model):
    CATEGORY_CHOICES = [
        ("BAT", "Bathroom"),
        ("BED", "Bedroom"),
        ("KIT", "Kitchen"),
        ("LIV", "Living room"),
        ("GAR", "Garden"),
        ("COR", "Corridor"),
        ("OTH", "Other")
    ]
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True)
    price = models.FloatField()
    category = models.CharField(
        max_length=3,
        choices=CATEGORY_CHOICES,
        null=False
    )
    length = models.FloatField(null=False)
    width = models.FloatField(null=False)
    height = models.FloatField(null=False)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)


class ProductImage(models.Model):
    image = models.ImageField(null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")


class ProductColor(models.Model):
    color = models.CharField(max_length=10, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="colors")


# class BuyRequest(models.Model):
#     pass

