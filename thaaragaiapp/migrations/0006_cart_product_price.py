# Generated by Django 5.0.1 on 2024-02-04 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thaaragaiapp', '0005_alter_cart_product_qty'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='product_price',
            field=models.IntegerField(default=0),
        ),
    ]
