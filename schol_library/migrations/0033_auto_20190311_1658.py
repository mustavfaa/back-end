# Generated by Django 2.1.4 on 2019-03-11 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0032_auto_20190311_1656'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authoredition',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='authoredition',
            name='name_kk',
        ),
        migrations.RemoveField(
            model_name='authoredition',
            name='name_ru',
        ),
        migrations.RemoveField(
            model_name='authoredition',
            name='sort',
        ),
        migrations.RemoveField(
            model_name='authoredition',
            name='uid',
        ),
        migrations.AddField(
            model_name='authoredition',
            name='name',
            field=models.CharField(default='', max_length=150, verbose_name='автор'),
        ),
    ]
