# Generated by Django 2.2 on 2019-05-02 09:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [

        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schol_library', '0051_auto_20190429_1249'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanEditionTeacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False, verbose_name='Deleted')),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True, verbose_name='date_added')),
                ('comment', models.CharField(blank=True, default='', max_length=1000, verbose_name='Comment')),
                ('exchange', models.BooleanField(default=False)),
                ('quantity', models.SmallIntegerField(default=100, verbose_name='Количество')),
                ('author', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='автор')),
                ('edition', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='schol_library.Edition', verbose_name='Издание')),
                ('school', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='portfoli.AlmaMater', verbose_name='школа')),
            ],
            options={
                'verbose_name': 'Издание для учителей',
                'verbose_name_plural': 'Издания для учителей',
                'ordering': ['edition'],
            },
        ),
        migrations.DeleteModel(
            name='Parameter',
        ),
    ]
