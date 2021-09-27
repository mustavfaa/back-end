from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from account.models import AccessToEdit
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.base import TemplateView
from django.views import View
from django.utils.decorators import method_decorator

from ekitaphana import settings
from .valid_view import head_librarian, llibrarian_or_head, llibrarian_or_admin
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from django.shortcuts import render
from .models import IncomeExpense, EditionInvoice, Invoice, Provider, Edition, PaperInvoice, EditionPaperInvoice, \
    RequestEdition, \
    CheckidRequestEdition, NumberBooks, IncomeExpense, InitialBalance, EditionInitialBalance, BooksOrder, \
    EditionBooksOrder
from schol_library import models as library_models, permissions as s_permissions
from .serializers import InvoiceSerializers, InitialBalanceSerializers
from rest_framework.response import Response
from rest_framework import status
from schol_library import serializers, models, api_serializers
from portfoli import models as p_models
from django.utils import translation
from django.http import HttpResponse, HttpResponseForbidden
from .api import cached_api
from rest_framework import status
from django.db.models import Value, F, Subquery
from django.core.cache import cache
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils import timezone
from django.db import connection

from ekitaphana.settings import BASE_1C_PATH
# Кабинет Зав.библиотекоря
@method_decorator(user_passes_test(head_librarian, login_url='home:index'), name='dispatch')
class HeadLibrarianView(APIView):
    template_name = 'schol_library/head_librarian/head_librarian3.html'

    def get(self, request):
        access = AccessToEdit.objects.get(school=request.user.libraryuser.school)
        if request.user.groups.filter(id=6).exists() or access.status_12 >= 1:
            context = {}
            if request.GET.get('all'):

                cache_name = 'eds' + str(translation.get_language())
                data = cache.get(cache_name)

                if data is None:
                    data = {}
                    data['books'] = serializers.EditionsSerializerS(
                        Edition.objects.select_related('klass',
                                                       'publisher',
                                                       'subject',
                                                       'language',
                                                       'author',
                                                       'study_direction',
                                                       'publish_date',
                                                       'series_by_year',
                                                       'metodology_complex').filter(deleted=False).order_by('-id',
                                                                                                            'name'),
                        many=True).data
                    data['years'] = serializers.YearSerializers(
                        models.Year.objects.filter(deleted=False).order_by('year'), many=True).data
                    data['authors'] = serializers.AuthorEditionSerializers(
                        models.AuthorEdition.objects.filter(deleted=False).order_by('name').iterator(), many=True).data
                    data['publishers'] = serializers.PublisherEditionSerializers(
                        models.PublisherEdition.objects.filter(deleted=False).order_by(
                            'name_' + str(translation.get_language())), many=True).data
                    data['languages'] = serializers.LangSerializers(
                        p_models.Language.objects.filter(deleted=False).order_by(
                            'name_' + str(translation.get_language())), many=True).data
                    data['klasss'] = serializers.KlassSerializers(p_models.Klass.objects.filter(deleted=False),
                                                                  many=True).data
                    data['subjects'] = serializers.SubjectSerializers(
                        p_models.Subject.objects.filter(deleted=False).order_by(
                            'name_' + str(translation.get_language())), many=True).data
                    data['metodology_complex'] = serializers.MetodologyComplexSerializers(
                        models.UMK.objects.filter(deleted=False).order_by('name_' + str(translation.get_language())),
                        many=True).data
                    data['study_direction'] = serializers.StudyDirectionsSerializer(
                        models.StudyDirections.objects.filter(deleted=False).order_by(
                            'name_' + str(translation.get_language())), many=True).data
                    cache.set(cache_name, data, 2592000)
                data['number_books'] = list(NumberBooks.objects.filter(
                    school=request.user.libraryuser.school).values_list('edition', flat=True))
                if not request.user.groups.filter(id=6).exists():
                    if access.edit_status > 0 and access.status_12 > 0:
                        data['warning'] = False
                    else:
                        data['warning'] = True
                else:
                    data['warning'] = False
                return Response(data, status=status.HTTP_200_OK)
            elif request.GET.get('number_books'):
                data = api_serializers.NumberBooksLibrianGetSerializer(NumberBooks.objects.filter(
                    school=request.user.libraryuser.school), many=True).data
                return Response(data, status=status.HTTP_200_OK)
            return render(request, template_name=self.template_name, context=context)
        return redirect('account:dashboard')

    def post(self, request, format=None):
        access = AccessToEdit.objects.get(school=request.user.libraryuser.school)
        if request.user.groups.filter(id=6).exists() or access.edit_status == 1 and access.status_12 == 1:

            if 'add' in request.data and 'book' in request.data:
                data_p = request.data['book']
                data_p['school'] = request.user.libraryuser.school.id
                data_p['it_filled'] = request.user.id

                serializer = serializers.NumberBooksSerializerS(data=data_p)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status.HTTP_200_OK)
                else:
                    print(serializer.error_messages, serializer.errors)
                    return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)


@method_decorator(user_passes_test(head_librarian, login_url='home:index'), name='dispatch')
class HeadEditLibrarianView(TemplateView):
    template_name = 'schol_library/head_librarian/edit_head_librarian.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.groups.filter(id=6).exists():
            try:
                AccessToEdit.objects.get(school=self.request.user.libraryuser.school, edit_status=1, status_12=1)
                return context
            except AccessToEdit.DoesNotExist:
                # messages.error(self.request, 'У вас нет доступа!')
                return redirect('account:dashboard')


# Кабинет Зав.библиотекоря: Высталвение ролей для зам.директора по учебоной работе
@method_decorator(user_passes_test(head_librarian, login_url='home:index'), name='dispatch')
class RoleAssignment(TemplateView, View):
    template_name = 'schol_library/head_librarian/role_assignment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.groups.filter(id=6).exists():
            try:
                AccessToEdit.objects.get(school=self.request.user.libraryuser.school, edit_status=1)
                return context
            except AccessToEdit.DoesNotExist:
                messages.error(self.request, 'У вас нет доступа!')
            return context


# Кабинет Зав директора просморт титул школы
@method_decorator(user_passes_test(llibrarian_or_head, login_url='home:index'), name='dispatch')
class HeadOfScienceView(TemplateView):
    template_name = 'schol_library/head_science/head_science.html'


@method_decorator(user_passes_test(llibrarian_or_head, login_url='home:index'), name='dispatch')
class Invoices(TemplateView):
    template_name = "schol_library/head_librarian/invoices.html"


