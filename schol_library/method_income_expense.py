from .models import IncomeExpense, ContentType


def del_ie_invoice(invoice):
    for eid in invoice.editioninvoice_set.all():
        try:
            content_type = ContentType.objects.get_for_model(eid)
            obj = IncomeExpense.objects.get(content_type=content_type, object_id=eid.id)
            obj.delete()
        except:
            pass
    invoice.status = False
    invoice.save()
    return invoice


def update_ie_invoice(invoice, user):
    for eid in invoice.editioninvoice_set.all():
        try:
            content_type = ContentType.objects.get_for_model(eid)
            obj = IncomeExpense.objects.get(content_type=content_type, object_id=eid.id)
            obj.delete()
        except:
            pass
    for eid in invoice.editioninvoice_set.all():
        IncomeExpense.objects.create(ie_object=eid,
                                     school_id=user.libraryuser.school.id,
                                     type_of_movement=1,
                                     quantity=eid.quantity,
                                     edition_id=eid.edition.id,
                                     summ=eid.amount,
                                     type=2
                                     )
    invoice.status = True
    invoice.save()
    return invoice


def del_ie_paper_invoice(invoice):
    for eid in invoice.editions_invoice.all():
        try:
            content_type = ContentType.objects.get_for_model(eid)
            obj = IncomeExpense.objects.get(content_type=content_type, object_id=eid.id)
            obj.delete()
        except:
            pass
    invoice.status = False
    invoice.save()
    return invoice


def update_ie_paper_invoice(invoice, user):
    for eid in invoice.editions_invoice.all():
        try:
            content_type = ContentType.objects.get_for_model(eid)
            obj = IncomeExpense.objects.get(content_type=content_type, object_id=eid.id).delete()
            obj.delete()
        except:
            pass
    for eid in invoice.editions_invoice.all():
        IncomeExpense.objects.create(ie_object=eid,
                                     school_id=user.libraryuser.school.id,
                                     type_of_movement=1,
                                     quantity=eid.quantity,
                                     edition_id=eid.edition.id,
                                     summ=eid.amount,
                                     type=2
                                     )
    invoice.status = True
    invoice.save()
    return invoice


def del_edition_act_write(invoice):
    for eid in invoice.editions_invoice.all():
        try:
            content_type = ContentType.objects.get_for_model(eid)
            obj = IncomeExpense.objects.get(content_type=content_type, object_id=eid.id)
            obj.delete()
        except:
            pass
    invoice.status = False
    invoice.save()
    return invoice


def update_edition_act_write(invoice, user):
    for eid in invoice.editions_invoice.all():
        try:
            content_type = ContentType.objects.get_for_model(eid)
            obj = IncomeExpense.objects.get(content_type=content_type, object_id=eid.id)
            obj.delete()
        except:
            pass
    for eid in invoice.editions_invoice.all():
        IncomeExpense.objects.create(ie_object=eid,
                                     school_id=user.libraryuser.school.id,
                                     type_of_movement=-1,
                                     quantity=eid.quantity,
                                     edition_id=eid.edition.id,
                                     summ=eid.amount,
                                     type=3
                                     )
    invoice.status = True
    invoice.save()
    return invoice