# Generated by Django 2.1.4 on 2019-02-01 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0010_edition_series_by_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edition',
            name='series_by_year',
            field=models.IntegerField(blank=True, default=2019, verbose_name='серия по годам'),
        ),
    ]
