# Generated by Django 2.2 on 2019-08-07 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0026_auto_20190805_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='provider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='schol_library.Provider'),
        ),
    ]
