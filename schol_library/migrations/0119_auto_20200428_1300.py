# Generated by Django 2.2 on 2020-04-28 07:00

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('schol_library', '0118_auto_20200428_1253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='numberbooks',
            name='in_register',
        ),
    ]
