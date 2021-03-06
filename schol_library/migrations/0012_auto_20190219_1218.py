# Generated by Django 2.1.4 on 2019-02-19 06:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0011_auto_20190201_1508'),
    ]

    operations = [
        migrations.CreateModel(
            name='Liter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False, verbose_name='Deleted')),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True, verbose_name='date_added')),
                ('comment', models.CharField(blank=True, default='', max_length=1000, verbose_name='Comment')),
                ('exchange', models.BooleanField(default=False)),
                ('name_ru', models.CharField(default='', max_length=500)),
                ('name_kk', models.CharField(blank=True, default='', max_length=500)),
                ('name_en', models.CharField(blank=True, default='', max_length=500)),
                ('sort', models.IntegerField(default=500)),
                ('uid', models.CharField(blank=True, default='', max_length=36, null=True)),
                ('name', models.CharField(max_length=3, verbose_name='Литер класса')),
            ],
            options={
                'verbose_name': 'Литер класса',
                'verbose_name_plural': 'Литеры класса',
            },
        ),
        migrations.RemoveField(
            model_name='schooltitul',
            name='liter',
        ),
        migrations.AlterField(
            model_name='schooltitul',
            name='year',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='portfoli.DateObjects', verbose_name='учебный год\u2028'),
        ),
    ]
