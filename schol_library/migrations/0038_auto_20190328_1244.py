# Generated by Django 2.1.4 on 2019-03-28 06:44

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('schol_library', '0037_auto_20190318_1650'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='edition',
            options={'ordering': ['klass', 'subject', 'name'], 'verbose_name': 'издание',
                     'verbose_name_plural': 'издания'},
        ),
    ]
