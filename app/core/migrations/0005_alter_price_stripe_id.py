# Generated by Django 4.1.3 on 2022-11-18 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='stripe_id',
            field=models.CharField(default='', max_length=256, null=True, verbose_name='Stripe product ID'),
        ),
    ]