# Generated by Django 2.1.4 on 2019-01-18 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0003_auto_20190117_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='numberbooks',
            name='edition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='schol_library.Edition', verbose_name='издание'),
        ),
        migrations.AlterField(
            model_name='numberbooks',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='portfoli.AlmaMater', verbose_name='школа'),
        ),
    ]