# Generated by Django 2.2 on 2020-04-23 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0030_auto_20200423_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesstoedit',
            name='school',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='portfoli.AlmaMater', verbose_name='школа'),
        ),
    ]