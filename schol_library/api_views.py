from rest_framework.generics import ListAPIView

from account.api import NewGetSchool, GetSchool
import datetime
from account.models import AccessToEdit
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.base import TemplateView
from django.views import View
from django.utils.decorators import method_decorator
from .valid_view import head_librarian, llibrarian_or_head, llibrarian_or_admin
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from django.shortcuts import render
from .models import IncomeExpense, EditionInvoice, Invoice, Provider, Edition, PaperInvoice, EditionPaperInvoice, \
    RequestEdition, \
    CheckidRequestEdition, NumberBooks, IncomeExpense, InitialBalance, EditionInitialBalance, BooksOrder, \
    EditionBooksOrder, User
from schol_library import models as library_models, permissions as s_permissions
from .serializers import InvoiceSerializers, InitialBalanceSerializers, GetInitialBalanceSerializers
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
from rest_framework.decorators import api_view
from portfoli.models import PortfolioWorkTimeLine
from schol_library.user_utils import LIBRARIAN
from schol_library.user_utils import LIBRARIAN_ZAM
from rest_framework.pagination import PageNumberPagination

from django.shortcuts import get_object_or_404
from .b_case_serializers import BriefcaseSerializers, BriefcaseSerializersSchoolID, PostEditionBriefcaseSerializers, \
    PostBriefcaseSerializers, \
    EditionBriefcaseSerializers, SchoolTitulListSerializer, PostPlanEditionTeacherSerializer, \
    GetPlanEditionTeacherSerializer
from .models import SchoolTitul, PlannedTitle, Edition, Briefcase, EditionBriefcase, Liter, StudyDirections, \
    PlanEditionTeacher
from .serializers import PlanSchoolTitulSerializers, PostPlanSchoolTitulSerializers, \
    ListPlanSchoolTitulSerializers, DateObjectsSerializer, PostPlanSchoolTitulDetailSerializers
from schol_library import b_case_serializers
from .views import get_counts_from_registry, BooksRecallView
import ast
from . import user_utils

try:
    from ekitaphana.settings import WHEN_READY

    wh_ready = WHEN_READY
except:
    wh_ready = ''



def my_school_list(user):
    library_role_ids = [LIBRARIAN, LIBRARIAN_ZAM]
    if user.is_superuser and 5 == 5:  # для тестов
        # scools = AccessToEdit.objects.all()[:11]
        scools = PortfolioWorkTimeLine.objects.filter(deleted=False, school__nash=True,
                                                      school__has_access_to_ekitaphana=True,
                                                      school__deleted=False).distinct('school')
        my_scools = scools.values('school_id',
                                  'school__name_ru',
                                  'school__name_kk')
    else:
        my_scools = PortfolioWorkTimeLine.objects.filter(portfolio__user=user,
                                                         current=True,
                                                         date_end__isnull=True,
                                                         uvolen=False,
                                                         checked=True,
                                                         school__has_access_to_ekitaphana=True,
                                                         deleted=False,
                                                         positions__in=library_role_ids,
                                                         ).distinct('school').values('school_id',
                                                                                     'school__name_ru',
                                                                                     'school__name_kk')
    return my_scools




