from django.db import models
from django.dispatch import receiver


class Currency(models.Model):
    name = models.CharField(max_length=150, verbose_name='Currency name')
    symbol = models.CharField(max_length=16, verbose_name='Currency symbol')

    def __str__(self):
        return f'{self.symbol}'


class Price(models.Model):

    unit_price = models.FloatField(verbose_name='Unit price')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    stripe_id = models.CharField(
        max_length=256,
        default='',
        verbose_name='Stripe product ID'
    )

    
    def __str__(self):
        return f'{self.unit_price}{self.currency.symbol}'


class Item(models.Model):
    name = models.CharField(max_length=150, verbose_name='Item name')
    description = models.TextField(verbose_name='Item Description')
    price = models.ForeignKey(Price, null=True, blank=True, on_delete=models.SET_NULL)
    stripe_id = models.CharField(max_length=256, default='', verbose_name='Stripe product ID')


    def __str__(self):
        return f'{self.id}) {self.name}'
