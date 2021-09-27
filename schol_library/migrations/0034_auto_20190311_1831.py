# Generated by Django 2.1.4 on 2019-03-11 12:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0033_auto_20190311_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schooltitul',
            name='class_teacher',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='классный руководитель'),
        ),
    ]