class LibraryCurrentWorkTimeLinesViewAPI(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        context = {}
        my_scools = my_school_list(request.user)
        context['my_schools'] = my_scools
        return Response(data=context)

class PaginationGetNewInitialBalanceView(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 10


class GetNewInitialBalanceView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated | s_permissions.HeadlibrianPermission]
    def get(self, request):
        posts = InitialBalance.objects.filter(
                school=request.user.libraryuser.school, deleted=False).select_related('author').order_by('-id')
        paginator = PaginationGetNewInitialBalanceView()
        results = paginator.paginate_queryset(posts,request)
        serializer = GetInitialBalanceSerializers(results, many=True)
        return paginator.get_paginated_response({"data": serializer.data})



class InitialBalanceViewAPI(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated | s_permissions.HeadlibrianPermission]
    pagination_class = PaginationGetNewInitialBalanceView
    def get(self, request):
        context = {}

        if request.GET.get('all_invoices'):
            ib_objects = InitialBalance.objects.filter(
                school=request.user.libraryuser.school, deleted=False).select_related('author').order_by('-id')

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
                invoice.editable = True
            context['invoice'] = serializers.InitialBalanceSerializers(invoice).data
            return Response(data=context)
        else:
            template_name = 'schol_library/head_librarian/paper_invoice.html'
            return render(request, template_name=template_name, context=context)

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
                    # if acces.date_invoice > invoice.date:
                    #     return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                    #                     status=status.HTTP_403_FORBIDDEN)

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
                # if str(acces.date_invoice) > data['date']:
                #     return Response({'errors': 'Запрещено создавать документ в закрытом периоде'},
                #                     status=status.HTTP_403_FORBIDDEN)
                data['author'] = request.user.id
                data['school'] = request.user.libraryuser.school.id
                data['status'] = True
                serializer = serializers.InitialBalanceSerializerPost(data=data)
                if serializer.is_valid():
                    serializer.save()
                    for item in serializer.initial_data['editions_val']:
                        serializer.instance.editions_invoice.create(edition_id=item['editionId'],
                                                                    amount=float(item['amount']),
                                                                    quantity=float(item['quantity']))

                    #                    serializer.instance.save()
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
                        # if acces.date_invoice > invoice.date:
                        #     return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                        #                     status=status.HTTP_403_FORBIDDEN)
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
                        # if acces.date_invoice > invoice.date:
                        #     return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                        #                     status=status.HTTP_403_FORBIDDEN)
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


class PaperInvoiceViewAPI(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated | s_permissions.HeadlibrianPermission]
    serializer = serializers.ActWriteOffSerializers
    post_e_model_s = serializers.PostEditionActWriteSerializers
    post_model_s = serializers.PostActWriteOffSerializers
    model = library_models.PaperInvoice
    e_model = library_models.EditionPaperInvoice

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
        elif request.GET.get('remont'):
            invoice = PaperInvoice.objects.get(pk=request.GET.get('remont'))
            invoice.author_fio = invoice.author.get_full_name()
            # acces = AccessToEdit.objects.filter(
            #     school_id=request.user.libraryuser.school.id)[0]
            # if acces.date_invoice > invoice.date:
            #     invoice.editable = False
            from django.db.models import Max
            l = list(invoice.editions_val.values('edition_id', 'quantity', 'amount').distinct())
            l1 = list(invoice.editions_invoice.all())
            l23 = []
            e = l1.__len__()
            for item in l:
                if item['edition_id'] in l23:
                    continue
                a = EditionPaperInvoice()
                a.invoice = invoice
                a.edition_id = item['edition_id']
                a.quantity = item['quantity']
                a.amount = item['amount']
                a.save()
                l23.append(item['edition_id'])

            for item in l1:
                item.delete()
            context['l'] = l
            context['invoice'] = serializers.PaperInvoiceSerializers(invoice).data
            # context['editions'] = serializers.EditionSerializerA(
            #     Edition.objects.filter(id__in=Subquery(editions_id)), many=True).data
            return Response(data=context)
        else:
            template_name = 'schol_library/head_librarian/paper_invoice.html'
            return render(request, template_name=template_name, context=context)

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


class ActWriteOffViewAPI(APIView):
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
            return Response(status=status.HTTP_400_BAD_REQUEST)

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


class BooksOrderViewAPI(APIView):
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


class SchoolTitulAPI(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    # permission_classes = [IsAuthenticated | s_permissions.HeadlibrianPermission]
    permission_classes = [IsAuthenticated | s_permissions.HeadlibrianPermissionByPosition]

    def my_school_ids_list(self, request):
        my_scools = my_school_list(request.user)
        school_ids_list = list(my_scools.values_list('school_id', flat=True).distinct())
        return school_ids_list

    def get(self, request):
        if request.GET.get('e_invoices'):

            serializer = serializers.GetSchoolTitulFullSerializer
            titul = models.SchoolTitulHead.objects.get(pk=request.GET['e_invoices'])
            if AccessToEdit.objects.filter(school=titul.school).__len__() <= 0:
                AccessToEdit.objects.create(school=titul.school)
            acces = AccessToEdit.objects.filter(school=titul.school)[0]

            if acces.date_invoice > titul.date:
                titul.editable = False

            # titul.students = models.SchoolTitul.objects.filter(titul_head=titul)

            data = {'invoice': serializer(titul).data}

            return Response(data=data)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        school_ids_list = self.my_school_ids_list(request)

        if 'create_i' in request.data:

            data = request.data['create_i']
            data['status'] = True
            if 'school' in data \
                    and not data['school'] in school_ids_list:
                return Response({'errors': 'Запрещено создавать документ в не своем учебном заведении'},
                                status=status.HTTP_403_FORBIDDEN)

            if AccessToEdit.objects.filter(school_id=data['school']).__len__() <= 0:
                AccessToEdit.objects.create(school_id=data['school'],
                                            edit_status=1,
                                            date_invoice=datetime.date(2021, 4, 1))

            acces = AccessToEdit.objects.filter(school_id=data['school'])[0]

            if str(acces.date_invoice) > data['date']:
                return Response({'errors': 'Запрещено создавать документ в закрытом периоде'},
                                status=status.HTTP_403_FORBIDDEN)

            serializer = serializers.PostSchoolTitulFullSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                s = serializer.data
                invoice = models.SchoolTitulHead.objects.get(pk=s['id'])

                if acces.date_invoice > invoice.date:
                    invoice.editable = False

                # invoice.students = models.SchoolTitul.objects.filter(titul_head=invoice)
                ret_data = serializers.GetSchoolTitulFullSerializer(invoice).data

                return Response(ret_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.data.get('ready'):
            titul = models.SchoolTitulHead.objects.get(pk=request.data.get('ready'))
            if AccessToEdit.objects.filter(school=titul.school).__len__() <= 0:
                AccessToEdit.objects.create(school=titul.school)

            acces = AccessToEdit.objects.filter(school=titul.school)[0]

            if titul.school.id in school_ids_list:
                if request.data.get('status_r'):
                    invoice_data = request.data.get('invoice')
                    if acces.date_invoice > titul.date:
                        return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                        status=status.HTTP_403_FORBIDDEN)

                    # invoice_data['school'] = request.user.libraryuser.school.id
                    invoice_data['status'] = False

                    serializer = serializers.PostSchoolTitulFullSerializer(titul, data=invoice_data)
                    if serializer.is_valid():
                        serializer.save()
                        models.SchoolTitul.objects.filter(titul_head=serializer.instance).delete()
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    data = serializer.data
                    if acces.date_invoice > titul.date:
                        titul.editable = False
                    # titul.students = models.SchoolTitul.objects.filter(titul_head=titul)
                    ret_data = serializers.GetSchoolTitulFullSerializer(titul).data

                    return Response(ret_data, status=status.HTTP_200_OK)

                else:
                    invoice_data = request.data.get('invoice')

                    if acces.date_invoice > titul.date:
                        return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                        status=status.HTTP_403_FORBIDDEN)

                    invoice_data['status'] = True
                    serializer = serializers.PostSchoolTitulFullSerializer(titul, data=invoice_data)

                    if serializer.is_valid():
                        serializer.save()
                        models.SchoolTitul.objects.filter(titul_head=serializer.instance).delete()

                        if acces.date_invoice > titul.date:
                            titul.editable = False

                        ret_data = serializers.GetSchoolTitulFullSerializer(titul).data

                        return Response(ret_data, status=status.HTTP_200_OK)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        elif 'deleted' in request.data:
            if request.user.groups.filter(id=6).exists() \
                    or AccessToEdit.objects.filter(school_id__in=school_ids_list,
                                                   edit_status=1).exists():

                invoice = models.SchoolTitulHead.objects.get(pk=request.data['deleted'],
                                                             school__in=school_ids_list)
                if AccessToEdit.objects.filter(school=invoice.school).__len__() <= 0:
                    AccessToEdit.objects.create(school=invoice.school)

                acces = AccessToEdit.objects.filter(school=invoice.school)[0]

                if acces.date_invoice > invoice.date:
                    return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                    status=status.HTTP_403_FORBIDDEN)

                invoice.deleted = request.data['set_status']
                invoice.save()
                data = {}

                if acces.date_invoice > invoice.date:
                    invoice.editable = False

                data['invoice'] = serializers.GetSchoolTitulFullSerializer(invoice).data

                return Response(data, status=status.HTTP_201_CREATED)

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class SchoolTitulPlannedAPI(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    # permission_classes = [IsAuthenticated | s_permissions.HeadlibrianPermission]
    permission_classes = [IsAuthenticated | s_permissions.HeadlibrianPermissionByPosition]

    def my_school_ids_list(self, request):
        my_scools = my_school_list(request.user)
        school_ids_list = list(my_scools.values_list('school_id', flat=True).distinct())
        return school_ids_list

    def get(self, request):
        if request.GET.get('e_invoices'):

            serializer = serializers.GetSchoolTitulPlannedFullSerializer
            titul = models.SchoolTitulPlannedHead.objects.get(pk=request.GET['e_invoices'])
            if AccessToEdit.objects.filter(school=titul.school).__len__() <= 0:
                AccessToEdit.objects.create(school=titul.school)
            acces = AccessToEdit.objects.filter(school=titul.school)[0]

            if acces.date_invoice > titul.date:
                titul.editable = False

            # titul.students = models.SchoolTitul.objects.filter(titul_head=titul)

            data = {'invoice': serializer(titul).data}

            return Response(data=data)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        school_ids_list = self.my_school_ids_list(request)

        if 'create_i' in request.data:

            data = request.data['create_i']
            data['date'] = timezone.now().date()
            data['status'] = True
            if 'school' in data \
                    and not data['school'] in school_ids_list:
                return Response({'errors': 'Запрещено создавать документ в не своем учебном заведении'},
                                status=status.HTTP_403_FORBIDDEN)

            if AccessToEdit.objects.filter(school_id=data['school']).__len__() <= 0:
                AccessToEdit.objects.create(school_id=data['school'],
                                            edit_status=1,
                                            date_invoice=datetime.date(2021, 4, 1))

            acces = AccessToEdit.objects.filter(school_id=data['school'])[0]

            if (acces.date_invoice) > data['date']:
                return Response({'errors': 'Запрещено создавать документ в закрытом периоде'},
                                status=status.HTTP_403_FORBIDDEN)

            # data['school'] = request.user.libraryuser.school.id
            serializer = serializers.PostSchoolTitulPlannedFullSerializer(data=data)

            if serializer.is_valid():
                serializer.save()

                s = serializer.data
                invoice = models.SchoolTitulPlannedHead.objects.get(pk=s['id'])
                if 'titul' in data:
                    invoice.titul_id = int(data['titul'])
                    invoice.percent = int(data['percent'])
                    invoice.save()
                if acces.date_invoice > invoice.date:
                    invoice.editable = False

                # invoice.students = models.SchoolTitul.objects.filter(titul_head=invoice)
                ret_data = serializers.GetSchoolTitulPlannedFullSerializer(invoice).data

                return Response(ret_data, status=status.HTTP_200_OK)

        elif request.data.get('ready'):
            titul = models.SchoolTitulPlannedHead.objects.get(pk=request.data.get('ready'))
            if AccessToEdit.objects.filter(school=titul.school).__len__() <= 0:
                AccessToEdit.objects.create(school=titul.school)

            acces = AccessToEdit.objects.filter(school=titul.school)[0]

            if titul.school.id in school_ids_list:
                if request.data.get('status_r'):
                    invoice_data = request.data.get('invoice')
                    if acces.date_invoice > titul.date:
                        return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                        status=status.HTTP_403_FORBIDDEN)

                    # invoice_data['school'] = request.user.libraryuser.school.id
                    invoice_data['status'] = False

                    serializer = serializers.PostSchoolTitulPlannedFullSerializer(titul, data=invoice_data)
                    if serializer.is_valid():
                        serializer.save()
                        models.SchoolTitul.objects.filter(titul_head=serializer.instance).delete()

                    data = serializer.data
                    if acces.date_invoice > titul.date:
                        titul.editable = False
                    # titul.students = models.SchoolTitul.objects.filter(titul_head=titul)
                    ret_data = serializers.GetSchoolTitulPlannedFullSerializer(titul).data

                    return Response(ret_data, status=status.HTTP_200_OK)

                else:
                    invoice_data = request.data.get('invoice')

                    if acces.date_invoice > titul.date:
                        return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                        status=status.HTTP_403_FORBIDDEN)

                    invoice_data['status'] = True
                    serializer = serializers.PostSchoolTitulPlannedFullSerializer(titul, data=invoice_data)

                    if serializer.is_valid():
                        serializer.save()
                        #  models.SchoolTitulPla.objects.filter(titul_head=serializer.instance).delete()

                        if acces.date_invoice > titul.date:
                            titul.editable = False

                        ret_data = serializers.GetSchoolTitulPlannedFullSerializer(titul).data

                        return Response(ret_data, status=status.HTTP_200_OK)

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        elif 'deleted' in request.data:
            if request.user.groups.filter(id=6).exists() \
                    or AccessToEdit.objects.filter(school_id__in=school_ids_list,
                                                   edit_status=1).exists():

                invoice = models.SchoolTitulPlannedHead.objects.get(pk=request.data['deleted'],
                                                                    school__in=school_ids_list)
                if AccessToEdit.objects.filter(school=invoice.school).__len__() <= 0:
                    AccessToEdit.objects.create(school=invoice.school)

                acces = AccessToEdit.objects.filter(school=invoice.school)[0]

                # if acces.date_invoice > invoice.date:
                #     return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                #                     status=status.HTTP_403_FORBIDDEN)

                invoice.deleted = request.data['set_status']
                invoice.save()
                data = {}

                if acces.date_invoice > invoice.date:
                    invoice.editable = False

                data['invoice'] = serializers.GetSchoolTitulPlannedFullSerializer(invoice).data

                return Response(data, status=status.HTTP_201_CREATED)

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def users_by_school(request):
    if request.method == 'GET':

        data = {}
        user = request.user
        schools = p_models.AlmaMater.objects.all()

        if not request.user.is_superuser:
            schools_from_wtl = user_utils.user_schools(user).values_list('school', flat=True)
            schools = schools.filter(pk__in=schools_from_wtl)

        school = request.GET.get('id')
        schools = schools.filter(pk=school)
        work_places = p_models.PortfolioWorkTimeLine.objects.filter(current=True,
                                                                    portfolio__deleted=False,
                                                                    deleted=False,
                                                                    checked=True,
                                                                    school__in=schools)

        work_places = work_places.values_list('portfolio', flat=True)

        portfolios = p_models.Portfolio.objects.select_related('user').filter(pk__in=work_places).distinct()
        portfolios = portfolios.order_by('name_ru')
        data['users'] = serializers.PortfolioSerializers(portfolios, many=True).data

        return JsonResponse(data)


