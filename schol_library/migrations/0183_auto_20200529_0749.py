# Generated by Django 2.2 on 2020-05-29 01:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0182_booksorder1_booksrecall1_editionbooksorder1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booksrecall',
            name='author',
        ),
        migrations.RemoveField(
            model_name='booksrecall',
            name='edition',
        ),
        migrations.RemoveField(
            model_name='booksrecall',
            name='order',
        ),
        migrations.RemoveField(
            model_name='booksrecall',
            name='school',
        ),
        migrations.RemoveField(
            model_name='editionbooksorder',
            name='edition',
        ),
        migrations.RemoveField(
            model_name='editionbooksorder',
            name='invoice',
        ),
        migrations.DeleteModel(
            name='BooksOrder',
        ),
        migrations.DeleteModel(
            name='BooksRecall',
        ),
        migrations.DeleteModel(
            name='EditionBooksOrder',
        ),
    ]
