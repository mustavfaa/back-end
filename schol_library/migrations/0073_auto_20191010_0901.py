# Generated by Django 2.2 on 2019-10-10 03:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('schol_library', '0072_auto_20191009_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestedition',
            name='date_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 10, 10, 9, 1, 5, 488384),
                                       verbose_name='время заявки'),
        ),
    ]
