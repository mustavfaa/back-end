# Generated by Django 2.2 on 2019-08-12 05:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('schol_library', '0029_auto_20190808_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edition',
            name='delivery_document',
            field=models.CharField(blank=True, default=0, max_length=200, verbose_name='документ поставки'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='publisher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='schol_library.PublisherEdition', verbose_name='издательство'),
        ),
    ]
