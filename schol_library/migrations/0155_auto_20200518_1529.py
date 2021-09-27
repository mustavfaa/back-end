# Generated by Django 2.2 on 2020-05-18 09:29

from django.db import migrations

from django.db import migrations, models
import datetime
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType


def add_initial_balance(apps, sch_editor):
    NumberBooks = apps.get_model('schol_library', 'NumberBooks')
    InitialBalance = apps.get_model('schol_library', 'InitialBalance')
    EditionInitialBalance = apps.get_model('schol_library', 'EditionInitialBalance')
    IncomeExpense = apps.get_model('schol_library', 'IncomeExpense')
    PaperInvoice = apps.get_model('schol_library', 'PaperInvoice')
    AlmaMater = apps.get_model('portfoli', 'AlmaMater')

    schs = NumberBooks.objects.all().exclude(edition=None).exclude(school=None).values_list('school',
                                                                                                            flat=True).distinct()

    sc = AlmaMater.objects.filter(pk__in=schs)
    d = NumberBooks.objects.all()
    for i in sc:
        nb = NumberBooks.objects.filter(school=i).exclude(edition=None)

        ib = InitialBalance()
        date = datetime.datetime.strptime('12/31/19', '%m/%d/%y')
        ib.school = i
        ib.date = date
        ib.status = True
        try:
            ib.author = i.librarian_user.user
        except:
            ib.author_id = 7
        ib.save()
        id_list = nb.values_list('id', flat=True)
        resitr_recs = IncomeExpense.objects.filter(number_book_id__in=id_list).delete()
        for el in nb:
            eib = EditionInitialBalance()
            eib.invoice = ib
            eib.edition = el.edition
            eib.quantity = el.in_warehouse
            eib.amount = el.summ
            eib.save()
            el.deleted = True
            el.save()


        ib.save()
        print(ib)


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0154_editioninitialbalance_initialbalance'),
    ]

    operations = [
        migrations.RunPython(add_initial_balance)
    ]