@api_view(["GET"])
def school_titul_list(request):
    if request.method == 'GET':
        try:
            data = {}
            user = request.user
            schools = user_utils.user_schools(user)

            data['warning'] = False

            if user.is_superuser:
                snippets = models.SchoolTitulHead.objects.filter(school__nash=True)

                if 'school' in request.query_params:
                    snippets = snippets.filter(school_id__in=request.query_params['school'].split(','))
                else:
                    snippets = snippets.filter(school_id__in=[])
            else:
                snippets = models.SchoolTitulHead.objects.filter(school__in=schools.values_list('school', flat=True),
                                                                 deleted=False)

            snippets = snippets.order_by('deleted',
                                         '-year',
                                         'klass',
                                         'liter_id').select_related('school',
                                                                    'kurator',
                                                                    'kurator__portfolio')

            work_places = p_models.PortfolioWorkTimeLine.objects.filter(current=True,
                                                                        portfolio__deleted=False,
                                                                        deleted=False,
                                                                        checked=True, )
            # if not request.user.is_superuser:
            work_places = work_places.filter(school__in=schools.values_list('school',
                                                                            flat=True))

            work_places = work_places.values_list('portfolio', flat=True)

            portfolios = p_models.Portfolio.objects.filter(pk__in=work_places).distinct().order_by('name_ru')
            data['users'] = serializers.PortfolioSerializers(portfolios, many=True).data
            data['liters'] = serializers.LiterSerializers(Liter.objects.filter(deleted=False), many=True).data
            data['data'] = serializers.GetHeadSchoolTitulSerializer(snippets, many=True).data
            data['languages'] = serializers.LanguageSerializer(p_models.Language.objects.filter(deleted=False),
                                                               many=True).data
            data['studyDirections'] = serializers.StudyDirectionsSerializer(
                StudyDirections.objects.filter(deleted=False), many=True).data
            data['klasss'] = serializers.KlassSerializersID(p_models.Klass.objects.filter(deleted=False, klass_type=2),
                                                            many=True).data
            data['datas'] = serializers.DateObjectsSerializer(
                p_models.DateObjects.objects.filter(deleted=False, id=9).order_by('id'), many=True).data
            return JsonResponse(data)

        except AccessToEdit.DoesNotExist:
            return JsonResponse({'errors': 'Нет доступа', 'warning': 0}, status=400)


