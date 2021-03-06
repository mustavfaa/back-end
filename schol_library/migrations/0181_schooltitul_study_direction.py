# Generated by Django 2.2 on 2020-05-27 05:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('schol_library', '0180_remove_schooltitul_study_direction'),
    ]

    operations = [
        migrations.AddField(
            model_name='schooltitul',
            name='study_direction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='schol_library.StudyDirections', verbose_name='направления обучения'),
        ),
    ]
