# Generated by Django 2.2 on 2021-04-07 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfoli', '0002_auto_20210407_2143'),
        ('schol_library', '0189_auto_20201025_1236'),
    ]

    operations = [
        migrations.AddField(
            model_name='schooltitulhead',
            name='language',
            field=models.ForeignKey(  null=True, on_delete=django.db.models.deletion.CASCADE, to='portfoli.Language', verbose_name='язык обучения'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schooltitulhead',
            name='liter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schol_library.Liter', verbose_name='Название класса'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schooltitulhead',
            name='students',
            field=models.IntegerField(default=0, verbose_name='количество учащихся'),
        ),
        migrations.AddField(
            model_name='schooltitulhead',
            name='study_direction',
            field=models.ForeignKey(null=True,
                                    on_delete=django.db.models.deletion.CASCADE, to='schol_library.StudyDirections', verbose_name='направления обучения'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='schooltitulhead',
            name='school',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='portfoli.AlmaMater', verbose_name='школа'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='schooltitulhead',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portfoli.DateObjects', verbose_name='Учебный год'),
        ),
    ]
