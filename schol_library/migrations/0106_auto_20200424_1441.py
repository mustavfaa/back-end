# Generated by Django 2.2 on 2020-04-24 08:41

from django.db import migrations, models
import schol_library.models


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0105_auto_20200424_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paperinvoice',
            name='bin',
            field=models.CharField(max_length=12, validators=[schol_library.models.validate_bin_length], verbose_name='БИН'),
        ),
    ]