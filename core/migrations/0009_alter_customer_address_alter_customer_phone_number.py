# Generated by Django 5.0.4 on 2024-04-30 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(default=None, max_length=20),
        ),
    ]