# Generated by Django 2.1.4 on 2019-01-25 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0007_numberbooks_it_filled'),
    ]

    operations = [
        migrations.AddField(
            model_name='edition',
            name='isbn',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='ISBN код'),
        ),
    ]
