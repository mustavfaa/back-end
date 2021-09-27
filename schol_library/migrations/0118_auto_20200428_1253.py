# Generated by Django 2.2 on 2020-04-28 06:53

from django.db import migrations


def kill_reg(apps, sch_editor):
    NumberBooks = apps.get_model('schol_library', 'NumberBooks')
    d = NumberBooks.objects.filter(in_register=False)
    for i in d:
        i.is_record_to_register = True
        print('reg')
        i.save()


class Migration(migrations.Migration):
    dependencies = [
        ('schol_library', '0117_auto_20200428_1251'),
    ]

    operations = [
        migrations.RunPython(kill_reg)
    ]
