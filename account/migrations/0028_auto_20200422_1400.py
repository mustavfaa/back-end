# Generated by Django 2.2 on 2020-04-22 08:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0027_auto_20200422_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesstoedit',
            name='date_invoice',
            field=models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='Дата для накладных'),
        ),
    ]