def get_data(school, params):
    start_year = params['year']
    st = models.SchoolTitulHead.objects.filter(deleted=False,
                                               school=school,
                                               year=start_year)
    st = st.values('study_direction',
                   'id',
                   'language',
                   #   'klass',
                   'klass__sort', 'comment',
                   'liter',
                   'students')

    if 'from_planned' in params and params['from_planned'] == 'true':
        st = models.SchoolTitulPlannedHead.objects.filter(deleted=False,
                                                          school=school,
                                                          year=start_year)
        st = st.values('study_direction',
                       # 'id',
                       'language',
                       #   'klass',
                       'klass__sort', 'comment',
                       'liter',
                       'students')
    st = st.order_by(
        'klass__sort',
        'liter__sort',
        'study_direction__sort'
    )
    klasss = p_models.Klass.objects.filter(klass_type=2,
                                           deleted=False).order_by('sort')

    klasss = list(klasss.values('id',
                                'sort'))
    st = list(st)
    fin = []

    for item in st:

        item['klass'] = None

        for kl in klasss:
            if item['klass__sort'] < kl['sort']:
                item['klass'] = kl['id']

                break

        if not item['klass'] is None:
            fin.append(item)

    return fin


@api_view(["GET"])
def school_titul_planned_list(request):
    if request.method == 'GET':
        try:
            data = {}
            user = request.user
            schools = user_utils.user_schools(user)

            data['warning'] = False

            if user.is_superuser:
                snippets = models.SchoolTitulPlannedHead.objects.filter(school__nash=True)
                if 'school' in request.query_params:
                    snippets = snippets.filter(school_id__in=request.query_params['school'].split(','))
                else:
                    snippets = snippets.filter(school_id__in=[])
            else:
                snippets = models.SchoolTitulPlannedHead.objects.filter(
                    school__in=schools.values_list('school', flat=True), deleted=False)

            snippets = snippets.order_by('deleted', '-year', 'klass', 'liter_id')

            work_places = p_models.PortfolioWorkTimeLine.objects.filter(current=True,
                                                                        portfolio__deleted=False,
                                                                        deleted=False,
                                                                        checked=True,
                                                                        )
            # if not request.user.is_superuser:
            work_places = work_places.filter(school__in=schools.values_list('school',
                                                                            flat=True))

            work_places = work_places.values_list('portfolio', flat=True)

            portfolios = p_models.Portfolio.objects.filter(pk__in=work_places).distinct().order_by('name_ru')
            data['users'] = serializers.PortfolioSerializers(portfolios, many=True).data
            data['liters'] = serializers.LiterSerializers(Liter.objects.filter(deleted=False), many=True).data
            data['data'] = serializers.GetHeadSchoolTitulPlannedSerializer(snippets, many=True).data
            data['languages'] = serializers.LanguageSerializer(p_models.Language.objects.filter(deleted=False),
                                                               many=True).data
            data['studyDirections'] = serializers.StudyDirectionsSerializer(
                StudyDirections.objects.filter(deleted=False),
                many=True).data
            data['klasss'] = serializers.KlassSerializersID(p_models.Klass.objects.filter(deleted=False, klass_type=2),
                                                            many=True).data
            data['datas'] = serializers.DateObjectsSerializer(
                p_models.DateObjects.objects.filter(deleted=False).order_by('id'), many=True).data
            return JsonResponse(data)

        except AccessToEdit.DoesNotExist:
            return JsonResponse({'errors': 'Нет доступа', 'warning': 0}, status=400)


