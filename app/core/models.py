from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save


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
        null=True,
        blank=True,
        default='',
        verbose_name='Stripe product ID'
    )

    def __str__(self):
        return f'{self.unit_price}{self.currency.symbol}'

@receiver(pre_save, sender=Price)
def check_updated_price(sender, instance, update_fields=None, **kwargs):
    try:
        old_instance = Price.objects.get(id=instance.id)
    except Price.DoesNotExist:
        return 
    
    if instance.unit_price != old_instance.unit_price or \
        instance.currency.name != old_instance.currency.name:
            instance.stripe_id = ''


class Item(models.Model):
    name = models.CharField(max_length=150, verbose_name='Item name')
    description = models.TextField(verbose_name='Item Description')
    price = models.ForeignKey(Price, null=True, blank=True, on_delete=models.SET_NULL)
    stripe_id = models.CharField(max_length=256, default='', verbose_name='Stripe product ID')


    def __str__(self):
        return f'{self.id}) {self.name}'


@receiver(pre_save, sender=Item)
def check_updated_item(sender, instance, update_fields=None, **kwargs):
    try:
        old_instance = Item.objects.get(id=instance.id)
    except Item.DoesNotExist:  # to handle initial object creation
        return None  # just exiting from signal

    # if something chaned
    if instance.name != old_instance.name or \
        instance.description != old_instance.description:
            # we need new Stripe Product instance
            instance.stripe_id = ''
            # and new Stripe Price instance
            instance.price.stripe_id = ''
            instance.price.save()


class Order(models.Model):
    items = models.ManyToManyField(Item)

    def __str__(self):
        return f'Order {self.id} with {len(self.items.all())} items'