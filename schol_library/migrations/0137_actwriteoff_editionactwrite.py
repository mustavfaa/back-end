# Generated by Django 2.2 on 2020-05-15 11:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    #    ('portfoli', '0108_auto_20200515_0814'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schol_library', '0136_auto_20200515_1715'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActWriteOff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False, verbose_name='Deleted')),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True, verbose_name='date_added')),
                ('date_delete', models.DateField(blank=True, null=True, verbose_name='date_delete')),
                ('comment', models.CharField(blank=True, default='', max_length=1000, verbose_name='Comment')),
                ('exchange', models.BooleanField(default=False)),
                ('idx', models.CharField(blank=True, default='Нету номера акта', max_length=300, verbose_name='Номер акта')),
                ('date', models.DateField(auto_now_add=True)),
                ('date_write', models.DateField(blank=True, verbose_name='дата на списание')),
                ('footing', models.TextField(null=True, verbose_name='Основание')),
                ('members_of_commission', models.TextField(null=True, verbose_name='члены комиссии')),
                ('status', models.BooleanField(blank=True, default=False, verbose_name='Статус')),
                ('amount', models.FloatField(blank=True, default=0, verbose_name='Сумма')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('school', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='portfoli.AlmaMater', verbose_name='школа')),
            ],
            options={
                'verbose_name': 'Акт на списание',
                'verbose_name_plural': 'Акты на списание',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='EditionActWrite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Инвентарный номер')),
                ('quantity', models.IntegerField(blank=True, default=0, verbose_name='количество')),
                ('amount', models.FloatField(blank=True, default=0, verbose_name='Сумма')),
                ('has', models.FloatField(blank=True, default=0, verbose_name='Кол ост')),
                ('summ', models.FloatField(blank=True, default=0, verbose_name='Сумма ост')),
                ('price', models.FloatField(blank=True, default=0, verbose_name='Цена')),
                ('income', models.IntegerField(blank=True, default=0, verbose_name='id_прихода')),
                ('income_type', models.IntegerField(blank=True, default=0, verbose_name='id_типа_прихода')),
                ('edition', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='schol_library.Edition', verbose_name='издание')),
                ('invoice', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='editions_invoice', to='schol_library.ActWriteOff', verbose_name='Акт на списание')),
            ],
            options={
                'verbose_name': 'Книга для акта на списание',
                'verbose_name_plural': 'Книги для актов на списание',
                'ordering': ['id'],
                'unique_together': {('invoice', 'edition', 'income', 'income_type')},
            },
        ),
    ]