@api_view(["GET"])
def goto_webinar(request):
    context = {}

    # get_top_string(request,context)

    if not request.user.is_authenticated:
        return HttpResponseForbidden('Не авторизованы в Ekitaphana')

    webinars = p_models.Webinar.objects.filter(finished=False)

    context['has_webinar'] = False

    if webinars.__len__() > 0 and request.user.is_authenticated:

        webinar = webinars[0]

        if webinar.for_all:
            context['has_webinar'] = True

        if webinar.for_zavuch and request.user.almamater_set.filter(nash=True).count() > 0:
            context['has_webinar'] = True

        if webinar.for_region_otv and p_models.AlmaMater.objects.filter(school_type__infocode__in=[1, 2],
                                                                        user=request.user).exists():
            context['has_webinar'] = True

        if request.user.is_superuser:
            context['has_webinar'] = True

    webinar = None

    if webinars.__len__() > 0 and context['has_webinar']:
        webinar = webinars[0]
    else:
        return HttpResponse('Нет открытых вебинаров')

    moders = webinar.moderator.split(',')

    if request.user.email in moders:
        role = '1'
    else:
        role = '0'
    conf_id = webinar.webinar_id
    from ekitaphana.settings import SITE_SERVER
    url = u'https://bilimgo.biz/wwwsmeetings/make_from_eportfolio/?salt=adafgjhDavs4fdwgsvajswlklkwk' \
          + u'&first_name=' + request.user.first_name \
          + u'&last_name=' + request.user.last_name \
          + u'&role=' + role \
          + u'&conf_id=' + conf_id \
          + u'&logout_url=' + SITE_SERVER

    import requests, json
    r = requests
    req = r.get(url)

    return redirect(json.loads(req.text)['target'])


@api_view(["GET"])
def has_webinar(request):
    context = {}

    # get_top_string(request,context)

    if not request.user.is_authenticated:
        return JsonResponse({'data': False})

    webinars = p_models.Webinar.objects.filter(finished=False)

    context['has_webinar'] = False

    if webinars.__len__() > 0 and request.user.is_authenticated:

        webinar = webinars[0]

        if webinar.for_all:
            context['has_webinar'] = True

        if webinar.for_zavuch and request.user.almamater_set.filter(nash=True).count() > 0:
            context['has_webinar'] = True

        if webinar.for_region_otv and p_models.AlmaMater.objects.filter(school_type__infocode__in=[1, 2],
                                                                        user=request.user).exists():
            context['has_webinar'] = True

        if request.user.is_superuser:
            context['has_webinar'] = True

    return JsonResponse({'data': context['has_webinar']})


@api_view(["GET"])
def school_titul_planned_build(request):
    if request.method == 'GET':
        try:
            data = {}
            user = request.user
            schools = user_utils.user_schools(user)

            data['warning'] = False

            if user.is_superuser:
                snippets = models.SchoolTitulPlannedHead.objects.filter(school__nash=True)
            else:
                snippets = models.SchoolTitulPlannedHead.objects.filter(
                    school__in=schools.values_list('school', flat=True))

            snippets = snippets.order_by('deleted', '-year', 'klass')

            work_places = p_models.PortfolioWorkTimeLine.objects.filter(current=True,
                                                                        portfolio__deleted=False,
                                                                        deleted=False,
                                                                        checked=True,
                                                                        )
            work_places = work_places.filter(school=request.query_params['school'])
            # if not request.user.is_superuser:
            work_places = work_places.filter(school__in=schools.values_list('school',
                                                                            flat=True))

            work_places = work_places.values_list('portfolio', flat=True)

            portfolios = p_models.Portfolio.objects.filter(pk__in=work_places).distinct().order_by('name_ru')
            data['users'] = serializers.PortfolioSerializers(portfolios, many=True).data
            data['liters'] = serializers.LiterSerializers(Liter.objects.filter(deleted=False), many=True).data
            #  data['data'] = serializers.GetHeadSchoolTitulPlannedSerializer(snippets, many=True).data

            data['languages'] = serializers.LanguageSerializer(p_models.Language.objects.filter(deleted=False),
                                                               many=True).data
            data['studyDirections'] = serializers.StudyDirectionsSerializer(
                StudyDirections.objects.filter(deleted=False),
                many=True).data
            data['klasss'] = serializers.KlassSerializersID(p_models.Klass.objects.filter(deleted=False, klass_type=2),
                                                            many=True).data
            data['datas'] = serializers.DateObjectsSerializer(
                p_models.DateObjects.objects.filter(deleted=False).order_by('id'), many=True).data

            data['data'] = get_data(work_places.values_list('school', flat=True).first(), request.query_params)

            return JsonResponse(data)

        except AccessToEdit.DoesNotExist:
            return JsonResponse({'errors': 'Нет доступа', 'warning': 0}, status=400)


def cached_api_briefcases(lang):
    cache_name = 'briefcases' + lang
    data = cache.get(cache_name)
    if data is None:
        data = {}
        data['years'] = DateObjectsSerializer(p_models.DateObjects.objects.all(), many=True).data
        data['languages'] = serializers.LanguageSerializer(
            p_models.Language.objects.all().order_by('name_' + lang), many=True).data
        data['klasses'] = serializers.KlassSerializersID(p_models.Klass.objects.filter(klass_type=2), many=True).data
        data['liters'] = serializers.LiterSerializers(Liter.objects.all(), many=True).data
        # тут вставляется Id
        data['editions'] = serializers.EditionSerializerA(
            Edition.objects.all().order_by('name'), many=True).data
        data['studyDirections'] = serializers.StudyDirectionsSerializer(StudyDirections.objects.all(),
                                                                        many=True).data
        cache.set(cache_name, data, 2592000)
    return data


