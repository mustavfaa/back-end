# Generated by Django 2.2 on 2020-05-18 09:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     #   ('portfoli', '0110_auto_20200518_1447'),
        ('schol_library', '0151_auto_20200518_1527'),
    ]

    operations = [
        # migrations.CreateModel(
        #     name='InitialBalance1',
        #     fields=[
        #         ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('deleted', models.BooleanField(default=False, verbose_name='Deleted')),
        #         ('date_added', models.DateTimeField(auto_now_add=True, null=True, verbose_name='date_added')),
        #         ('date_delete', models.DateField(blank=True, null=True, verbose_name='date_delete')),
        #         ('comment', models.CharField(blank=True, default='', max_length=1000, verbose_name='Comment')),
        #         ('exchange', models.BooleanField(default=False)),
        #         ('date', models.DateField(null=True, verbose_name='Дата ввода остатков')),
        #         ('status', models.BooleanField(default=False)),
        #         ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='автор')),
        #         ('school', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='portfoli.AlmaMater', verbose_name='школа')),
        #     ],
        #     options={
        #         'verbose_name': 'начальный остаток',
        #         'verbose_name_plural': 'начальные остатки',
        #     },
        # ),
        # migrations.CreateModel(
        #     name='EditionInitialBalance1',
        #     fields=[
        #         ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('quantity', models.IntegerField(blank=True, default=0, verbose_name='количество')),
        #         ('amount', models.FloatField(blank=True, default=0, verbose_name='сумма')),
        #         ('edition', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='schol_library.Edition', verbose_name='издание')),
        #         ('invoice', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='editions_invoice', to='schol_library.InitialBalance1', verbose_name='Начальный остаток')),
        #     ],
        #     options={
        #         'verbose_name': 'Книги для начальных остатков в издательстве',
        #         'verbose_name_plural': 'Книги для начальных остатковх в издательстве',
        #         'ordering': ['id'],
        #         'unique_together': {('invoice', 'edition')},
        #     },
        # ),
    ]
