# Generated by Django 2.2 on 2020-05-18 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0152_editioninitialbalance1_initialbalance1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='initialbalance',
            name='author',
        ),
        migrations.RemoveField(
            model_name='initialbalance',
            name='school',
        ),
        migrations.DeleteModel(
            name='EditionInitialBalance',
        ),
        migrations.DeleteModel(
            name='InitialBalance',
        ),
    ]
