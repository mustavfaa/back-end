# Generated by Django 2.2 on 2019-08-29 05:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0044_auto_20190829_1057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='editionpaperinvoice',
            name='planned_quantity',
        ),
    ]