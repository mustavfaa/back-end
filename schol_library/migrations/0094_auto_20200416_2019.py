# Generated by Django 2.2 on 2020-04-16 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0093_auto_20200416_1713'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incomeexpense',
            name='edition',
        ),
        migrations.RemoveField(
            model_name='incomeexpense',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='incomeexpense',
            name='summ',
        ),
    ]