class BriefcaseAPI(APIView):
    # permission_classes = [AccessPermission]
    authentication_classes = [BasicAuthentication, TokenAuthentication, SessionAuthentication]

    def get(self, request, format=None):
        data = {}
        user = request.user
        schools = user_utils.user_schools(user)
        schools = schools.values_list('school', flat=True)
        if user.is_superuser:
            schools = p_models.AlmaMater.objects.filter(nash=True)
        # try:
        #     data = {}
        #     user = request.user
        #     if not user.groups.filter(id=6).exists():
        #         if AccessToEdit.objects.get(school=user.libraryuser.school).edit_status > 0:
        #             data['worning'] = False
        #         else:
        #             data['worning'] = True
        #     else:
        #         data['worning'] = False
        # except AccessToEdit.DoesNotExist:
        #     return JsonResponse({'errors': 'Нет доступа'}, status=400)

        if request.GET.get('briefcase'):
            data['invoices'] = BriefcaseSerializers(Briefcase.objects.filter(school__in=schools).order_by('deleted',
                                                                                                          '-year',
                                                                                                          'klass'),
                                                    many=True).data
            if not request.user.is_superuser:
                qs = Briefcase.objects.filter(school__in=schools,
                                              deleted=False).order_by('deleted',
                                                                      '-year',
                                                                      'klass')
                if request.GET.get('typeDoc'):
                    if request.GET.get('typeDoc') == 'pt':
                        ob = models.SchoolTitulPlannedHead.objects.get(pk=request.GET.get('docId'))

                    qs = qs.filter(klass=ob.klass,
                                   school=ob.school,
                                   study_direction=ob.study_direction,
                                   language=ob.language,
                                   year=ob.year)

                data['invoices'] = BriefcaseSerializers(qs, many=True).data
            snippets = PlannedTitle.objects.filter(school=user.libraryuser.school, deleted=False).order_by('klass')
            data['klasses'] = SchoolTitulListSerializer(snippets, many=True).data
            data['liters'] = serializers.LiterSerializers(Liter.objects.all(), many=True).data
            data['languages'] = serializers.LanguageSerializer(p_models.Language.objects.all(), many=True).data
            data['studyDirections'] = serializers.StudyDirectionsSerializer(StudyDirections.objects.all(),
                                                                            many=True).data
            data['class_list'] = serializers.KlassSerializersID(p_models.Klass.objects.filter(klass_type=2),
                                                                many=True).data
            data['datas'] = serializers.DateObjectsSerializer(
                p_models.DateObjects.objects.filter(year_number__gte=2021).order_by('year_number'), many=True).data

        if request.GET.get('get_create'):
            data = cached_api_briefcases(lang=translation.get_language())

        if request.GET.get('e_invoices'):
            # data = cached_api_briefcases(lang=translation.get_language())
            bc = Briefcase.objects.get(id=request.GET['e_invoices'], school__in=schools)
            # acces = AccessToEdit.objects.filter(
            #     school_id=request.user.libraryuser.school.id)[0]
            # if acces.date_invoice > bc.date:
            bc.editable = True
            data['invoice'] = BriefcaseSerializersSchoolID(bc).data
            # data['beditions'] = EditionBriefcaseSerializers(
            #     EditionBriefcase.objects.filter(briefcase__id=request.GET['get_briefcase']), many=True).data

        if request.GET.get('editions_teacher'):
            plan_t = PlanEditionTeacher.objects.filter(school__id=user.libraryuser.school.id)
            data = cached_api_briefcases(lang=translation.get_language())
            data['teacherEditions'] = GetPlanEditionTeacherSerializer(plan_t, many=True).data
        return Response(data)

    def post(self, request, format=None):
        acces = AccessToEdit.objects.filter(
            school_id=request.user.libraryuser.school.id)[0]
        # user = User.objects.get(auth_token=request.data['token'])

        user = request.user
        schools = user_utils.user_schools(user)
        schools = schools.values_list('school', flat=True)

        if user.is_superuser:
            schools = p_models.AlmaMater.objects.filter(nash=True).values_list('id', flat=True)

        if 'pt' in request.data:

            pt = None
            bss = models.Briefcase.objects.filter(school__in=schools,
                                                  pk=request.data.get('pt')['bc'])
            if len(bss) == 0:
                return Response("No school",
                                status=status.HTTP_400_BAD_REQUEST)

            pts = models.SchoolTitulPlannedHead.objects.filter(pk=request.data.get('pt')['pt'],
                                                               school__in=schools)
            if len(pts) == 0:
                return Response("No school",
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                pt = pts[0]

            pt.briefcase_id = int(request.data.get('pt')['bc'])
            pt.save()

            return Response(data='ok', status=status.HTTP_201_CREATED)

        if 'create_i' in request.data:
            briefcase = request.data['create_i']
            if not briefcase['school'] in schools:
                return Response("No school", status=status.HTTP_400_BAD_REQUEST)
            briefcase['status'] = True
            if not 'description' in briefcase:
                briefcase['description'] = ''

            briefcase['description'] = briefcase['description'].lstrip().rstrip()
            briefcase['school'] = briefcase['school']
            briefcase['author'] = user.id
            briefcase['name'] = p_models.Klass.objects.get(
                pk=briefcase['klass']).name + ' ' + p_models.Language.objects.get(pk=briefcase['language']).name + ' ' + \
                                briefcase['description']

            bc = Briefcase.objects.filter(
                language=briefcase['language'],
                klass=briefcase['klass'],
                school=briefcase['school'],
                study_direction=briefcase['study_direction'])

            if (len(bc) > 0):
                return JsonResponse({'error': True, 'status': 'has', 'id': bc[0].id})

            else:
                serializer = PostBriefcaseSerializers(data=briefcase)
                if serializer.is_valid():
                    serializer.save()
                    # serializer.instance.editions_invoice.all().delete()

                    for item in serializer.initial_data['editions_val']:
                        edition = EditionBriefcase()
                        edition.briefcase = serializer.instance
                        edition.surplus = item['surplus']
                        edition.edition = Edition.objects.get(pk=item['edition'])
                        edition.save()

                    serializer.instance.save()

                    ret_data = BriefcaseSerializers(instance=serializer.instance).data
                    return Response(data=ret_data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.data.get('ready'):

            try:
                invoice = Briefcase.objects.get(pk=request.data.get('ready'), school__in=schools)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)

            if invoice.school.id == request.user.libraryuser.school.id or True:
                invoice_data = request.data.get('invoice')

                try:
                    invoice_data['school'] = invoice_data['school']['school_id']
                except:
                    pass
                bc = Briefcase.objects.filter(
                    language=invoice_data['language'],
                    klass=invoice_data['klass'],
                    school=invoice_data['school'],
                    study_direction=invoice_data['study_direction']).exclude(pk=invoice_data['id'])

                if len(bc) > 0:
                    return JsonResponse({'error': True, 'status': 'has', 'id': bc[0].id})

                if request.data.get('status_r'):

                    if acces.date_invoice > invoice.date:
                        return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                        status=status.HTTP_403_FORBIDDEN)
                    # invoice_data['school'] = invoice.school.id
                    # invoice_data['author'] = request.user.id
                    invoice_data['status'] = False
                    serializer = PostBriefcaseSerializers(
                        invoice, data=invoice_data)
                    if serializer.is_valid():
                        serializer.save()
                        serializer.instance.editions_val.delete()
                        for item in serializer.initial_data['editions_val']:
                            edition = EditionBriefcase()
                            edition.briefcase = serializer.instance
                            edition.surplus = item['surplus']
                            edition.edition = Edition.objects.get(pk=item['edition'])
                            edition.save()
                        ret_data = BriefcaseSerializers(instance=serializer.instance).data
                        return Response(data=ret_data, status=status.HTTP_201_CREATED)
                else:
                    # invoice_data = request.data.get('invoice')
                    if acces.date_invoice > invoice.date:
                        return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                        status=status.HTTP_403_FORBIDDEN)
                    # invoice_data['school'] = invoice.school.id
                    # invoice_data['author'] = request.user.id
                    invoice_data['status'] = True
                    serializer = PostBriefcaseSerializers(
                        invoice, data=invoice_data)
                    if serializer.is_valid():
                        serializer.save()
                        serializer.instance.editions_val.delete()
                        for item in serializer.initial_data['editions_val']:
                            edition = EditionBriefcase()
                            edition.briefcase = serializer.instance
                            edition.surplus = item['surplus']
                            edition.edition = Edition.objects.get(pk=item['edition'])
                            edition.save()
                        ret_data = BriefcaseSerializers(instance=serializer.instance).data
                        return Response(data=ret_data, status=status.HTTP_201_CREATED)
                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST)


            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'deleted' in request.data:
            # if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
            #         school_id=request.user.libraryuser.school.id, edit_status=1).exists():
            try:
                invoice = Briefcase.objects.get(pk=request.data['deleted'],
                                                school__in=schools)
                invoice.deleted = request.data['set_status']
                invoice.save()
                data = BriefcaseSerializers(invoice).data
                return Response(data, status=status.HTTP_201_CREATED)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # if acces.date_invoice > invoice.date:
            #     return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
            #                     status=status.HTTP_403_FORBIDDEN)

        if request.data.get('add_briefcase'):
            try:
                param = request.data['add_briefcase']

                plan_title = get_object_or_404(PlannedTitle, pk=param['plan_titul'])
                briefcase = get_object_or_404(Briefcase, pk=param['briefcase'])
                plan_title.briefcase = briefcase
                plan_title.save()
                briefcase = BriefcaseSerializers(briefcase)
                return Response(briefcase.data, status=status.HTTP_201_CREATED)
            except PlannedTitle.DoesNotExist:
                return JsonResponse({'errors': 'Ошибка добавления'}, status=400)

        if request.data.get('teacher_editions'):
            editions = request.data['teacher_editions']
            for edition in editions:
                edition['school'] = user.libraryuser.school.id
                edition['author'] = user.id
            serializer = PostPlanEditionTeacherSerializer(data=editions, many=True)
            if serializer.is_valid():
                serializer.save()
                serializer = GetPlanEditionTeacherSerializer(
                    PlanEditionTeacher.objects.filter(school=user.libraryuser.school), many=True).data
                return Response(serializer, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        if request.GET.get('edition'):
            snippet = EditionBriefcase.objects.get(id=request.GET.get('edition'))
            snippet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if request.GET.get('teacher_edition'):
            snippet = PlanEditionTeacher.objects.get(id=request.GET.get('teacher_edition'))
            snippet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if request.GET.get('param'):
            snippet = PlannedTitle.objects.get(id=request.GET.get('param'))
            snippet.briefcase = None
            snippet.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if request.GET.get('briefcase'):
            user = User.objects.get(auth_token=request.headers['Token'])
            snippet = Briefcase.objects.get(id=request.GET.get('briefcase'))
            snippet.delete()
            serializer = SchoolTitulListSerializer(PlannedTitle.objects.filter(school=user.libraryuser.school),
                                                   many=True).data
            return JsonResponse({"data": serializer}, status=200)

        return JsonResponse({'errors': 'Нет доступа'}, status=400)


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


class ImportBooksList(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        if not request.user.is_superuser and not request.user.groups.filter(id=6).exists():
            return HttpResponseForbidden('forbidden')
        # data = ast.literal_eval(request.data.data)
        data = request.data['data']
        hz = 0
        for i in data:
            try:
                e = Edition.objects.get(pk=int(i['id']))
            except:
                e = Edition()
                if not int(i['id']) == 0:
                    e.id = int(i['id'])
            #   print(i['subject'])
            e.klass = p_models.Klass.objects.get_or_create(name_ru=i['klass'])[0]

            try:
                e.subject = p_models.Subject.objects.filter(name_ru=i['subject'].strip()).order_by('id')[0]
            except:
                e.subject = p_models.Subject.objects.get_or_create(name_ru=i['subject'].strip())[0]

            try:
                e.language = p_models.Language.objects.filter(name_ru=i['language'].strip()).order_by('id')[0]
            except:
                e.language = p_models.Language.objects.get_or_create(name_ru=i['language'].strip())[0]

            try:
                e.metodology_complex = \
                    models.UMK.objects.filter(name_ru=i['metodology_complex'].strip()).order_by('id')[0]
            except:
                e.metodology_complex = models.UMK.objects.get_or_create(name_ru=i['metodology_complex'].strip())[0]

            e.study_direction = models.StudyDirections.objects.get_or_create(name_ru=i['study_direction'].strip())[0]
            e.name = i['name'].strip()

            if 'isbn' in i:
                e.isbn = i['isbn']
            try:
                e.publisher = \
                    library_models.PublisherEdition.objects.filter(name_ru=i['publisher'].strip()).order_by('id')[0]
            except:
                e.publisher = library_models.PublisherEdition.objects.get_or_create(name_ru=i['publisher'].strip())[0]

            try:
                e.author = models.AuthorEdition.objects.filter(name=i['author'].strip()).order_by('id')[0]
            except:
                e.author = models.AuthorEdition.objects.get_or_create(name=i['author'].strip())[0]

            #
            # e.author = models.AuthorEdition.objects.get_or_create(name=i['author'].strip())[0]

            if 'publish_date' in i:
                try:
                    e.publish_date = models.Year.objects.filter(year=i['publish_date']).order_by('id')[0]
                except:
                    print(i['publish_date'])
                    e.publish_date = models.Year.objects.get_or_create(year=i['publish_date'])[0]

            try:
                e.amount = float(i['amount'])
            except:
                e.amount = 0

            try:
                e.funding_cycle = models.FundingСycle.objects.get_or_create(name_ru=i['funding_cycle'].strip())[0]
            except:
                e.funding_cycle = None
            e.save()
            print(hz)
            hz = hz + 1
        cache.set('all_editions_for_api', None)
        return Response(data={'status': 'ok'}, status=status.HTTP_200_OK)


class ImportOst(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        if not request.user.is_superuser:
            return HttpResponseForbidden('forbidden')
        # data = ast.literal_eval(request.data.data)
        data = request.data['data']

        for i in data:
            e = EditionInitialBalance()
            e.edition_id = int(i['edition_id'])
            e.invoice_id = int(i['invoice_id'])
            e.quantity = float(i['quantity'])
            e.amount = float(i['amount'])

            # e.language = p_models.Language.objects.get_or_create(name_ru=i['language'].strip())[0]
            # e.metodology_complex = models.UMK.objects.get_or_create(name_ru=i['metodology_complex'].strip())[0]
            # e.study_direction = models.StudyDirections.objects.get_or_create(name_ru=i['study_direction'].strip())[0]
            # e.name = i['name'].strip()
            # e.publisher = library_models.PublisherEdition.objects.get_or_create(name_ru=i['publisher'].strip())[0]
            # e.author = models.AuthorEdition.objects.get_or_create(name=i['author'].strip())[0]
            # e.publish_date = models.Year.objects.get_or_create(year=i['publish_date'])[0]
            # e.amount = float(i['amount'])
            # e.funding_cycle = models.FundingСycle.objects.get_or_create(name_ru=i['funding_cycle'].strip())[0]
            e.save()

        return Response(data={'status': 'ok'}, status=status.HTTP_200_OK)


class SchoolTitullList(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        context = {}
        user = request.user
        tituls = models.SchoolTitul.objects.filter(school=user.libraryuser.school.id)
        if 'year' in request.GET:
            year = p_models.DateObjects.objects.get(pk=request.GET['year'])
            tituls.filter(year=year)
        serializer = serializers.GlobalSchoolTitulSerializer
        context['tituls'] = serializer(tituls, many=True).data
        return Response(data=context)


class AdminBooksMoving(APIView):
    permission_classes = [s_permissions.HeadlibrianPermission | s_permissions.SuperUserPermission]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        if request.GET.get('all_invoices'):
            reords = models.BooksMovingHead.objects.all()
            serializer = serializers.AdminBookMovingSerializer
            data = serializer(reords, many=True).data
            return Response(data=data)
        elif request.GET.get('e_invoices'):
            invoice = models.BooksMovingHead.objects.get(pk=request.GET.get('e_invoices'))
            context = {}
            context['invoice'] = serializers.AdminDetailBookMovingSerializer(invoice).data
            return Response(data=context)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        if request.data.get('ready'):
            invoice = models.BooksMovingHead.objects.get(pk=request.data.get('ready'))
            if request.data.get('status_r'):
                invoice.status = False
            else:
                invoice.status = True
            invoice.save()
            ret_data = serializers.AdminDetailBookMovingSerializer(invoice).data
            return Response(data=ret_data, status=status.HTTP_201_CREATED)
        # elif 'deleted' in request.data:
        #     invoice = models.BooksMovingHead.objects.get(pk=request.data['deleted'])
        #     invoice.deleted = request.data['set_status']
        #     invoice.save()
        #     ret_data = serializers.AdminBookMovingSerializer(invoice).data
        #     return Response(ret_data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class BooksMoving(APIView):
    permission_classes = [IsAuthenticated, s_permissions.HeadlibrianPermission]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        if request.GET.get('all_invoices'):
            recipient_query = models.BooksMovingHead.objects.filter(recipient_school=request.user.libraryuser.school)
            sender_query = models.BooksMovingHead.objects.filter(sender_school=request.user.libraryuser.school)
            reords = recipient_query | sender_query
            serializer = serializers.AdminBookMovingSerializer
            data = serializer(reords, many=True).data
            return Response(data=data)
        elif request.GET.get('e_invoices'):
            invoice = models.BooksMovingHead.objects.get(pk=request.GET.get('e_invoices'))
            context = {}
            context['invoice'] = serializers.AdminDetailBookMovingSerializer(invoice).data
            return Response(data=context)

        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def cat_ver(request):
    ob = models.CatVer.objects.last()
    if ob is None:
        ob = models.CatVer()
        ob.save()
    return Response(str(ob.ver))


@api_view(["GET"])
def when_ready(request):
    return Response(str(wh_ready))
