# Generated by Django 2.2 on 2019-07-30 06:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0024_auto_20190730_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='edition_invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='providers', to='schol_library.EditionInvoice'),
        ),
    ]
