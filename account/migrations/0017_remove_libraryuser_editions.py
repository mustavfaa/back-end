# Generated by Django 2.1.4 on 2019-02-27 04:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_auto_20190219_1555'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='libraryuser',
            name='editions',
        ),
    ]