@method_decorator(user_passes_test(llibrarian_or_head, login_url='home:index'), name='dispatch')
class InvoiceView(APIView):

    def post(self, request, format=None):

        if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                school_id=request.user.libraryuser.school.id, edit_status=1).exists():
            if request.data.get('power_of_attorney'):
                if serializers.NumberProvider(data=request.data).is_valid():
                    try:
                        invoice = Invoice.objects.get(pk=request.data['id'], school=request.user.libraryuser.school)
                        invoice.power_of_attorney = request.data.get('power_of_attorney')
                        invoice.save()
                        return Response(status=status.HTTP_201_CREATED)
                    except:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                return Response(status=status.HTTP_400_BAD_REQUEST)

            elif 'confidant' in request.data:
                data = {}
                data['confidant'] = request.data.get('confidant')
                try:
                    invoice = Invoice.objects.get(pk=request.data['id'], school=request.user.libraryuser.school)
                    confidant = serializers.ValidateConfidante(invoice, data=data)
                    if confidant.is_valid():
                        confidant.save()
                        return Response(status=status.HTTP_201_CREATED)
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            elif 'freight_carrier' in request.data:
                data = {}
                data['freight_carrier'] = request.data.get('freight_carrier')
                try:
                    invoice = Invoice.objects.get(
                        id=request.data.get('invoice'),
                        school=request.user.libraryuser.school)
                    freight_carrier = serializers.ValidateFreightCarrier(invoice, data=data)
                    if freight_carrier.is_valid():
                        freight_carrier.save()
                        return Response(status=status.HTTP_201_CREATED)
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            elif request.data.get('date_extracts'):
                if serializers.ValidateDateExtracts(data=request.data).is_valid():
                    try:
                        invoice = Invoice.objects.get(pk=request.data['id'], school=request.user.libraryuser.school)
                        invoice.date_extracts = request.data.get('date_extracts')
                        invoice.save()
                        return Response(status=status.HTTP_201_CREATED)
                    except:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                return Response(status=status.HTTP_400_BAD_REQUEST)

            elif request.data.get('date_power_of_attorney'):
                if serializers.ValidateDatePowerOfAttorney(data=request.data).is_valid():
                    try:
                        invoice = Invoice.objects.get(pk=request.data['id'], school=request.user.libraryuser.school)
                        invoice.date_power_of_attorney = request.data.get('date_power_of_attorney')
                        invoice.save()
                        return Response(status=status.HTTP_201_CREATED)
                    except:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                return Response(status=status.HTTP_400_BAD_REQUEST)

            elif request.data.get('number'):
                if serializers.ValidateNumber(data=request.data).is_valid():
                    try:
                        invoice = Invoice.objects.get(pk=request.data['id'], school=request.user.libraryuser.school)
                        invoice.number = request.data.get('number')
                        invoice.save()
                        return Response(status=status.HTTP_201_CREATED)
                    except:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                return Response(status=status.HTTP_400_BAD_REQUEST)

            elif request.data.get('ready'):

                invoice = Invoice.objects.get(pk=request.data.get('ready'))
                if invoice.school.id == request.user.libraryuser.school.id:
                    if 'status_r' in request.data or request.data.get('status_r'):
                        serializer = serializers.InvoiceSerializers(invoice).data
                        return Response(serializer, status=status.HTTP_200_OK)
                    else:
                        serializer = serializers.InvoiceSerializers(invoice).data
                        return Response(serializer, status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                eid = EditionInvoice.objects.get(pk=request.data['id'])
                if eid.invoice.school == request.user.libraryuser.school:
                    eid.quantity = int(request.data['quantity'])
                    eid.save()
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def get(self, request):
        context = {}

        if request.GET.get('all_invoices'):
            context['invoices'] = InvoiceSerializers(
                Invoice.objects.filter(school=request.user.libraryuser.school).order_by('-id'), many=True).data
            context['languages'] = serializers.LanguageSerializer(
                p_models.Language.objects.filter(deleted=False).order_by('name_' + translation.get_language()),
                many=True).data
            context['klasses'] = serializers.KlassSerializersID(p_models.Klass.objects.filter(deleted=False),
                                                                many=True).data
            context['providers'] = serializers.ProviderSerializers(Provider.objects.filter(deleted=False),
                                                                   many=True).data
            return Response(data=context)

        elif request.GET.get('e_invoices'):

            wtls = p_models.PortfolioWorkTimeLine.objects.filter(school=request.user.libraryuser.school,
                                                                 uvolen=False,
                                                                 current=True,
                                                                 deleted=False).values_list('portfolio', flat=True)

            context['portfolios'] = serializers.PortfolioMSerializers(p_models.Portfolio.objects.filter(pk__in=wtls),
                                                                      many=True).data
            invoice = Invoice.objects.get(pk=request.GET.get('e_invoices'), school=request.user.libraryuser.school)
            context['invoice'] = InvoiceSerializers(invoice).data
            ed = Edition.objects.filter(publisher=invoice.publisher)
            context['customer'] = serializers.ProviderSerializers(Provider.objects.get(id=1)).data
            context['editions'] = serializers.EditionSerializerA(ed, many=True).data
            context['subjects'] = serializers.SubjectSerializers(
                p_models.Subject.objects.filter(id__in=ed.values_list('subject', flat=True)), many=True).data
            return Response(data=context)
        elif request.GET.get('pdf_invoice'):
            import httplib2
            h = httplib2.Http()

            AUTH = 'cmVwb3J0ZXI6bXg1XiM1'
            HEADERS = {
                'Authorization': 'Basic ' + AUTH
            }
            a, b = h.request(
                uri=BASE_1C_PATH+"/eponortfoliohz/hs/otchet/get_otchet/?invoice=" + request.GET['pdf_invoice'],
                method="GET",
                headers=HEADERS,
            )
            return HttpResponse(b,
                                content_type='application/pdf')
        else:
            template_name = 'schol_library/head_librarian/invoice.html'
            return render(request, template_name=template_name, context=context)


@method_decorator(user_passes_test(llibrarian_or_admin, login_url='home:index'), name='dispatch')
class PaperInvoiceView(APIView):

    def get(self, request):
        context = {}

        if request.GET.get('all_invoices'):
            # context = cached_api(lang=translation.get_language())
            invoices_objects = PaperInvoice.objects.filter(school=request.user.libraryuser.school).select_related(
                'author').order_by('-id')
            for obj in invoices_objects:
                obj.author_fio = obj.author.get_full_name()
            context['invoices'] = serializers.PaperInvoiceSerializersForNewFront(invoices_objects
                                                                                 , many=True).data
            return Response(data=context)

        elif request.GET.get('e_invoices'):
            invoice = PaperInvoice.objects.get(pk=request.GET.get('e_invoices'))
            invoice.author_fio = invoice.author.get_full_name()
            acces = AccessToEdit.objects.filter(
                school_id=request.user.libraryuser.school.id)[0]
            if acces.date_invoice > invoice.date:
                invoice.editable = False
            context['invoice'] = serializers.PaperInvoiceSerializers(invoice).data
            # context['editions'] = serializers.EditionSerializerA(
            #     Edition.objects.filter(id__in=Subquery(editions_id)), many=True).data
            return Response(data=context)
        else:
            template_name = 'schol_library/head_librarian/paper_invoice.html'
            return render(request, template_name=template_name, context=context)

    # Пост запросы
    def post(self, request, format=None):
        acces = AccessToEdit.objects.filter(
            school_id=request.user.libraryuser.school.id)[0]

        if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                school_id=request.user.libraryuser.school.id, edit_status=1).exists():

            if 'deleted' in request.data:
                if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                        school_id=request.user.libraryuser.school.id, edit_status=1).exists():
                    invoice = PaperInvoice.objects.get(pk=request.data['deleted'],
                                                       school=request.user.libraryuser.school)
                    if acces.date_invoice > invoice.date:
                        return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                        status=status.HTTP_403_FORBIDDEN)
                    invoice.deleted = True
                    invoice.save()
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            elif 'create_i' in request.data:
                data = request.data['create_i']
                if str(acces.date_invoice) > data['date']:
                    return Response({'errors': 'Запрещено создавать документ в закрытом периоде'},
                                    status=status.HTTP_403_FORBIDDEN)
                data['author'] = request.user.id
                data['school'] = request.user.libraryuser.school.id
                serializer = serializers.PaperInvoiceSerializerPost(data=data)
                if serializer.is_valid():
                    serializer.save()
                    s = serializer.data
                    s['sum'] = 0
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                error = {
                    'errors': serializer.errors.values()
                }
                return Response(error)

            elif 'create_edition_invoice' in request.data or request.data.get('create_edition_invoice'):
                serializer = serializers.PostEditionPaperInvoiceSerializers(data=request.data['create_edition_invoice'])
                context = {}
                if serializer.is_valid():
                    serializer.save()
                    context['ei'] = serializer.data
                    context['invoice'] = serializers.PaperInvoiceSerializers(
                        PaperInvoice.objects.get(pk=context['ei']['invoice'],
                                                 school=request.user.libraryuser.school)).data
                    return Response(context, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            elif request.data.get('ready'):
                invoice = PaperInvoice.objects.get(pk=request.data.get('ready'),
                                                   school=request.user.libraryuser.school)
                if invoice.school.id == request.user.libraryuser.school.id:

                    if request.data.get('status_r'):
                        invoice_data = request.data.get('invoice')
                        if acces.date_invoice > invoice.date:
                            return Response({'errors': 'Запрещено создавать документ в закрытом периоде'},
                                            status=status.HTTP_403_FORBIDDEN)
                        invoice_data['school'] = invoice.school.id
                        invoice_data['author'] = request.user.id
                        invoice_data['status'] = False
                        serializer = serializers.PaperInvoiceSerializerPost(
                            invoice, data=invoice_data)
                        if serializer.is_valid():
                            serializer.save()
                            # del_ie_paper_invoice(invoice=invoice)
                            return Response(serializer.data, status=status.HTTP_200_OK)
                        error = {
                            'errors': serializer.errors.values()
                        }
                        return Response(error)
                    else:
                        invoice_data = request.data.get('invoice')
                        if acces.date_invoice > invoice.date:
                            return Response({'errors': 'Запрещено создавать документ в закрытом периоде'},
                                            status=status.HTTP_403_FORBIDDEN)
                        invoice_data['school'] = invoice.school.id
                        invoice_data['author'] = request.user.id
                        invoice_data['status'] = True
                        serializer = serializers.PaperInvoiceSerializerPost(
                            invoice, data=invoice_data)
                        if serializer.is_valid():
                            serializer.save()
                            # update_ie_paper_invoice(invoice=invoice, user=request.user)
                            return Response(serializer.data, status=status.HTTP_200_OK)
                        error = {
                            'errors': serializer.errors.values()
                        }
                        return Response(error)

                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)

            if request.data.get('quantity'):
                try:
                    eid = EditionPaperInvoice.objects.get(pk=request.data['id'])
                    if not eid.invoice.status:

                        if eid.invoice.school == request.user.libraryuser.school:
                            eid.quantity = int(request.data['quantity'])
                            eid.save()
                            return Response(status=status.HTTP_201_CREATED)
                        else:
                            return Response(status=status.HTTP_404_NOT_FOUND)
                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            if request.data.get('delete_e') or 'delete_e' in request.data:
                error = {
                    'err': "Error"
                }
                try:
                    de = EditionPaperInvoice.objects.get(id=int(request.data.get('delete_e')))
                    if de.invoice.school == request.user.libraryuser.school:
                        de.delete()
                        return Response({'id': request.data.get('delete_e')}, status=status.HTTP_200_OK)
                    else:
                        return Response(error, status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)

            if request.data.get('amount'):
                try:
                    eid = EditionPaperInvoice.objects.get(pk=request.data['id'])
                    if eid.invoice.school == request.user.libraryuser.school and not eid.invoice.status:
                        eid.amount = int(request.data['amount'])
                        eid.save()
                        return Response(status=status.HTTP_201_CREATED)
                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                eid = EditionPaperInvoice.objects.get(pk=request.data['id'])
                if eid.invoice.school == request.user.libraryuser.school:
                    eid.quantity = int(request.data['quantity'])
                    eid.save()
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, format=None):
        error = {
            'err': "Error"
        }
        if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                school_id=request.user.libraryuser.school.id, edit_status=1).exists():
            try:
                context = {}
                de = EditionPaperInvoice.objects.get(id=int(request.GET.get('e_invoices')))
                if de.invoice.school == request.user.libraryuser.school:
                    de.delete()
                    context['ei'] = serializers.PaperInvoiceSerializers(de.invoice).data
                    return Response(data=context, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(user_passes_test(llibrarian_or_admin, login_url='home:index'), name='dispatch')
class InitialBalanceView(APIView):

    def get(self, request):
        context = {}

        if request.GET.get('all_invoices'):
            ib_objects = InitialBalance.objects.filter(
                school=request.user.libraryuser.school).select_related('author').order_by('-id')
            for obj in ib_objects:
                obj.author_fio = obj.author.get_full_name()
            context['invoices'] = serializers.NewInitialBalanceSerializers(
                ib_objects, many=True).data
            return Response(data=context)

        elif request.GET.get('e_invoices'):
            invoice = InitialBalance.objects.get(pk=request.GET.get('e_invoices'))
            invoice.author_fio = invoice.author.get_full_name()
            acces = AccessToEdit.objects.filter(
                school_id=request.user.libraryuser.school.id)[0]
            if acces.date_invoice > invoice.date:
                invoice.editable = False

            context['invoice'] = serializers.InitialBalanceSerializers(invoice).data
            return Response(data=context)
        else:
            template_name = 'schol_library/head_librarian/paper_invoice.html'
            return render(request, template_name=template_name, context=context)

    # Пост запросы
    def post(self, request, format=None):
        acces = AccessToEdit.objects.filter(
            school_id=request.user.libraryuser.school.id)[0]

        if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                school_id=request.user.libraryuser.school.id, edit_status=1).exists():

            if 'deleted' in request.data:
                if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                        school_id=request.user.libraryuser.school.id, edit_status=1).exists():
                    invoice = InitialBalance.objects.get(pk=request.data['deleted'],
                                                         school=request.user.libraryuser.school)
                    if acces.date_invoice > invoice.date:
                        return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                        status=status.HTTP_403_FORBIDDEN)
                    invoice.deleted = True
                    invoice.save()
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            elif 'create_i' in request.data:
                data = request.data['create_i']
                if str(acces.date_invoice) > data['date']:
                    return Response({'errors': 'Запрещено создавать документ в закрытом периоде'},
                                    status=status.HTTP_403_FORBIDDEN)
                data['author'] = request.user.id
                data['school'] = request.user.libraryuser.school.id
                serializer = serializers.InitialBalanceSerializerPost(data=data)
                if serializer.is_valid():
                    serializer.save()
                    s = serializer.data
                    s['sum'] = 0
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                error = {
                    'errors': serializer.errors.values()
                }
                return Response(error)

            elif 'create_edition_invoice' in request.data or request.data.get('create_edition_invoice'):
                serializer = serializers.PostEditionInitialbalanceSerializers(
                    data=request.data['create_edition_invoice'])
                context = {}
                if serializer.is_valid():
                    serializer.save()
                    context['ei'] = serializer.data
                    context['invoice'] = serializers.InitialBalanceSerializers(
                        InitialBalance.objects.get(pk=context['ei']['invoice'],
                                                   school=request.user.libraryuser.school)).data
                    return Response(context, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            elif request.data.get('ready'):
                invoice = InitialBalance.objects.get(pk=request.data.get('ready'),
                                                     school=request.user.libraryuser.school)
                if invoice.school.id == request.user.libraryuser.school.id:

                    if request.data.get('status_r'):
                        invoice_data = request.data.get('invoice')
                        if acces.date_invoice > invoice.date:
                            return Response({'errors': 'Запрещено создавать документ в закрытом периоде'},
                                            status=status.HTTP_403_FORBIDDEN)
                        invoice_data['school'] = invoice.school.id
                        invoice_data['author'] = request.user.id
                        invoice_data['status'] = False
                        serializer = serializers.InitialBalanceSerializerPost(
                            invoice, data=invoice_data)
                        if serializer.is_valid():
                            serializer.save()
                            # del_ie_paper_invoice(invoice=invoice)
                            return Response(serializer.data, status=status.HTTP_200_OK)
                        error = {
                            'errors': serializer.errors.values()
                        }
                        return Response(error)
                    else:
                        invoice_data = request.data.get('invoice')
                        if acces.date_invoice > invoice.date:
                            return Response({'errors': 'Запрещено создавать документ в закрытом периоде'},
                                            status=status.HTTP_403_FORBIDDEN)
                        invoice_data['school'] = invoice.school.id
                        invoice_data['author'] = request.user.id
                        invoice_data['status'] = True
                        serializer = serializers.InitialBalanceSerializerPost(
                            invoice, data=invoice_data)
                        if serializer.is_valid():
                            serializer.save()
                            # update_ie_paper_invoice(invoice=invoice, user=request.user)
                            return Response(serializer.data, status=status.HTTP_200_OK)
                        error = {
                            'errors': serializer.errors.values()
                        }
                        return Response(error)

                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)

            if request.data.get('quantity'):
                try:
                    eid = EditionInitialBalance.objects.get(pk=request.data['id'])
                    if not eid.invoice.status:
                        if eid.invoice.school == request.user.libraryuser.school:
                            eid.quantity = int(request.data['quantity'])
                            eid.save()
                            return Response(status=status.HTTP_201_CREATED)
                        else:
                            return Response(status=status.HTTP_404_NOT_FOUND)
                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            if request.data.get('delete_e') or 'delete_e' in request.data:
                error = {
                    'err': "Error"
                }
                try:
                    de = EditionInitialBalance.objects.get(id=int(request.data.get('delete_e')))
                    if de.invoice.school == request.user.libraryuser.school:
                        de.delete()
                        return Response({'id': request.data.get('delete_e')}, status=status.HTTP_200_OK)
                    else:
                        return Response(error, status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)

            if request.data.get('amount'):
                try:
                    eid = EditionInitialBalance.objects.get(pk=request.data['id'])
                    if eid.invoice.school == request.user.libraryuser.school and not eid.invoice.status:
                        eid.amount = int(request.data['amount'])
                        eid.save()
                        return Response(status=status.HTTP_201_CREATED)
                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                eid = EditionInitialBalance.objects.get(pk=request.data['id'])
                if eid.invoice.school == request.user.libraryuser.school:
                    eid.quantity = int(request.data['quantity'])
                    eid.save()
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, format=None):
        error = {
            'err': "Error"
        }
        if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                school_id=request.user.libraryuser.school.id, edit_status=1).exists():
            try:
                context = {}
                de = EditionPaperInvoice.objects.get(id=int(request.GET.get('e_invoices')))
                if de.invoice.school == request.user.libraryuser.school:
                    de.delete()
                    context['ei'] = serializers.InitialBalanceSerializers(de.invoice).data
                    return Response(data=context, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


class BooksOrderView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated | s_permissions.HeadlibrianPermission]

    def get(self, request):
        context = {}

        if request.GET.get('all_invoices'):
            # context = cached_api(lang=translation.get_language())
            bo_objects = BooksOrder.objects.filter(
                school=request.user.libraryuser.school
            ).select_related('author').order_by('-id')
            for obj in bo_objects:
                obj.author_fio = obj.author.get_full_name()
            context['invoices'] = serializers.OrderBooksSerializers(bo_objects, many=True).data
            return Response(data=context)

        elif request.GET.get('e_invoices'):
            invoice = BooksOrder.objects.get(pk=request.GET.get('e_invoices'),
                                             school=request.user.libraryuser.school)
            invoice.author_fio = invoice.author.get_full_name()
            acces = AccessToEdit.objects.filter(
                school_id=request.user.libraryuser.school.id)[0]
            if acces.date_invoice > invoice.date:
                invoice.editable = False

            context['invoice'] = serializers.OrderBooksSerializers(invoice).data
            return Response(data=context)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # Пост запросы
    def post(self, request, format=None):
        acces = AccessToEdit.objects.filter(
            school_id=request.user.libraryuser.school.id)[0]

        if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                school_id=request.user.libraryuser.school.id, edit_status=1).exists():

            if 'deleted' in request.data:
                if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                        school_id=request.user.libraryuser.school.id, edit_status=1).exists():
                    invoice = BooksOrder.objects.get(pk=request.data['deleted'],
                                                     school=request.user.libraryuser.school)
                    if acces.date_invoice > invoice.date:
                        return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                        status=status.HTTP_403_FORBIDDEN)
                    invoice.deleted = request.data['set_status']
                    invoice.save()
                    invoice.author_fio = invoice.author.get_full_name()
                    acces = AccessToEdit.objects.filter(
                        school_id=request.user.libraryuser.school.id)[0]
                    if acces.date_invoice > invoice.date:
                        invoice.editable = False
                    data = {}
                    data['invoice'] = serializers.OrderBooksSerializers(invoice).data
                    return Response(data, status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            elif 'create_i' in request.data:
                data = request.data['create_i']
                if str(acces.date_invoice) > data['date']:
                    return Response({'errors': 'Запрещено создавать документ в закрытом периоде'},
                                    status=status.HTTP_403_FORBIDDEN)
                data['author'] = request.user.id
                data['school'] = request.user.libraryuser.school.id
                serializer = serializers.BooksOrderSerializerPost(data=data)
                if serializer.is_valid():
                    serializer.save()

                    serializer.instance.editions_invoice.all().delete()

                    for item in serializer.initial_data['editions_val']:
                        serializer.instance.editions_invoice.create(edition_id=item['editionId'],
                                                                    quantity=float(item['quantity']))

                    s = serializer.data
                    invoice = models.BooksOrder.objects.get(pk=s['id'])
                    if acces.date_invoice > invoice.date:
                        invoice.editable = False
                    invoice.author_fio = invoice.author.get_full_name()
                    ret_data = serializers.OrderBooksSerializers(invoice).data
                    s['sum'] = 0
                    return Response(ret_data, status=status.HTTP_201_CREATED)
                error = {
                    'errors': serializer.errors.values()
                }
                return Response(error)

            if request.data.get('quantity'):
                try:
                    eid = EditionBooksOrder.objects.get(pk=request.data['id'])

                    if eid.invoice.school == request.user.libraryuser.school:
                        eid.quantity = int(request.data['quantity'])
                        eid.save()
                        return Response(status=status.HTTP_201_CREATED)
                    else:
                        return Response(status=status.HTTP_404_NOT_FOUND)
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            if request.data.get('delete_e') or 'delete_e' in request.data:
                error = {
                    'err': "Error"
                }
                try:
                    de = EditionBooksOrder.objects.get(id=int(request.data.get('delete_e')))
                    if de.invoice.school == request.user.libraryuser.school:
                        de.delete()
                        return Response({'id': request.data.get('delete_e')}, status=status.HTTP_200_OK)
                    else:
                        return Response(error, status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)

            elif request.data.get('ready'):
                invoice = BooksOrder.objects.get(pk=request.data.get('ready'))
                if invoice.school.id == request.user.libraryuser.school.id:
                    if request.data.get('status_r'):
                        invoice_data = request.data.get('invoice')
                        if acces.date_invoice > invoice.date:
                            return Response({'errors': 'Запрещено создавать документ в закрытом периоде'},
                                            status=status.HTTP_403_FORBIDDEN)
                        invoice_data['school'] = invoice.school.id
                        invoice_data['author'] = request.user.id
                        invoice_data['status'] = False
                        serializer = serializers.BooksOrderSerializerPost(invoice, data=invoice_data)
                        if serializer.is_valid():
                            serializer.save()
                            serializer.instance.editions_invoice.all().delete()

                            for item in serializer.initial_data['editions_val']:
                                serializer.instance.editions_invoice.create(edition_id=item['editionId'],
                                                                            quantity=float(item['quantity']))
                            if acces.date_invoice > invoice.date:
                                invoice.editable = False
                            invoice.author_fio = invoice.author.get_full_name()
                            ret_data = serializers.OrderBooksSerializers(invoice).data
                            return Response(ret_data, status=status.HTTP_200_OK)
                        error = {
                            'errors': serializer.errors.values()
                        }
                        return Response(error)
                    else:
                        invoice_data = request.data.get('invoice')
                        if acces.date_invoice > invoice.date:
                            return Response({'errors': 'Запрещено создавать документ в закрытом периоде'},
                                            status=status.HTTP_403_FORBIDDEN)
                        invoice_data['school'] = invoice.school.id
                        invoice_data['author'] = request.user.id
                        invoice_data['status'] = True
                        serializer = serializers.BooksOrderSerializerPost(invoice, data=invoice_data)
                        if serializer.is_valid():
                            serializer.save()

                            serializer.instance.editions_invoice.all().delete()

                            for item in serializer.initial_data['editions_val']:
                                serializer.instance.editions_invoice.create(edition_id=item['editionId'],
                                                                            quantity=float(item['quantity']))
                            serializer.save()
                            if acces.date_invoice > invoice.date:
                                invoice.editable = False
                            invoice.author_fio = invoice.author.get_full_name()
                            ret_data = serializers.OrderBooksSerializers(invoice).data
                            return Response(ret_data, status=status.HTTP_200_OK)
                        error = {
                            'errors': serializer.errors.values()
                        }
                        return Response(error)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)

            try:
                eid = EditionBooksOrder.objects.get(pk=request.data['id'])
                if eid.invoice.school == request.user.libraryuser.school:
                    eid.quantity = int(request.data['quantity'])
                    eid.save()
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, format=None):
        error = {
            'err': "Error"
        }
        if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                school_id=request.user.libraryuser.school.id, edit_status=1).exists():
            try:
                context = {}
                de = EditionBooksOrder.objects.get(id=int(request.GET.get('e_invoices')))
                if de.invoice.school == request.user.libraryuser.school:
                    de.delete()
                    context['ei'] = serializers.OrderBooksSerializers(de.invoice).data
                    return Response(data=context, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(user_passes_test(llibrarian_or_head, login_url='home:index'), name='dispatch')
class RequestEditionView(APIView):

    def get(self, request):
        context = {}
        if request.GET.get('all_edition'):
            context = cached_api(lang=translation.get_language())
            context['languages'] = serializers.LanguageSerializer(
                p_models.Language.objects.filter(deleted=False).order_by('name_' + translation.get_language()),
                many=True).data
            context['klasses'] = serializers.KlassSerializersID(p_models.Klass.objects.filter(deleted=False),
                                                                many=True).data
            context['my_request_edition'] = serializers.RequestEditionSerializerGet(
                RequestEdition.objects.filter(shipper_id=request.user.libraryuser.school.id, checkid=False), many=True
            ).data
            checkid_id_list = CheckidRequestEdition.objects.filter(
                school_id=request.user.libraryuser.school.id).values_list('id', flat=True)
            r1 = RequestEdition.objects.filter(
                shipper_id=request.user.libraryuser.school.id).values_list('id', flat=True).distinct()
            r2 = RequestEdition.objects.filter(
                checkidrequestedition__in=checkid_id_list).values_list('id', flat=True).distinct()
            sr = r1 | r2
            request_edition = RequestEdition.objects.filter(checkid=False).exclude(id__in=sr).count()
            context['count2'] = request_edition
            context['count3'] = CheckidRequestEdition.objects.filter(
                school_id=request.user.libraryuser.school.id, check2=False).count()
            return Response(data=context)

        if request.GET.get("get_edition_r"):
            checkid_id_list = CheckidRequestEdition.objects.filter(
                school_id=request.user.libraryuser.school.id).values_list('id', flat=True)
            r1 = RequestEdition.objects.filter(
                shipper_id=request.user.libraryuser.school.id).values_list('id', flat=True).distinct()
            r2 = RequestEdition.objects.filter(
                checkidrequestedition__in=checkid_id_list).values_list('id', flat=True).distinct()
            sr = r1 | r2
            request_edition = RequestEdition.objects.filter(checkid=False).exclude(id__in=sr)
            data = serializers.RequestEditionSerializerGet(request_edition, many=True).data
            return Response(data=data, status=status.HTTP_200_OK)

        if request.GET.get("get_my_checkid"):
            get_my_checkid = CheckidRequestEdition.objects.filter(
                school_id=request.user.libraryuser.school.id, check2=False)
            data = serializers.CheckidRequestEditionS3(get_my_checkid, many=True).data
            return Response(data=data, status=status.HTTP_200_OK)

        else:
            template_name = 'schol_library/head_librarian/request_edition.html'
            return render(request, template_name=template_name, context=context)

    def post(self, request, format=None):
        acces = AccessToEdit.objects.filter(
            school_id=request.user.libraryuser.school.id)[0]
        if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                school_id=request.user.libraryuser.school.id, edit_status=1).exists():
            if 'add_request_edition' in request.data or request.data.get('add_request_edition'):
                data = request.data.get('add_request_edition')
                data['shipper'] = request.user.libraryuser.school.id
                data['author'] = request.user.id
                serializer = serializers.RequestEditionSerializerPost(data=data)
                if serializer.is_valid():
                    serializer.save()
                    serializer = serializers.RequestEditionSerializerGet(
                        RequestEdition.objects.get(id=serializer.data['id']))
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response({'error': serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)

            if 'this_request' in request.data and request.data.get("this_request"):
                try:
                    v = CheckidRequestEdition.objects.get(id=request.data.get("this_request"))
                    q_value = v.request_edition.quantity - v.quantity
                    if q_value > 0:
                        RequestEdition.objects.create(
                            edition=v.request_edition.edition,
                            shipper=v.request_edition.shipper,
                            provider=v.request_edition.provider,
                            author=v.request_edition.author,
                            date_time=v.request_edition.date_time,
                            checkid=v.request_edition.checkid,
                            quantity=q_value
                        )

                    obj = RequestEdition.objects.get(id=v.request_edition.id)

                    IncomeExpense.objects.create(
                        ie_object=obj,
                        school_id=obj.shipper.id,
                        type_of_movement=1,
                        quantity=v.quantity,
                        edition_id=obj.edition.id)

                    IncomeExpense.objects.create(
                        ie_object=obj,
                        school_id=v.school.id,
                        type_of_movement=-1,
                        quantity=v.quantity,
                        edition_id=obj.edition.id)

                    v.request_edition.quantity = v.quantity
                    v.check2 = True
                    v.save()
                    v2 = v.request_edition
                    v2.provider = v.school
                    v2.save()
                    v = serializers.RequestEditionSerializerGet(
                        RequestEdition.objects.filter(shipper_id=request.user.libraryuser.school.id), many=True).data
                    return Response(v, status=status.HTTP_201_CREATED)
                except:
                    return Response({'error': 'error'}, status=status.HTTP_400_BAD_REQUEST)

            if 'add_request' in request.data or request.data.get('add_request'):
                data = request.data.get('add_request')
                data['school'] = request.user.libraryuser.school.id
                data['author'] = request.user.id
                v = serializers.CheckidRequestEditionS2(data=data)
                if v.is_valid():
                    v.save()
                    sv = serializers.CheckidRequestEditionS(CheckidRequestEdition.objects.get(id=v.data['id']))
                    return Response(sv.data, status=status.HTTP_201_CREATED)
                return Response({'error': v.error_messages}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, format=None):
        error = {
            'err': "Error"
        }
        if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                school_id=request.user.libraryuser.school.id, edit_status=1).exists():
            if request.GET.get('my_check_del'):
                try:
                    de = CheckidRequestEdition.objects.get(id=int(request.GET.get('my_check_del')))
                    de.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                except:
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)

            try:
                de = EditionPaperInvoice.objects.get(id=int(request.GET.get('e_invoices')))
                if de.invoice.school == request.user.libraryuser.school:
                    de.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def get_counts_from_registry(school=None, edition=[]):
    query_text = """
    select edition_id as edition,
       income,
       income_type,
       school_id as school,
       sum(type_of_movement * quantity) as has,
       sum(type_of_movement * summ)     as summ


from schol_library_incomeexpense

where  true and school_id > 1 and edition_id > 1


group by edition_id,
         income,
         income_type,
         school_id
having 
sum(type_of_movement * quantity) <> 0 
order by edition_id
    """
    result = []

    with connection.cursor() as cursor:
        if school is not None:
            query_text = query_text.replace('school_id > 1', "school_id=" + str(school.pk))
        if len(edition) > 0:
            query_text = query_text.replace('edition_id > 1', "edition_id in " + '(%s)' % ', '.join(map(repr, edition)))
        cursor.execute(query_text)
        result = dictfetchall(cursor)

    return result


