# Generated by Django 2.2 on 2019-08-14 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0036_auto_20190813_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='editioninvoice',
            name='amount',
            field=models.IntegerField(blank=True, default=0, verbose_name='цена'),
        ),
        migrations.AddField(
            model_name='editionpaperinvoice',
            name='amount',
            field=models.IntegerField(blank=True, default=0, verbose_name='цена'),
        ),
    ]