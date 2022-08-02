from statistics import mode
from django.db import models

class CurrencyData(models.Model):
    id = models.UUIDField(primary_key=True)
    language = models.CharField(max_length=36)
    Country_name = models.CharField(max_length=120)
    Country_code = models.CharField(max_length=10)
    Date = models.DateField(max_length=20)
    Rate = models.CharField(max_length=20)