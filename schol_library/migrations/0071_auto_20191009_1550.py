# Generated by Django 2.2 on 2019-10-09 09:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('schol_library', '0070_auto_20191009_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestedition',
            name='date_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 10, 9, 15, 50, 26, 237270),
                                       verbose_name='время заявки'),
        ),
    ]
