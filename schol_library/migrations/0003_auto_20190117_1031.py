# Generated by Django 2.1.4 on 2019-01-17 04:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    #    ('portfoli', '0001_initial'),
        ('schol_library', '0002_numberbooks'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmountBooks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False, verbose_name='Deleted')),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True, verbose_name='date_added')),
                ('comment', models.CharField(blank=True, default='', max_length=1000, verbose_name='Comment')),
                ('exchange', models.BooleanField(default=False)),
                ('on_hands', models.IntegerField(blank=True, verbose_name='на руках')),
                ('in_warehouse', models.IntegerField(blank=True, verbose_name='на складе')),
                ('amount', models.IntegerField(blank=True, verbose_name='общее количество книг в школе')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portfoli.AlmaMater', verbose_name='школа')),
            ],
            options={
                'verbose_name': 'общее количество книг',
                'verbose_name_plural': 'общее количество книг',
            },
        ),
        migrations.AlterModelOptions(
            name='numberbooks',
            options={'verbose_name': 'количество книг изданий', 'verbose_name_plural': 'количество книг изданий'},
        ),
    ]
