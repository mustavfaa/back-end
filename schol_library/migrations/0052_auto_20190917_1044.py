# Generated by Django 2.2 on 2019-09-17 04:44

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    #    ('portfoli', '0072_auto_20190917_1044'),
        ('schol_library', '0051_auto_20190910_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incomeexpense',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='portfoli.AlmaMater', verbose_name='школа'),
        ),
        migrations.CreateModel(
            name='RequestEdition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False, verbose_name='Deleted')),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True, verbose_name='date_added')),
                ('comment', models.CharField(blank=True, default='', max_length=1000, verbose_name='Comment')),
                ('exchange', models.BooleanField(default=False)),
                ('date_time', models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 17, 10, 44, 15, 93656), verbose_name='время заявки')),
                ('quantity', models.IntegerField(blank=True, default=0, verbose_name='количество')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('edition', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='schol_library.Edition', verbose_name='издание')),
                ('provider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='provider', to='portfoli.AlmaMater', verbose_name='Школа поставщик')),
                ('shipper', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shipper', to='portfoli.AlmaMater', verbose_name='Школа получатель')),
            ],
            options={
                'verbose_name': 'Заявка на перемещение',
                'verbose_name_plural': 'Заявки на перемешение',
                'ordering': ['id'],
                'unique_together': {('shipper', 'edition')},
            },
        ),
    ]
