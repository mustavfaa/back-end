# Generated by Django 2.1.4 on 2019-03-02 08:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schol_library', '0027_auto_20190227_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='schooltitul',
            name='class_teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='классный руководитель'),
        ),
    ]