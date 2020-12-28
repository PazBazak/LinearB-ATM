from django.db import models
from decimal import Decimal


# Create your models here.


class Currency(models.Model):
    name = models.TextField(max_length=36)

    def __str__(self):
        return self.name


class Bill(models.Model):

    class BillValues(models.IntegerChoices):
        B200 = 200
        B100 = 100
        B50 = 50
        B20 = 20

    value = models.IntegerField(choices=BillValues.choices)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.value) + self.currency.name


class Coin(models.Model):

    COIN_CHOICES = (
        (Decimal("10.0"), "C10"),
        (Decimal("5.0"), "C5"),
        (Decimal("1.0"), "C1"),
        (Decimal("0.1"), "C0_1"),
        (Decimal("0.01"), "C0_01"),
    )

    value = models.DecimalField(max_digits=4, decimal_places=2, choices=COIN_CHOICES)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.value) + self.currency.name




