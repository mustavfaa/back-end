# Generated by Django 2.1.4 on 2019-02-14 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_remove_libraryuser_role'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rolehistory',
            options={'ordering': ['-data_appointment'], 'verbose_name': 'Журнал назначений', 'verbose_name_plural': 'Журналы назначении'},
        ),
    ]