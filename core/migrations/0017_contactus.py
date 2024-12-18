# Generated by Django 4.2.11 on 2024-05-15 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_customer_district_customer_postcode_customer_town'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('message', models.TextField()),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
        ),
    ]
