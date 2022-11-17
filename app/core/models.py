from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=150, verbose_name='Item name')
    description = models.TextField(verbose_name='Item Description')
    price = models.PositiveIntegerField(verbose_name='Item price')


    def __str__(self):
        return f'{self.name} {self.price}'

