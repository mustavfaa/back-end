# Generated by Django 2.2 on 2020-06-01 05:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('schol_library', '0186_auto_20200601_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='booksmovinghead',
            name='recall',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='schol_library.BooksRecall'),
        ),
    ]
