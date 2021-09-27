# Generated by Django 2.1.4 on 2019-03-11 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0030_auto_20190311_1544'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authoredition',
            name='name',
        ),
        migrations.RemoveField(
            model_name='publisheredition',
            name='name',
        ),
        migrations.AddField(
            model_name='authoredition',
            name='name_en',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AddField(
            model_name='authoredition',
            name='name_kk',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AddField(
            model_name='authoredition',
            name='name_ru',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='authoredition',
            name='sort',
            field=models.IntegerField(default=500),
        ),
        migrations.AddField(
            model_name='authoredition',
            name='uid',
            field=models.CharField(blank=True, default='', max_length=36, null=True),
        ),
        migrations.AddField(
            model_name='publisheredition',
            name='name_en',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AddField(
            model_name='publisheredition',
            name='name_kk',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AddField(
            model_name='publisheredition',
            name='name_ru',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='publisheredition',
            name='sort',
            field=models.IntegerField(default=500),
        ),
        migrations.AddField(
            model_name='publisheredition',
            name='uid',
            field=models.CharField(blank=True, default='', max_length=36, null=True),
        ),
    ]
