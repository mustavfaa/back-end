# Generated by Django 2.2 on 2019-06-17 02:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('schol_library', '0021_editioncomplex'),
    ]

    operations = [
        migrations.AddField(
            model_name='edition',
            name='edition_complex',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='schol_library.EditionComplex'),
        ),
    ]