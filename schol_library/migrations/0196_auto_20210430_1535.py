# Generated by Django 2.2 on 2021-04-30 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0195_auto_20210429_1745'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='schooltitulhead',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='schooltitulplannedhead',
            unique_together=set(),
        ),
    ]
