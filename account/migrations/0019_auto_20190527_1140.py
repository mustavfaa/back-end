# Generated by Django 2.2 on 2019-05-27 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0018_auto_20190430_1018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='libraryuser',
            name='close_cabinet',
        ),
        migrations.RemoveField(
            model_name='libraryuser',
            name='school',
        ),
    ]
