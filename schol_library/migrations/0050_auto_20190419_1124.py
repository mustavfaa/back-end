# Generated by Django 2.2 on 2019-04-19 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0049_auto_20190418_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='briefcase',
            name='description',
            field=models.CharField(blank=True, max_length=50, verbose_name='описание'),
        ),
        migrations.AlterField(
            model_name='briefcase',
            name='name',
            field=models.CharField(blank=True, max_length=70, verbose_name='название портфеля'),
        ),
        migrations.DeleteModel(
            name='SetUMK',
        ),
    ]
