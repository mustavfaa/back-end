# Generated by Django 2.2 on 2020-04-09 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0089_numberbooks_amounts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='numberbooks',
            name='in_warehouse',
            field=models.IntegerField(blank=True, default=0, verbose_name='на складе'),
        ),
        migrations.AlterField(
            model_name='numberbooks',
            name='on_hands',
            field=models.IntegerField(blank=True, default=0, verbose_name='на руках'),
        ),
    ]