@method_decorator(user_passes_test(llibrarian_or_head, login_url='home:index'), name='dispatch')
class ActWriteOffView(APIView):
    serializer = serializers.NewActWriteOffSerializers
    serializer2 = serializers.ActWriteOffSerializers
    post_e_model_s = serializers.PostEditionActWriteSerializers
    post_model_s = serializers.PostActWriteOffSerializers
    model = library_models.ActWriteOff
    e_model = library_models.EditionActWrite

    def get(self, request):
        context = {}

        if request.GET.get('all_invoices'):
            # context = cached_api(lang=translation.get_language())
            # snippets = NumberBooks.objects.filter(school=request.user.libraryuser.school)
            # serializer = serializers.RegisterAPIList(snippets, many=True)
            # context['books'] = serializer.data
            act_objects = self.model.objects.filter(
                school=request.user.libraryuser.school).select_related('author').order_by('-id')
            for obj in act_objects:
                obj.author_fio = obj.author.get_full_name()

            context['invoices'] = self.serializer(
                act_objects,
                many=True
            ).data
            return Response(data=context)

        elif request.GET.get('e_invoices'):
            invoice = self.model.objects.get(
                pk=request.GET.get('e_invoices'),
                school=request.user.libraryuser.school
            )
            invoice.author_fio = invoice.author.get_full_name()
            acces = AccessToEdit.objects.filter(
                school_id=request.user.libraryuser.school.id)[0]
            if acces.date_invoice > invoice.date:
                invoice.editable = False
            context['invoice'] = self.serializer2(invoice).data
            return Response(data=context)
        else:
            template_name = 'schol_library/head_librarian/act_write_off.html'
            return render(request, template_name=template_name, context=context)

    # Пост запросы
    def post(self, request, format=None):
        acces = AccessToEdit.objects.filter(
            school_id=request.user.libraryuser.school.id)[0]

        if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                school_id=request.user.libraryuser.school.id, edit_status=1).exists():

            if 'deleted' in request.data:
                if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                        school_id=request.user.libraryuser.school.id, edit_status=1
                ).exists():
                    invoice = self.model.objects.get(
                        pk=request.data['deleted'],
                        school=request.user.libraryuser.school
                    )
                    if acces.date_invoice > invoice.date:
                        return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                        status=status.HTTP_403_FORBIDDEN)

                    invoice.deleted = True
                    invoice.save()
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            elif 'create_i' in request.data:
                data = request.data['create_i']
                if str(acces.date_invoice) > data['date']:
                    return Response({'errors': 'Запрещено создавать документ в закрытом периоде'},
                                    status=status.HTTP_403_FORBIDDEN)
                data['author'] = request.user.id
                data['school'] = request.user.libraryuser.school.id
                serializer = self.post_model_s(data=data)
                if serializer.is_valid():
                    serializer.save()
                    s = serializer.data
                    s['sum'] = 0
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                error = {
                    'errors': serializer.errors.values()
                }
                return Response(error)

            elif 'create_edition_invoice' in request.data or request.data.get('create_edition_invoice'):
                try:
                    data = request.data.get('create_edition_invoice')
                    invoice = self.model.objects.get(pk=data.get('invoice'))

                    if data.get('quantity') <= data.get('has'):
                        serializer = self.post_e_model_s(data=data)
                        context = {}
                        if serializer.is_valid():
                            serializer.save()
                            context['ei'] = serializer.data
                            context['invoice'] = self.serializer(invoice).data

                            return Response(context, status=status.HTTP_201_CREATED)

                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    return Response(status=status.HTTP_400_BAD_REQUEST)

                except:

                    return Response(status=status.HTTP_404_NOT_FOUND)

            elif request.data.get('ready'):
                invoice = self.model.objects.get(pk=request.data.get('ready'))
                if invoice.school.id == request.user.libraryuser.school.id:
                    invoice_data = request.data.get('invoice')
                    if acces.date_invoice > invoice.date:
                        return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                        status=status.HTTP_403_FORBIDDEN)
                    if invoice_data['status'] == False:
                        invoice_data['status'] = True
                    else:
                        invoice_data['status'] = False
                    invoice_data['school'] = invoice.school.id
                    invoice_data['author'] = request.user.id
                    serializer = self.post_model_s(invoice, data=invoice_data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    error = {
                        'errors': serializer.errors.values()
                    }
                    return Response(error)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)

            if request.data.get('delete_e') or 'delete_e' in request.data:
                error = {
                    'err': "Error"
                }
                try:
                    de = self.e_model.objects.get(id=int(request.data.get('delete_e')))
                    de.delete()
                    return Response({'id': request.data.get('delete_e')}, status=status.HTTP_200_OK)
                except:
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)

            try:
                eid = self.e_model.objects.get(pk=request.data['id'])
                if eid.invoice.school == request.user.libraryuser.school:
                    eid.quantity = int(request.data['quantity'])
                    eid.save()
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, format=None):
        error = {
            'err': "Error"
        }
        if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                school_id=request.user.libraryuser.school.id, edit_status=1).exists():
            try:
                context = {}
                de = self.e_model.objects.get(id=int(request.GET.get('e_invoices')))
                if de.invoice.school == request.user.libraryuser.school:
                    de.delete()
                    context['ei'] = self.serializer(de.invoice).data
                    return Response(data=context, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


# NeW API
class EditionListView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated | s_permissions.HeadlibrianPermission]
    serializer = api_serializers.EditionsSerializer
    post_serializer = api_serializers.NumberBooksSerializer
    model = models.Edition
    numberbook_model = models.NumberBooks

    def get(self, request, format=None):
        data = cache.get('all_editions_for_api')
        if data is None:

            big_qs = self.model.objects.select_related('klass',
                                                       'publisher',
                                                       'subject',
                                                       'language',
                                                       'author',
                                                       'study_direction',
                                                       'publish_date',
                                                       'series_by_year',
                                                       'metodology_complex').filter(deleted=False).order_by('name')

            data = self.serializer(big_qs, many=True).data
            cache.set('all_editions_for_api', data)

        # if not request.user.is_superuser:
        #     data = []
        return Response(data)


