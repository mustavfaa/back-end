# Generated by Django 2.1.4 on 2019-04-08 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0044_liter_sort'),
    ]

    operations = [
        migrations.CreateModel(
            name='SetUMK',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False, verbose_name='Deleted')),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True, verbose_name='date_added')),
                ('comment', models.CharField(blank=True, default='', max_length=1000, verbose_name='Comment')),
                ('exchange', models.BooleanField(default=False)),
                ('amount', models.IntegerField(verbose_name='Количетво')),
                ('edition', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='schol_library.Edition', verbose_name='издание')),
                ('plan_title', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='sets', to='schol_library.PlannedTitle', verbose_name='плановый титул')),
            ],
            options={
                'verbose_name': 'Набор УМК',
                'verbose_name_plural': 'Наборы УМК',
                'ordering': ['plan_title'],
            },
        ),
    ]
