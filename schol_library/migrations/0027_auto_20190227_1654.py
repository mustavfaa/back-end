# Generated by Django 2.1.4 on 2019-02-27 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0026_auto_20190227_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='edition',
            name='publish_date',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='publish_date', to='schol_library.Year', verbose_name='год издания'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='edition',
            name='series_by_year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='series_by_year', to='schol_library.Year', verbose_name='серия по годам'),
        ),
    ]
