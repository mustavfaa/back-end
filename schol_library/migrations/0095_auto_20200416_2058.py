# Generated by Django 2.2 on 2020-04-16 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0094_auto_20200416_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='incomeexpense',
            name='edition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='schol_library.Edition'),
        ),
        migrations.AddField(
            model_name='incomeexpense',
            name='quantity',
            field=models.IntegerField(blank=True, default=0, verbose_name='количество'),
        ),
        migrations.AddField(
            model_name='incomeexpense',
            name='summ',
            field=models.IntegerField(blank=True, default=0, verbose_name='Сумма'),
        ),
    ]
