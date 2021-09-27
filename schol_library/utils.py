from django.db.models import F
from schol_library.models import NumberBooks, EditionInvoice, EditionPaperInvoice, RequestEdition, Edition
from portfoli.models import AlmaMater


def all_editions(school):
    eds = list()
    for edition in Edition.objects.all().distinct().order_by('id'):
        # school = AlmaMater.objects.get(pk=109017212)

        # Бумажная наклданая
        es = EditionPaperInvoice.objects.filter(
            invoice__deleted=False,
            invoice__school=school,
            edition=edition).values_list('quantity', flat=True).union(

            # Заявки на получение
            RequestEdition.objects.filter(
                shipper=school, edition=edition).values_list('quantity', flat=True),

            # Началбные книги
            NumberBooks.objects.filter(
                deleted=False, school=school, edition=edition).annotate(
                quantity=F('on_hands') + F('in_warehouse')).values_list('quantity', flat=True),

            # Электронные накладные
            EditionInvoice.objects.filter(
                invoice__deleted=False,
                invoice__school=school,
                edition=edition
            ).values_list('quantity', flat=True)
        )
        ed_p_i = sum(es)
        eds2 = sum(RequestEdition.objects.filter(
            provider=school,
            edition=edition).values_list('quantity'))

        obj = {
            'edition': edition,
            'result': ed_p_i - eds2
        }
        eds.append(obj)
    return eds

