# Generated by Django 2.2 on 2019-09-10 05:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0049_auto_20190909_1501'),
    ]

    operations = [
        migrations.RenameField(
            model_name='incomeexpense',
            old_name='school_id',
            new_name='school',
        ),
    ]