# Generated by Django 2.2 on 2020-04-27 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0108_editionactwrite_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='actwriteoff',
            name='amount',
            field=models.FloatField(blank=True, default=0, verbose_name='Сумма'),
        ),
    ]
