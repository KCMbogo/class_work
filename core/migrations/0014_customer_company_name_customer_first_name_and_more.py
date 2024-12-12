# Generated by Django 5.0.4 on 2024-05-01 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_remove_order_customer_remove_review_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='company_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='customer',
            name='first_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='customer',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
