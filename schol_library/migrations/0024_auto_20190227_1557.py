# Generated by Django 2.1.4 on 2019-02-27 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0023_auto_20190227_1554'),
    ]

    operations = [
        migrations.RenameField(
            model_name='year',
            old_name='year',
            new_name='name',
        ),
    ]