class SchoolListView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated | s_permissions.HeadlibrianPermission]
    serializer = api_serializers.SchoolSerializer

    model = models.p_models.AlmaMater

    def get(self, request, format=None):
        big_qs = self.model.objects.filter(deleted=False, nash=True)

        data = self.serializer(big_qs, many=True).data

        return Response(data)


# def post(self, request, format=None):
#     data_p = request.data
#     for item in data_p:
#         item['school'] = request.user.libraryuser.school.id
#         item['it_filled'] = request.user.id
#
#     serializer = self.post_serializer(data=data_p, many=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status.HTTP_200_OK)
#     else:
#         return Response({
#             'error_messages': serializer.error_messages,
#             'errors': serializer.errors
#
#         }, status=status.HTTP_400_BAD_REQUEST)


class NewActWriteOffView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated | s_permissions.HeadlibrianPermission]
    serializer = serializers.ActWriteOffSerializers
    post_e_model_s = serializers.PostEditionActWriteSerializers
    post_model_s = serializers.PostActWriteOffSerializers
    model = library_models.ActWriteOff
    e_model = library_models.EditionActWrite

    def get(self, request):
        context = dict()
        if request.GET.get('e_invoices'):
            invoice = self.model.objects.get(
                pk=request.GET.get('e_invoices'),
                school=request.user.libraryuser.school
            )
            editions_id = self.e_model.objects.filter(
                invoice=invoice,
                invoice__deleted=False
            ).values_list('edition_id', flat=True)
            context['editions_id'] = list(editions_id)
            context['invoice'] = self.serializer(invoice).data
            context['editions'] = serializers.EditionSerializerA(
                Edition.objects.filter(
                    id__in=Subquery(editions_id)
                ), many=True
            ).data
            return Response(data=context)

        snippets = NumberBooks.objects.filter(school=request.user.libraryuser.school)
        serializer = serializers.NumberBooksSerializerBooksAPIList(snippets, many=True)
        context['books'] = serializer.data
        context['invoices'] = self.serializer(
            self.model.objects.filter(
                school=request.user.libraryuser.school,
                deleted=False),
            many=True
        ).data
        return Response(data=context)

    # Пост запросы
    def post(self, request, format=None):

        if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                school_id=request.user.libraryuser.school.id, edit_status=1).exists():

            if 'deleted' in request.data:
                if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                        school_id=request.user.libraryuser.school.id, edit_status=1
                ).exists():
                    invoice = self.model.objects.get(
                        pk=request.data['deleted'],
                        school=request.user.libraryuser.school
                    )

                    invoice.deleted = True
                    invoice.save()
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            elif 'create_i' in request.data:
                data = request.data['create_i']
                data['author'] = request.user.id
                data['school'] = request.user.libraryuser.school.id
                serializer = self.post_model_s(data=data)
                if serializer.is_valid():
                    serializer.save()
                    s = serializer.data
                    s['sum'] = 0
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                error = {
                    'errors': serializer.errors.values()
                }
                return Response(error)

            elif 'create_edition_invoice' in request.data or request.data.get('create_edition_invoice'):
                try:
                    data = request.data.get('create_edition_invoice')
                    invoice = self.model.objects.get(pk=data.get('invoice'))
                    # n_boock = NumberBooks.objects.get(school_id=invoice.school_id, edition_id=data.get('edition'))
                    # data['amount'] = round(n_boock.results.get('amount') * data.get('quantity'), 2)

                    if data.get('quantity') <= data.get('has'):
                        serializer = self.post_e_model_s(data=data)
                        context = {}
                        if serializer.is_valid():
                            serializer.save()
                            context['ei'] = serializer.data
                            context['invoice'] = self.serializer(invoice).data
                            return Response(context, status=status.HTTP_201_CREATED)
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response(status=status.HTTP_404_NOT_FOUND)

            elif request.data.get('ready'):
                invoice = self.model.objects.get(pk=request.data.get('ready'))
                if invoice.school.id == request.user.libraryuser.school.id:
                    if request.data.get('status_r'):
                        invoice_data = request.data.get('invoice')
                        invoice_data['school'] = invoice.school.id
                        invoice_data['author'] = request.user.id
                        invoice_data['status'] = False
                        serializer = self.post_model_s(invoice, data=invoice_data)
                        if serializer.is_valid():
                            serializer.save()
                            return Response(serializer.data, status=status.HTTP_200_OK)
                        error = {
                            'errors': serializer.errors.values()
                        }
                        return Response(error)
                    else:
                        invoice_data = request.data.get('invoice')
                        invoice_data['school'] = invoice.school.id
                        invoice_data['author'] = request.user.id
                        invoice_data['status'] = True
                        serializer = self.post_model_s(invoice, data=invoice_data)
                        if serializer.is_valid():
                            serializer.save()
                            return Response(serializer.data, status=status.HTTP_200_OK)
                        error = {
                            'errors': serializer.errors.values()
                        }
                        return Response(error)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)

            if request.data.get('delete_e') or 'delete_e' in request.data:
                error = {
                    'err': "Error"
                }
                try:
                    de = self.e_model.objects.get(id=int(request.data.get('delete_e')))
                    de.delete()
                    return Response({'id': request.data.get('delete_e')}, status=status.HTTP_200_OK)
                except:
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)

            try:
                eid = self.e_model.objects.get(pk=request.data['id'])
                if eid.invoice.school == request.user.libraryuser.school:
                    eid.quantity = int(request.data['quantity'])
                    eid.save()
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, format=None):
        error = {
            'err': "Error"
        }
        if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                school_id=request.user.libraryuser.school.id, edit_status=1).exists():
            try:
                context = {}
                de = self.e_model.objects.get(id=int(request.GET.get('e_invoices')))
                if de.invoice.school == request.user.libraryuser.school:
                    de.delete()
                    context['ei'] = self.serializer(de.invoice).data
                    return Response(data=context, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


class NewPaperInvoiceView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated | s_permissions.HeadlibrianPermission]
    serializer = serializers.ActWriteOffSerializers
    post_e_model_s = serializers.PostEditionActWriteSerializers
    post_model_s = serializers.PostActWriteOffSerializers
    model = library_models.PaperInvoice
    e_model = library_models.EditionPaperInvoice

    def get(self, request):

        context = {}

        if request.GET.get('e_invoices'):
            invoice = PaperInvoice.objects.get(pk=request.GET.get('e_invoices'), school=request.user.libraryuser.school)
            editions_id = EditionPaperInvoice.objects.filter(invoice=invoice, invoice__deleted=False).values_list(
                'edition_id', flat=True)
            context['editions_id'] = list(editions_id)
            context['invoice'] = serializers.PaperInvoiceSerializers(invoice).data
            context['editions'] = serializers.EditionSerializerA(
                Edition.objects.filter(id__in=Subquery(editions_id)), many=True).data
            return Response(data=context)
        # context = cached_api(lang=translation.get_language())
        # context['invoices'] = serializers.PaperInvoiceSerializers(
        #     PaperInvoice.objects.filter(
        #         school=request.user.libraryuser.school, deleted=False), many=True).data
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Пост запросы
    def post(self, request, format=None):
        acces = AccessToEdit.objects.filter(
            school_id=request.user.libraryuser.school.id)[0]

        if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                school_id=request.user.libraryuser.school.id, edit_status=1).exists():

            if 'deleted' in request.data:
                if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                        school_id=request.user.libraryuser.school.id, edit_status=1).exists():
                    invoice = PaperInvoice.objects.get(pk=request.data['deleted'],
                                                       school=request.user.libraryuser.school)
                    if acces.date_invoice > invoice.date:
                        return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                        status=status.HTTP_403_FORBIDDEN)
                    invoice.deleted = request.data['set_status']
                    invoice.save()
                    invoice.author_fio = invoice.author.get_full_name()
                    acces = AccessToEdit.objects.filter(
                        school_id=request.user.libraryuser.school.id)[0]
                    if acces.date_invoice > invoice.date:
                        invoice.editable = False
                    data = {}
                    data['invoice'] = serializers.PaperInvoiceSerializers(invoice).data

                    return Response(data, status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            elif 'create_i' in request.data:
                data = request.data['create_i']
                if str(acces.date_invoice) > data['date']:
                    return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                    status=status.HTTP_403_FORBIDDEN)
                data['author'] = request.user.id
                data['school'] = request.user.libraryuser.school.id
                serializer = serializers.PaperInvoiceSerializerPost(data=data)
                if serializer.is_valid():
                    serializer.save()
                    serializer.instance.editions_invoice.all().delete()

                    for item in serializer.initial_data['editions_val']:
                        serializer.instance.editions_invoice.create(edition_id=item['editionId'],
                                                                    amount=float(item['amount']),
                                                                    quantity=float(item['quantity']))
                    s = serializer.data
                    s['sum'] = 0
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                error = {
                    'errors': serializer.errors.values()
                }
                return Response(error)

            elif 'create_edition_invoice' in request.data or request.data.get('create_edition_invoice'):
                serializer = serializers.PostEditionPaperInvoiceSerializers(data=request.data['create_edition_invoice'])
                context = {}
                if serializer.is_valid():
                    serializer.save()
                    context['ei'] = serializer.data
                    context['invoice'] = serializers.PaperInvoiceSerializers(
                        PaperInvoice.objects.get(pk=context['ei']['invoice'],
                                                 school=request.user.libraryuser.school)).data
                    return Response(context, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            elif request.data.get('ready'):
                invoice = PaperInvoice.objects.get(pk=request.data.get('ready'))
                if invoice.school.id == request.user.libraryuser.school.id:
                    if request.data.get('status_r'):
                        invoice_data = request.data.get('invoice')
                        if acces.date_invoice > invoice.date:
                            return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                            status=status.HTTP_403_FORBIDDEN)
                        invoice_data['school'] = invoice.school.id
                        invoice_data['author'] = request.user.id
                        invoice_data['status'] = False
                        serializer = serializers.PaperInvoiceSerializerPost(invoice, data=invoice_data)
                        if serializer.is_valid():
                            serializer.save()
                            serializer.instance.editions_invoice.all().delete()

                            for item in serializer.initial_data['editions_val']:
                                serializer.instance.editions_invoice.create(edition_id=item['editionId'],
                                                                            amount=float(item['amount']),
                                                                            quantity=float(item['quantity']))

                            return Response(serializer.data, status=status.HTTP_200_OK)
                        error = {
                            'errors': serializer.errors.values()
                        }
                        return Response(error)
                    else:
                        invoice_data = request.data.get('invoice')
                        if acces.date_invoice > invoice.date:
                            return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                            status=status.HTTP_403_FORBIDDEN)
                        invoice_data['school'] = invoice.school.id
                        invoice_data['author'] = request.user.id
                        invoice_data['status'] = True
                        serializer = serializers.PaperInvoiceSerializerPost(invoice, data=invoice_data)
                        if serializer.is_valid():
                            serializer.save()

                            serializer.instance.editions_invoice.all().delete()

                            for item in serializer.initial_data['editions_val']:
                                serializer.instance.editions_invoice.create(edition_id=item['editionId'],
                                                                            amount=float(item['amount']),
                                                                            quantity=float(item['quantity']))
                            serializer.save()
                            return Response(serializer.data, status=status.HTTP_200_OK)
                        error = {
                            'errors': serializer.errors.values()
                        }
                        return Response(error)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)

            if request.data.get('quantity'):
                try:
                    eid = EditionPaperInvoice.objects.get(pk=request.data['id'])
                    if not eid.invoice.status:

                        if eid.invoice.school == request.user.libraryuser.school:
                            eid.quantity = int(request.data['quantity'])
                            eid.save()
                            return Response(status=status.HTTP_201_CREATED)
                        else:
                            return Response(status=status.HTTP_404_NOT_FOUND)
                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            if request.data.get('delete_e') or 'delete_e' in request.data:
                error = {
                    'err': "Error"
                }
                try:
                    de = EditionPaperInvoice.objects.get(id=int(request.data.get('delete_e')))
                    if de.invoice.school == request.user.libraryuser.school:
                        de.delete()
                        return Response({'id': request.data.get('delete_e')}, status=status.HTTP_200_OK)
                    else:
                        return Response(error, status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)

            if request.data.get('amount'):
                try:
                    eid = EditionPaperInvoice.objects.get(pk=request.data['id'])
                    if eid.invoice.school == request.user.libraryuser.school and not eid.invoice.status:
                        eid.amount = int(request.data['amount'])
                        eid.save()
                        return Response(status=status.HTTP_201_CREATED)
                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                eid = EditionPaperInvoice.objects.get(pk=request.data['id'])
                if eid.invoice.school == request.user.libraryuser.school:
                    eid.quantity = int(request.data['quantity'])
                    eid.save()
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, format=None):
        error = {
            'err': "Error"
        }
        if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                school_id=request.user.libraryuser.school.id, edit_status=1).exists():
            try:
                context = {}
                de = EditionPaperInvoice.objects.get(id=int(request.GET.get('e_invoices')))
                if de.invoice.school == request.user.libraryuser.school:
                    de.delete()
                    context['ei'] = serializers.PaperInvoiceSerializers(de.invoice).data
                    return Response(data=context, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


class NewActWriteOffView2(APIView):
    serializer = serializers.NewActWriteOffSerializers
    post_e_model_s = serializers.PostEditionActWriteSerializers
    post_model_s = serializers.PostActWriteOffSerializers
    model = library_models.ActWriteOff
    e_model = library_models.EditionActWrite
    serializer2 = serializers.ActWriteOffSerializers
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated | s_permissions.HeadlibrianPermission]

    def get(self, request):
        context = {}

        if request.GET.get('all_invoices'):
            context = cached_api(lang=translation.get_language())
            # snippets = NumberBooks.objects.filter(school=request.user.libraryuser.school)
            # serializer = serializers.RegisterAPIList(snippets, many=True)
            # context['books'] = serializer.data
            context['invoices'] = self.serializer(
                self.model.objects.filter(
                    school=request.user.libraryuser.school),
                many=True
            ).data
            return Response(data=context)

        elif request.GET.get('e_invoices'):
            invoice = self.model.objects.get(
                pk=request.GET.get('e_invoices'),
                school=request.user.libraryuser.school
            )
            editions_id = self.e_model.objects.filter(
                invoice=invoice,
                invoice__deleted=False
            ).values_list('edition_id', flat=True)
            context['editions_id'] = list(editions_id)
            context['invoice'] = self.serializer(invoice).data
            context['editions'] = serializers.EditionSerializerA(
                Edition.objects.filter(
                    id__in=Subquery(editions_id)
                ), many=True
            ).data
            return Response(data=context)

        return Response(status=status.HTTP_404_NOT_FOUND)

    # Пост запросы
    def post(self, request, format=None):
        acces = AccessToEdit.objects.filter(
            school_id=request.user.libraryuser.school.id)[0]

        if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                school_id=request.user.libraryuser.school.id, edit_status=1).exists():

            if 'deleted' in request.data:
                if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                        school_id=request.user.libraryuser.school.id, edit_status=1).exists():
                    invoice = self.model.objects.get(pk=request.data['deleted'],
                                                     school=request.user.libraryuser.school)
                    if acces.date_invoice > invoice.date:
                        return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                        status=status.HTTP_403_FORBIDDEN)

                    invoice.deleted = request.data['set_status']

                    invoice.save()
                    invoice.author_fio = invoice.author.get_full_name()

                    if acces.date_invoice > invoice.date:
                        invoice.editable = False
                    invoice.author_fio = invoice.author.get_full_name()
                    ret_data = {}
                    ret_data['invoice'] = serializers.ActWriteOffSerializers(invoice).data
                    return Response(ret_data, status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            elif 'create_i' in request.data:

                data = request.data['create_i']
                if str(acces.date_invoice) > data['date_invoice']:
                    return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                    status=status.HTTP_403_FORBIDDEN)
                data['author'] = request.user.id
                data['school'] = request.user.libraryuser.school.id
                serializer = self.post_model_s(data=data)

                if serializer.is_valid():

                    serializer.save()
                    serializer.instance.editions_invoice.all().delete()

                    for item in serializer.initial_data['editions_val']:
                        serializer.instance.editions_invoice.create(edition_id=item['editionId'],
                                                                    price=float(item['price']),
                                                                    has=float(item['has']),
                                                                    summ=float(item['summ']),
                                                                    income=int(item['income']),
                                                                    income_type=int(item['income_type']),
                                                                    amount=float(item['amount']),
                                                                    quantity=float(item['quantity']))
                    serializer.save()
                    s = serializer.data
                    invoice = models.ActWriteOff.objects.get(pk=s['id'])
                    if acces.date_invoice > invoice.date:
                        invoice.editable = False
                    invoice.author_fio = invoice.author.get_full_name()
                    ret_data = serializers.ActWriteOffSerializers(invoice).data
                    s['sum'] = 0
                    return Response(ret_data, status=status.HTTP_201_CREATED)
                error = {
                    'errors': serializer.errors.values()
                }
                return Response(error)

            elif request.data.get('ready'):
                invoice = self.model.objects.get(pk=request.data.get('ready'))
                if invoice.school.id == request.user.libraryuser.school.id:
                    invoice_data = request.data.get('invoice')
                    if acces.date_invoice > invoice.date:
                        return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                        status=status.HTTP_403_FORBIDDEN)
                    if request.data.get('status_r') == False:
                        invoice_data['status'] = True
                    else:
                        invoice_data['status'] = False
                    invoice_data['school'] = invoice.school.id
                    invoice_data['author'] = request.user.id
                    serializer = self.post_model_s(invoice, data=invoice_data)
                    if serializer.is_valid():
                        serializer.save()
                        serializer.instance.editions_invoice.all().delete()

                        for item in serializer.initial_data['editions_val']:
                            serializer.instance.editions_invoice.create(edition_id=item['editionId'],
                                                                        price=float(item['price']),
                                                                        has=float(item['has']),
                                                                        summ=float(item['summ']),
                                                                        income=int(item['income']),
                                                                        income_type=int(item['income_type']),
                                                                        amount=float(item['amount']),
                                                                        quantity=float(item['quantity']))
                        serializer.save()
                        if acces.date_invoice > invoice.date:
                            invoice.editable = False
                        invoice.author_fio = invoice.author.get_full_name()
                        ret_data = serializers.ActWriteOffSerializers(invoice).data

                        return Response(ret_data, status=status.HTTP_200_OK)
                    error = {
                        'errors': serializer.errors.values()
                    }
                    return Response(error)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)

            if request.data.get('delete_e') or 'delete_e' in request.data:
                error = {
                    'err': "Error"
                }
                try:
                    de = self.e_model.objects.get(id=int(request.data.get('delete_e')))
                    de.delete()
                    return Response({'id': request.data.get('delete_e')}, status=status.HTTP_200_OK)
                except:
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)

            try:
                eid = self.e_model.objects.get(pk=request.data['id'])
                if eid.invoice.school == request.user.libraryuser.school:
                    eid.quantity = int(request.data['quantity'])
                    eid.save()
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, format=None):
        error = {
            'err': "Error"
        }
        if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                school_id=request.user.libraryuser.school.id, edit_status=1).exists():
            try:
                context = {}
                de = self.e_model.objects.get(id=int(request.GET.get('e_invoices')))
                if de.invoice.school == request.user.libraryuser.school:
                    de.delete()
                    context['ei'] = self.serializer(de.invoice).data
                    return Response(data=context, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


class PaginationGetNewInitialBalanceView(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10


class GetNewInitialBalanceView(ListAPIView):
    serializers_class = InitialBalanceSerializers
    pagination_class = PaginationGetNewInitialBalanceView
    queryset = InitialBalance.objects.all()


class NewInitialBalanceView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated | s_permissions.HeadlibrianPermission]
    serializer = serializers.InitialBalanceSerializers
    post_e_model_s = serializers.PostEditionInitialbalanceSerializers
    post_model_s = serializers.InitialBalanceSerializerPost
    model = library_models.InitialBalance
    e_model = library_models.EditionInitialBalance


    def get(self, request):
        context = {}

        if request.GET.get('all_invoices'):
            context = cached_api(lang=translation.get_language())
            context['invoices'] = serializers.InitialBalanceSerializers(
                InitialBalance.objects.filter(
                    school=request.user.libraryuser.school).order_by('-id'), many=True).data
            return Response(data=context)
            # cart  = InitialBalance.objects.filter(school=request.user.libraryuser.school).order_by('-id')
            # cart_details = InitialBalance.objects.all()
            # page = self.paginate_queryset(cart_details)
            # if page is not None:
            #     serializer = InitialBalanceSerializers(page, many=True)
            #     return self.get_paginated_response(serializer.data)
            #
            # serializer = InitialBalanceSerializers(cart_details, many=True)
            # return Response(serializer.data)

        elif request.GET.get('e_invoices'):
            invoice = InitialBalance.objects.get(pk=request.GET.get('e_invoices'),
                                                 school=request.user.libraryuser.school)
            editions_id = EditionInitialBalance.objects.filter(invoice=invoice,
                                                               invoice__deleted=False).values_list('edition_id',
                                                                                                   flat=True)
            context['editions_id'] = list(editions_id)
            context['invoice'] = serializers.InitialBalanceSerializers(invoice).data
            context['editions'] = serializers.EditionSerializerA(
                Edition.objects.filter(id__in=Subquery(editions_id)), many=True).data
            return Response(data=context)
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Пост запросы
    def post(self, request, format=None):
        acces = AccessToEdit.objects.filter(school_id=request.user.libraryuser.school.id)[0]
        # if acces.date_invoice < timezone.now().date():
        #     return Response(status=status.HTTP_403_FORBIDDEN)

        if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                school_id=request.user.libraryuser.school.id,
                edit_status=1).exists():

            if 'deleted' in request.data:
                if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                        school_id=request.user.libraryuser.school.id, edit_status=1).exists():

                    invoice = InitialBalance.objects.get(pk=request.data['deleted'],
                                                         school=request.user.libraryuser.school)
                    if acces.date_invoice > invoice.date:
                        return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                        status=status.HTTP_403_FORBIDDEN)

                    invoice.deleted = request.data['set_status']

                    invoice.save()

                    invoice.author_fio = invoice.author.get_full_name()
                    acces = AccessToEdit.objects.filter(
                        school_id=request.user.libraryuser.school.id)[0]
                    if acces.date_invoice > invoice.date:
                        invoice.editable = False
                    data = {}
                    data['invoice'] = serializers.InitialBalanceSerializers(invoice).data

                    return Response(data, status=status.HTTP_201_CREATED)

                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)


            elif 'create_i' in request.data:
                data = request.data['create_i']
                if str(acces.date_invoice) > data['date']:
                    return Response({'errors': 'Запрещено создавать документ в закрытом периоде'},
                                    status=status.HTTP_403_FORBIDDEN)
                data['author'] = request.user.id
                data['school'] = request.user.libraryuser.school.id
                serializer = serializers.InitialBalanceSerializerPost(data=data)
                if serializer.is_valid():
                    serializer.save()
                    for item in serializer.initial_data['editions_val']:
                        serializer.instance.editions_invoice.create(edition_id=item['editionId'],
                                                                    amount=float(item['amount']),
                                                                    quantity=float(item['quantity']))

                    serializer.save()
                    s = serializer.data
                    s['sum'] = 0
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                error = {
                    'errors': serializer.errors.values()
                }
                return Response(error)

            elif request.data.get('ready'):
                invoice = InitialBalance.objects.get(pk=request.data.get('ready'))
                if invoice.school.id == request.user.libraryuser.school.id:

                    if request.data.get('status_r'):
                        invoice_data = request.data.get('invoice')
                        if acces.date_invoice > invoice.date:
                            return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                            status=status.HTTP_403_FORBIDDEN)
                        invoice_data['school'] = invoice.school.id
                        invoice_data['author'] = request.user.id
                        invoice_data['status'] = False

                        serializer = serializers.InitialBalanceSerializerPost(
                            invoice, data=invoice_data)
                        if serializer.is_valid():
                            serializer.save()
                            serializer.instance.editions_invoice.all().delete()

                            for item in serializer.initial_data['editions_val']:
                                serializer.instance.editions_invoice.create(edition_id=item['editionId'],
                                                                            amount=float(item['amount']),
                                                                            quantity=float(item['quantity']))
                            # del_ie_paper_invoice(invoice=invoice)

                            return Response(serializer.data, status=status.HTTP_200_OK)
                        error = {
                            'errors': serializer.errors.values()
                        }
                        return Response(error)
                    else:
                        invoice_data = request.data.get('invoice')
                        if acces.date_invoice > invoice.date:
                            return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                            status=status.HTTP_403_FORBIDDEN)
                        invoice_data['school'] = invoice.school.id
                        invoice_data['author'] = request.user.id
                        invoice_data['status'] = True
                        serializer = serializers.InitialBalanceSerializerPost(invoice, data=invoice_data)
                        if serializer.is_valid():
                            serializer.save()
                            serializer.instance.editions_invoice.all().delete()

                            for item in serializer.initial_data['editions_val']:
                                serializer.instance.editions_invoice.create(edition_id=item['editionId'],
                                                                            amount=float(item['amount']),
                                                                            quantity=float(item['quantity']))
                            serializer.save()
                            # update_ie_paper_invoice(invoice=invoice, user=request.user)
                            return Response(serializer.data, status=status.HTTP_200_OK)
                        error = {
                            'errors': serializer.errors.values()
                        }
                        return Response(error)

                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)

            if request.data.get('quantity'):
                try:
                    eid = EditionInitialBalance.objects.get(pk=request.data['id'])
                    if not eid.invoice.status:
                        if eid.invoice.school == request.user.libraryuser.school:
                            eid.quantity = int(request.data['quantity'])
                            eid.save()
                            return Response(status=status.HTTP_201_CREATED)
                        else:
                            return Response(status=status.HTTP_404_NOT_FOUND)
                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            if request.data.get('delete_e') or 'delete_e' in request.data:
                error = {
                    'err': "Error"
                }
                try:
                    de = EditionInitialBalance.objects.get(id=int(request.data.get('delete_e')))
                    if de.invoice.school == request.user.libraryuser.school:
                        de.delete()
                        return Response({'id': request.data.get('delete_e')}, status=status.HTTP_200_OK)
                    else:
                        return Response(error, status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)

            if request.data.get('amount'):
                try:
                    eid = EditionInitialBalance.objects.get(pk=request.data['id'])
                    if eid.invoice.school == request.user.libraryuser.school and not eid.invoice.status:
                        eid.amount = int(request.data['amount'])
                        eid.save()
                        return Response(status=status.HTTP_201_CREATED)
                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                eid = EditionInitialBalance.objects.get(pk=request.data['id'])
                if eid.invoice.school == request.user.libraryuser.school:
                    eid.quantity = int(request.data['quantity'])
                    eid.save()
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, format=None):
        error = {
            'err': "Error"
        }
        if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                school_id=request.user.libraryuser.school.id, edit_status=1).exists():
            try:
                context = {}
                de = EditionPaperInvoice.objects.get(id=int(request.GET.get('e_invoices')))
                if de.invoice.school == request.user.libraryuser.school:
                    de.delete()
                    context['ei'] = serializers.InitialBalanceSerializers(de.invoice).data
                    return Response(data=context, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


class BookOrdersGlobalList(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        context = {}
        if request.GET.get('all_orders'):
            order_records = library_models.EditionBooksOrder.objects.select_related('invoice',
                                                                                    'invoice__author').filter(
                invoice__status=True, invoice__deleted=False)
            for i in order_records:
                i.school = i.invoice.school_id
                i.date = i.invoice.date
                i.author = i.invoice.author_id
                i.author_fio = i.invoice.author.get_full_name()

            serializer = serializers.AdminBooksOrders
            context['orders'] = serializer(order_records, many=True).data
            return Response(data=context)
        elif 'ready_in_school' in request.GET:
            order_ed = models.EditionBooksOrder.objects.get(pk=request.GET['ready_in_school'])
            context['ready_in_school'] = get_counts_from_registry(None, [order_ed.edition_id])
            return Response(data=context)
        elif 'user_detail_info' in request.GET:
            user = p_models.User.objects.get(pk=request.GET['user_detail_info']).portfolio_set.first()
            deatil = serializers.ABOPortfolioMSerializers(user).data
            context['user_detail'] = deatil
            return Response(data=context)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class BooksRecallView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated | s_permissions.HeadlibrianPermission]

    def get(self, request):
        if request.GET.get('all_orders'):
            reords = models.BooksRecall.objects.all().select_related('order')
            for i in reords:
                i.order_school = i.order.school_id
            serializer = serializers.BooksRecallSerializer
            data = serializer(reords, many=True).data
            return Response(data=data)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        data = request.data.get('recall')
        data['author'] = request.user.id
        data['school'] = request.user.libraryuser.school.id

        serializer = serializers.BooksRecallSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            models.BooksMovingHead.objects.filter(recall=serializer.instance.id).delete()
            bm = models.BooksMovingHead()
            bm.author = request.user
            bm.recipient_school = serializer.instance.order.school
            bm.sender_school = serializer.instance.school
            bm.status = True  # Сразу проведенное перемещение
            bm.recall = serializer.instance
            bm.date = timezone.now().date()
            bm.save()
            bme = models.BooksMovingEdition()
            bme.invoice = bm
            bme.edition = serializer.instance.edition
            bme.quantity = serializer.instance.quantity
            bme.income = bm.id
            bme.income_type = 3
            bme.save()
            bm.save()

            return Response(data=data)

        return Response(status=status.HTTP_400_BAD_REQUEST)


# class KontingentView(APIView):
#     authentication_classes = [TokenAuthentication, SessionAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#
#         if request.GET.get('all'):
#             reords = models.Kontingent.objects.filter(deleted=False)
#
#             serializer = serializers.KontingentSerializer
#             data = serializer(reords, many=True).data
#             return Response(data=data)
#
#         elif request.GET.get('pk'):
#             reords = models.Kontingent.objects.filter(school=request.GET.get('pk'), year=9)
#             if len(reords)>0:
#                 p = reords[0]
#             else:
#                 p = models.Kontingent()
#
#             serializer = serializers.KontingentSerializer
#             data = serializer(p).data
#             return Response(data=data)
#
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     def post(self, request):
#         data = request.data.get('data')
#         data['author'] = request.user.id
#         data['school'] = request.user.libraryuser.school.id
#
#         serializer = serializers.KontingentSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response(data=data)
#
#         return Response(status=status.HTTP_400_BAD_REQUEST)


def get_ost(request):
    context = {}
    context['books'] = get_counts_from_registry(request.user.libraryuser.school)

    return JsonResponse(context)


def clear_up_nb(request):
    nb = models.NumberBooks
    nb_no_school = nb.objects.filter(school=None)
    nb_no_edition = nb.objects.filter(edition=None)
    nb_all = nb_no_edition | nb_no_school
    nb_all.delete()

    nb_no_amount = nb.objects.filter(amounts=0).select_related('edition')
    for el in nb_no_amount:
        el.amounts = el.in_warehouse * el.edition.amount
        el.save()

    return HttpResponse('ok')


def get_demand_books(school_filter=None):
    query_text = """
select s1.edition_id  as edition,
       s2.school_id   as school,
       s1.surplus, 
       s2.year_id as year,
       s2.klass_id    as klass,
       s2.language_id as language,
       s2.study_direction_id as study_direction
 from schol_library_editionbriefcase as s1
       inner join schol_library_briefcase s2 on s1.briefcase_id = s2.id
where s2.status and s2.year_id = 9
       """
    if not school_filter is None:
        query_text = query_text + ' and s2.school_id=' + str(school_filter.id)

    result = {}

    with connection.cursor() as cursor:
        cursor.execute(query_text)
        result['briefcases'] = dictfetchall(cursor)

    query_text = """
 select study_direction_id as study_direcrion,
       sls.school_id          as school,
       language_id        as language,
       sls.klass_id           as klass,
       liter_id           as liter,
       students,
       sls.year_id            as year
from schol_library_schooltitul
       inner join schol_library_schooltitulhead as sls on schol_library_schooltitul.titul_head_id = sls.id
where sls.status
  and sls.year_id = 9
           """
    if not school_filter is None:
        query_text = query_text + ' and sls.school_id=' + str(school_filter.id)

    query_text += ' order by school,klass'

    with connection.cursor() as cursor:
        cursor.execute(query_text)
        result['titul'] = dictfetchall(cursor)

    return result


def get_demand(request):
    school_filter = None
    if not request.user.is_superuser and not request.user.groups.filter(id=6).exists():
        school_filter = request.user.libraryuser.school

    return JsonResponse(get_demand_books(school_filter))


def change_editon_set(request):
    context = {}
    if not request.user.is_superuser:
        return HttpResponseForbidden('forbidden')

    if request.method == 'GET':
        return render(request, 'schol_library/superuser/change_editions_id.html', context)
    elif request.method == 'POST':
        new = Edition.objects.get(pk=request.POST['new_id'])
        for i in request.POST['old_id'].split(','):

            old = Edition.objects.get(pk=i)

            sets = {}
            sets['ed_paper_invoice'] = old.editionpaperinvoice_set.all()
            sets['ed_invoice'] = old.editioninvoice_set.all()
            sets['ed_initial_balance'] = old.editioninitialbalance_set.all()
            sets['ed_briefcase'] = old.editionbriefcase_set.all()
            sets['ed_books_order'] = old.editionbooksorder_set.all()
            sets['ed_act_writeoff'] = old.editionactwrite_set.all()

            sets['books_recall'] = old.booksrecall_set.all()
            sets['request_edition'] = old.requestedition_set.all()
            sets['plane_edition_teacher'] = old.planeditionteacher_set.all()
            sets['number_book'] = old.numberbooks_set.all()
            sets['income_expence'] = old.incomeexpense_set.all()

            for set in sets.values():
                for el in set:
                    el.edition = new
                    el.save()

        return HttpResponse('ok')


def get_all_ost(request):
    context = {}
    if not request.user.is_superuser and not request.user.groups.filter(id=6).exists():
        return HttpResponseForbidden('forbidden')

    query_text = """
        select edition_id as edition,
           income,
           income_type,
           school_id as school,
           sum(type_of_movement * quantity) as has,
           sum(type_of_movement * summ)     as summ


    from schol_library_incomeexpense

    where  true and school_id > 1 and edition_id > 1


    group by edition_id,
             income,
             income_type,
             school_id
    having sum(type_of_movement * quantity) <> 0 order by edition_id
        """
    result = []
    with connection.cursor() as cursor:
        cursor.execute(query_text)
        result = dictfetchall(cursor)
    context['books'] = result
    return JsonResponse(context)


def clear_up_nb(request):
    nb = models.NumberBooks
    nb_no_school = nb.objects.filter(school=None)
    nb_no_edition = nb.objects.filter(edition=None)
    nb_all = nb_no_edition | nb_no_school
    nb_all.delete()

    nb_no_amount = nb.objects.filter(amounts=0).select_related('edition')
    i = 0
    for el in nb_no_amount:
        i += 1
        print(i)
        el.amounts = el.in_warehouse * el.edition.amount
        el.save()

    return HttpResponse('ok')


class SchoolTitul(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated | s_permissions.HeadlibrianPermission]

    def get(self, request):
        if request.GET.get('e_invoices'):
            # reords = models.BooksRecall.objects.all().select_related('order')
            # for i in reords:
            #     i.order_school = i.order.school_id

            serializer = serializers.GetSchoolTitulFullSerializer
            titul = models.SchoolTitulHead.objects.get(pk=request.GET['e_invoices'])
            acces = AccessToEdit.objects.filter(
                school_id=request.user.libraryuser.school.id)[0]
            if acces.date_invoice > titul.date:
                titul.editable = False
            titul.students = models.SchoolTitul.objects.filter(titul_head=titul)
            data = {'invoice': serializer(titul).data}

            return Response(data=data)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        acces = AccessToEdit.objects.filter(
            school_id=request.user.libraryuser.school.id)[0]
        if 'create_i' in request.data:
            data = request.data['create_i']
            if str(acces.date_invoice) > data['date']:
                return Response({'errors': 'Запрещено создавать документ в закрытом периоде'},
                                status=status.HTTP_403_FORBIDDEN)
            data['school'] = request.user.libraryuser.school.id
            serializer = serializers.PostSchoolTitulFullSerializer(data=data)
            if serializer.is_valid():
                serializer.save()

                for i in serializer.initial_data['students']:
                    serializer.instance.school_titul.create(
                        titul_head=serializer.instance,
                        school=serializer.instance.school,
                        klass=serializer.instance.klass,
                        liter=models.Liter.objects.get(pk=i['liter']),
                        students=i['students'],
                        year=serializer.instance.year,
                        language=p_models.Language.objects.get(pk=i['language']),
                        study_direction=models.StudyDirections.objects.get(pk=i['study_direction'])
                    )
                s = serializer.data
                invoice = models.SchoolTitulHead.objects.get(pk=s['id'])
                if acces.date_invoice > invoice.date:
                    invoice.editable = False
                invoice.students = models.SchoolTitul.objects.filter(titul_head=invoice)
                ret_data = serializers.GetSchoolTitulFullSerializer(invoice).data
                return Response(ret_data, status=status.HTTP_200_OK)
        elif request.data.get('ready'):
            titul = models.SchoolTitulHead.objects.get(pk=request.data.get('ready'))
            if titul.school.id == request.user.libraryuser.school.id:
                if request.data.get('status_r'):
                    invoice_data = request.data.get('invoice')
                    if acces.date_invoice > titul.date:
                        return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                        status=status.HTTP_403_FORBIDDEN)

                    invoice_data['school'] = request.user.libraryuser.school.id
                    invoice_data['status'] = False

                    serializer = serializers.PostSchoolTitulFullSerializer(titul, data=invoice_data)
                    if serializer.is_valid():
                        serializer.save()
                        models.SchoolTitul.objects.filter(titul_head=serializer.instance).delete()

                        for i in serializer.initial_data['students']:
                            serializer.instance.school_titul.create(titul_head=serializer.instance,
                                                                    school=serializer.instance.school,
                                                                    klass=serializer.instance.klass,
                                                                    liter=models.Liter.objects.get(pk=i['liter']),
                                                                    students=i['students'],
                                                                    year=serializer.instance.year,
                                                                    language=p_models.Language.objects.get(
                                                                        pk=i['language']),
                                                                    study_direction=models.StudyDirections.objects.get(
                                                                        pk=i['study_direction']))

                    data = serializer.data
                    if acces.date_invoice > titul.date:
                        titul.editable = False
                    titul.students = models.SchoolTitul.objects.filter(titul_head=titul)
                    ret_data = serializers.GetSchoolTitulFullSerializer(titul).data
                    return Response(ret_data, status=status.HTTP_200_OK)
                else:
                    invoice_data = request.data.get('invoice')
                    if acces.date_invoice > titul.date:
                        return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                        status=status.HTTP_403_FORBIDDEN)
                    invoice_data['school'] = request.user.libraryuser.school.id
                    invoice_data['status'] = True
                    serializer = serializers.PostSchoolTitulFullSerializer(titul, data=invoice_data)
                    if serializer.is_valid():
                        serializer.save()
                        models.SchoolTitul.objects.filter(titul_head=serializer.instance).delete()

                        for i in serializer.initial_data['students']:
                            serializer.instance.school_titul.create(titul_head=serializer.instance,
                                                                    school=serializer.instance.school,
                                                                    klass=serializer.instance.klass,
                                                                    liter=models.Liter.objects.get(pk=i['liter']),
                                                                    students=i['students'],
                                                                    year=serializer.instance.year,
                                                                    language=p_models.Language.objects.get(
                                                                        pk=i['language']),
                                                                    study_direction=models.StudyDirections.objects.get(
                                                                        pk=i['study_direction']))

                        if acces.date_invoice > titul.date:
                            titul.editable = False
                        titul.students = models.SchoolTitul.objects.filter(titul_head=titul)
                        ret_data = serializers.GetSchoolTitulFullSerializer(titul).data
                        return Response(ret_data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        elif 'deleted' in request.data:
            if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                    school_id=request.user.libraryuser.school.id, edit_status=1).exists():
                invoice = models.SchoolTitulHead.objects.get(pk=request.data['deleted'],
                                                             school=request.user.libraryuser.school)
                if acces.date_invoice > invoice.date:
                    return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                    status=status.HTTP_403_FORBIDDEN)
                invoice.deleted = request.data['set_status']
                invoice.save()
                data = {}
                if acces.date_invoice > invoice.date:
                    invoice.editable = False
                invoice.students = models.SchoolTitul.objects.filter(titul_head=invoice)
                data['invoice'] = serializers.GetSchoolTitulFullSerializer(invoice).data
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)
