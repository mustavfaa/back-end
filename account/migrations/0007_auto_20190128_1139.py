# Generated by Django 2.1.4 on 2019-01-28 05:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    #    ('portfoli', '0001_initial'),
        ('account', '0006_auto_20190125_1635'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessToEdit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False, verbose_name='Deleted')),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True, verbose_name='date_added')),
                ('comment', models.CharField(blank=True, default='', max_length=1000, verbose_name='Comment')),
                ('exchange', models.BooleanField(default=False)),
                ('edit_status', models.SmallIntegerField(blank=True, choices=[(0, 'Нет доступа'), (1, 'Есть доступ')], default=0)),
                ('school', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='portfoli.AlmaMater', verbose_name='школа')),
            ],
            options={
                'verbose_name': 'Роль пользователя',
                'verbose_name_plural': 'Роли пользователей',
            },
        ),
        migrations.AlterField(
            model_name='libraryuser',
            name='role',
            field=models.SmallIntegerField(blank=True, choices=[(0, 'Нет роли'), (1, 'Бибилотекарь'), (2, 'Зам директора по учебной работе'), (3, 'Зав библиотеки')], default=0),
        ),
    ]
