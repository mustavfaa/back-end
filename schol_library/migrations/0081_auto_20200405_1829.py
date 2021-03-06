# Generated by Django 2.2 on 2020-04-05 12:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    #    ('portfoli', '0090_auto_20200405_1829'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schol_library', '0080_auto_20200108_2123'),
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
                ('date_write', models.DateField(blank=True, null=True, verbose_name='дата на списание')),
                ('footing', models.TextField(null=True, verbose_name='Основание')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('school', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='portfoli.AlmaMater', verbose_name='школа')),
                ('year', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='schol_library.Year')),
            ],
            options={
                'verbose_name': 'Акт на списание',
                'verbose_name_plural': 'Акты на списание',
                'ordering': ['date'],
            },
        ),
        migrations.DeleteModel(
            name='BillingInvoice',
        ),
    ]
