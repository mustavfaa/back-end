# Generated by Django 2.1.4 on 2019-01-25 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0008_edition_isbn'),
        ('account', '0004_auto_20190125_1609'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='libraryuser',
            name='editions',
        ),
        migrations.AddField(
            model_name='libraryuser',
            name='edition',
            field=models.ManyToManyField(related_name='editions', related_query_name='edition', to='schol_library.Edition', verbose_name='издания для библиотекоря'),
        ),
    ]