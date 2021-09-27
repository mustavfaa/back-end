# Generated by Django 2.1.4 on 2019-01-25 04:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schol_library', '0006_auto_20190121_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='numberbooks',
            name='it_filled',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='заполнил'),
        ),
    ]