# Generated by Django 2.2 on 2020-05-18 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0150_auto_20200518_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editionbriefcase',
            name='surplus',
            field=models.SmallIntegerField(default=0, verbose_name='Процент обеспечения'),
        ),
    ]
