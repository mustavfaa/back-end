# Generated by Django 2.2 on 2019-09-23 06:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0060_auto_20190923_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkidrequestedition',
            name='check2',
            field=models.BooleanField(blank=True, default=False, verbose_name='статус'),
        ),
        migrations.AlterField(
            model_name='requestedition',
            name='date_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 23, 12, 41, 35, 766691), verbose_name='время заявки'),
        ),
    ]