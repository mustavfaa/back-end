# Generated by Django 2.2 on 2020-05-05 10:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('schol_library', '0122_editioninitialbalance_initialbalance'),
    ]

    operations = [
        migrations.AddField(
            model_name='initialbalance',
            name='date',
            field=models.DateTimeField(null=True, verbose_name='Дата ввода остатков'),
        ),
    ]