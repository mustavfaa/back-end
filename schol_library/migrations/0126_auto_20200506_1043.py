# Generated by Django 2.2 on 2020-05-06 04:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('schol_library', '0125_auto_20200506_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='initialbalance',
            name='date',
            field=models.DateField(null=True, verbose_name='Дата ввода остатков'),
        ),
    ]
