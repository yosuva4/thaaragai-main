# Generated by Django 5.0.1 on 2024-02-02 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thaaragaiapp', '0002_alter_products_producttype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='productCode',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
