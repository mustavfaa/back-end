# Generated by Django 2.2 on 2020-04-07 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0087_auto_20200407_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editionactwrite',
            name='invoice',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='editions_invoice', to='schol_library.ActWriteOff', verbose_name='Акт на списание'),
        ),
        migrations.AlterField(
            model_name='editionpaperinvoice',
            name='invoice',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='editions_invoice', to='schol_library.PaperInvoice', verbose_name='Накладная'),
        ),
        migrations.AlterField(
            model_name='paperinvoice',
            name='date_invoice',
            field=models.DateField(blank=True, null=True, verbose_name='дата счет фактуры'),
        ),
    ]