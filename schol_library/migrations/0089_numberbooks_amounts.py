# Generated by Django 2.2 on 2020-04-08 11:52

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0088_auto_20200407_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='numberbooks',
            name='amounts',
            field=models.IntegerField(blank=True, default=0, verbose_name='сумма'),
        ),
    ]
