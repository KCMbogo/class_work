# Generated by Django 4.2.11 on 2024-05-22 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_contactus_is_signed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contactus',
            old_name='is_signed',
            new_name='is_email_signed',
        ),
    ]
