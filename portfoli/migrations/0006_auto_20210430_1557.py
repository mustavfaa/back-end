# Generated by Django 2.2 on 2021-04-30 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfoli', '0005_auto_20210430_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='klass',
            name='klass_type',
            field=models.IntegerField(choices=[(2, 'Школьные классы')], default=2),
        ),
    ]
