# Generated by Django 4.1.5 on 2023-01-19 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_alter_listing_description_comment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comments',
        ),
    ]
