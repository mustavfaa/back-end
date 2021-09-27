# Generated by Django 2.2 on 2021-06-08 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfoli', '0013_auto_20210526_0607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='almamater',
            name='image',
            field=models.ImageField(default='nophoto.png', upload_to='usr/2021-06-08/almamater'),
        ),
        migrations.AlterField(
            model_name='aspirantprivate',
            name='image',
            field=models.ImageField(upload_to='usr/2021-06-08/private_docs/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='coursetype',
            name='image',
            field=models.ImageField(null=True, upload_to='usr/common/2021-06-08/coursetype', verbose_name='Scan view'),
        ),
        migrations.AlterField(
            model_name='notificationfile',
            name='file',
            field=models.FileField(upload_to='usr/2021-06-08/notifications'),
        ),
        migrations.AlterField(
            model_name='protocol',
            name='file',
            field=models.FileField(upload_to='usr/2021-06-08/protocol'),
        ),
        migrations.AlterField(
            model_name='registerschool',
            name='image',
            field=models.ImageField(upload_to='usr/2021-06-08/responisble_statement', verbose_name='Приказ'),
        ),
        migrations.AlterField(
            model_name='schooltype',
            name='image',
            field=models.ImageField(default='/static/images/nophoto.png', upload_to='usr/common/2021-06-08/school_types'),
        ),
        migrations.AlterField(
            model_name='testschool',
            name='image',
            field=models.ImageField(default='/static/images/nophoto.png', upload_to='usr/2021-06-08/testalmamater'),
        ),
    ]