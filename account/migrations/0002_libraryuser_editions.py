# Generated by Django 2.1.4 on 2019-01-25 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0006_auto_20190121_1741'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='libraryuser',
            name='editions',
            field=models.ManyToManyField(to='schol_library.Edition'),
        ),
    ]
