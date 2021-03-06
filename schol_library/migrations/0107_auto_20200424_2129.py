# Generated by Django 2.2 on 2020-04-24 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0106_auto_20200424_1441'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='editionactwrite',
            options={'ordering': ['id'], 'verbose_name': 'Книга для акта на списание', 'verbose_name_plural': 'Книги для актов на списание'},
        ),
        migrations.AddField(
            model_name='numberbooks',
            name='in_register',
            field=models.BooleanField(default=False, editable=False, verbose_name='В регистре'),
        ),
        migrations.AlterField(
            model_name='incomeexpense',
            name='number_book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='schol_library.NumberBooks'),
        ),
    ]
