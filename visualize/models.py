from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.

class CompanyFundamentals(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    pe = models.FloatField()
    pb = models.FloatField()
    div = models.FloatField(null=True)
    volume = models.BigIntegerField(null=True)
    marketcap = models.BigIntegerField()
    yearhigh = models.FloatField()
    yearlow = models.FloatField()
    rev2018 = models.BigIntegerField(null=True)
    rev2019 = models.BigIntegerField(null=True)
    rev2020 = models.BigIntegerField(null=True)
    rev2021 = models.BigIntegerField(null=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.symbol
