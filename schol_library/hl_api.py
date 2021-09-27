from account.models import AccessToEdit

from ekitaphana.settings import BASE_1C_PATH
from django.core.cache import cache
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import translation
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from portfoli import models as p_models
from .b_case_serializers import BriefcaseSerializers, PostEditionBriefcaseSerializers, PostBriefcaseSerializers, \
    EditionBriefcaseSerializers, SchoolTitulListSerializer, PostPlanEditionTeacherSerializer, \
    GetPlanEditionTeacherSerializer
from .models import SchoolTitul, PlannedTitle, Edition, Briefcase, EditionBriefcase, Liter, StudyDirections, \
    PlanEditionTeacher, NumberBooks
from .serializers import PlanSchoolTitulSerializers, PostPlanSchoolTitulSerializers, \
    ListPlanSchoolTitulSerializers, DateObjectsSerializer, PostPlanSchoolTitulDetailSerializers
from schol_library import b_case_serializers
from schol_library import serializers
import math
import httplib2
from django.http import HttpResponse
from .permissions import AccessPermission, AccessPermissionS12, HeadlibrianPermission
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from django.utils import timezone

def cached_api(lang):
    cache_name = 'titul' + lang
    data = cache.get(cache_name)
    if data is None:
        data = {}
        data['years'] = DateObjectsSerializer(p_models.DateObjects.objects.all(), many=True).data
        data['languages'] = serializers.LanguageSerializer(
            p_models.Language.objects.all().order_by('name_' + lang), many=True).data
        data['klasses'] = serializers.KlassSerializersID(p_models.Klass.objects.all(), many=True).data
        data['liters'] = serializers.LiterSerializers(Liter.objects.all(), many=True).data
        data['editions'] = serializers.EditionSerializerA(
            Edition.objects.all().order_by('name'), many=True).data
        data['studyDirections'] = serializers.StudyDirectionsSerializer(StudyDirections.objects.all(),
                                                                        many=True).data
        cache.set(cache_name, data, 2592000)
    return data


def cached_api_briefcases(lang):
    cache_name = 'briefcases' + lang
    data = cache.get(cache_name)
    if data is None:
        data = {}
        data['years'] = DateObjectsSerializer(p_models.DateObjects.objects.all(), many=True).data
        data['languages'] = serializers.LanguageSerializer(
            p_models.Language.objects.all().order_by('name_' + lang), many=True).data
        data['klasses'] = serializers.KlassSerializersID(p_models.Klass.objects.all(), many=True).data
        data['liters'] = serializers.LiterSerializers(Liter.objects.all(), many=True).data
        # тут вставляется Id
        data['editions'] = serializers.EditionSerializerA(
            Edition.objects.all().order_by('name'), many=True).data
        data['studyDirections'] = serializers.StudyDirectionsSerializer(StudyDirections.objects.all(),
                                                                        many=True).data
        cache.set(cache_name, data, 2592000)
    return data


# Формирование планого титульного списка школы
class PlannedTitleCreateAPI(APIView):
    permission_classes = [AccessPermission]

    def get(self, request, format=None):
        data = cached_api(lang=translation.get_language())
        try:
            user = User.objects.get(auth_token=request.headers['Token'])
            if not user.groups.filter(id=6).exists():
                if AccessToEdit.objects.get(school=user.libraryuser.school).edit_status > 0:
                    data['warning'] = False
                else:
                    data['warning'] = True
            else:
                data['warning'] = False
        except AccessToEdit.DoesNotExist:
            return JsonResponse({'errors': 'Нет доступа'}, status=400)

        if request.method == 'GET':
            year = PlannedTitle.objects.filter(school=self.request.user.libraryuser.school, deleted=False).values_list(
                'year', flat=True)
            data['datas'] = DateObjectsSerializer(p_models.DateObjects.objects.filter(pk__in=year), many=True).data
            year_id = SchoolTitul.objects.filter(school=user.libraryuser.school).values_list('year', flat=True)
            data['school_tituls'] = PlanSchoolTitulSerializers(
                SchoolTitul.objects.filter(
                    school=user.libraryuser.school,
                    deleted=False).order_by('klass'), many=True).data
            data['plan_years'] = DateObjectsSerializer(p_models.DateObjects.objects.filter(id__in=year_id),
                                                       many=True).data
            data['years'] = DateObjectsSerializer(p_models.DateObjects.objects.all(), many=True).data
            return Response(data)

    def post(self, request, format=None):
        user = User.objects.get(auth_token=request.data['token'])
        if user.groups.filter(id__in=[1, 6]).exists():
            serializer = PostPlanSchoolTitulSerializers(data=request.data['school_tituls'], many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse({'error': 'ne proshel validaciu'}, status=401)
        else:
            return JsonResponse({'error': 'ne proshel validaciu'}, status=401)

    def delete(self, request, format=None):
        user = User.objects.get(auth_token=request.headers['Token'])
        if request.GET.get('plan_year'):
            snippets = PlannedTitle.objects.filter(year__id=request.GET.get('plan_year'), deleted=False,
                                                   school=user.libraryuser.school)
            for i in snippets:
                i.deleted = True
                i.save()
            return Response(status=status.HTTP_204_NO_CONTENT)


class PlannedTitleListEditAPI(APIView):
    permission_classes = [AccessPermission]

    def get(self, request, format=None):
        try:
            user = get_object_or_404(User, auth_token=request.headers['Token'])
            AccessToEdit.objects.get(school=user.libraryuser.school)
        except AccessToEdit.DoesNotExist:
            return JsonResponse({'errors': 'Нет доступа'}, status=400)

        if request.method == 'GET':
            if request.GET['pk']:
                year = get_object_or_404(p_models.DateObjects, pk=request.GET['pk'])
                if year:
                    data = {}
                    data['school_tituls'] = PlanSchoolTitulSerializers(
                        PlannedTitle.objects.filter(school=user.libraryuser.school, year=year, deleted=False).order_by(
                            'klass'), many=True).data
                    return Response(data)
                else:
                    return Response({'errors': 'Не указаны данные'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'errors': 'Не указаны данные'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        user = User.objects.get(auth_token=request.data['token'])
        if user.groups.filter(id=1).exists():
            if request.data.get('plan_titul'):
                serializer = b_case_serializers.PlanTitulSerializerInPlan(data=request.data.get('plan_titul'))
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            s = []
            eror = []
            serializers = PostPlanSchoolTitulDetailSerializers(data=request.data['school_tituls'], many=True)
            if serializers.is_valid():
                for serializer in request.data['school_tituls']:
                    plan_title = PlannedTitle.objects.get(id=serializer['id'])
                    serializer = PostPlanSchoolTitulDetailSerializers(plan_title, data=serializer)
                    if serializer.is_valid():
                        serializer.save()
                        s.append(serializer.data)
                    else:
                        eror.append(serializer.data)
                return JsonResponse({'sucses_val': s, 'eror_val': eror}, status=status.HTTP_201_CREATED)
            return JsonResponse({'error': 'не прошел валидацию'}, status=401)
        else:
            return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, format=None):
        if request.GET.get('titul'):
            snippet = PlannedTitle.objects.get(id=request.GET.get('titul'))
            snippet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class ListPlannedTitlesYearAPI(APIView):
    def get(self, request, format=None):
        try:
            user = get_object_or_404(User, auth_token=request.GET['token'])
        except User.DoesNotExist:
            return JsonResponse({'errors': 'Нет доступа'}, status=400)

        if request.method == 'GET':
            serializer = ListPlanSchoolTitulSerializers(PlannedTitle.objects.filter(
                school=user.libraryuser.school,
                year_id=request.GET['pk'],
                deleted=False
            ), many=True)
            return Response(serializer.data)


class BriefcaseAPI(APIView):
    # permission_classes = [AccessPermission]
    authentication_classes = [BasicAuthentication, TokenAuthentication, SessionAuthentication]

    def get(self, request, format=None):
        try:
            data = {}
            user = request.user
            if not user.groups.filter(id=6).exists():
                if AccessToEdit.objects.get(school=user.libraryuser.school).edit_status > 0:
                    data['worning'] = False
                else:
                    data['worning'] = True
            else:
                data['worning'] = False
        except AccessToEdit.DoesNotExist:
            return JsonResponse({'errors': 'Нет доступа'}, status=400)

        if request.GET.get('briefcase'):
            data['invoices'] = BriefcaseSerializers(Briefcase.objects.filter(school=user.libraryuser.school.id).order_by('-id'),
                                                    many=True).data
            snippets = PlannedTitle.objects.filter(school=user.libraryuser.school, deleted=False).order_by('klass')
            data['klasses'] = SchoolTitulListSerializer(snippets, many=True).data
            data['liters'] = serializers.LiterSerializers(Liter.objects.all(), many=True).data
            data['languages'] = serializers.LanguageSerializer(p_models.Language.objects.all(), many=True).data
            data['studyDirections'] = serializers.StudyDirectionsSerializer(StudyDirections.objects.all(),
                                                                            many=True).data
            data['class_list'] = serializers.KlassSerializersID(p_models.Klass.objects.all(), many=True).data
            data['datas'] = serializers.DateObjectsSerializer(p_models.DateObjects.objects.all(),many=True).data

        if request.GET.get('get_create'):
            data = cached_api_briefcases(lang=translation.get_language())

        if request.GET.get('e_invoices'):
            # data = cached_api_briefcases(lang=translation.get_language())
            bc = Briefcase.objects.get(id=request.GET['e_invoices'])
            acces = AccessToEdit.objects.filter(
                school_id=request.user.libraryuser.school.id)[0]
            if acces.date_invoice > bc.date:
                bc.editable = False
            data['invoice'] = BriefcaseSerializers(bc).data
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
        if 'create_i' in request.data:
            briefcase = request.data['create_i']

            if not 'description' in briefcase:
                briefcase['description'] =''

            briefcase['description'] = briefcase['description'].lstrip().rstrip()
            briefcase['school'] = user.libraryuser.school.id
            briefcase['author'] = user.id
            briefcase['name'] = p_models.Klass.objects.get(
                pk=briefcase['klass']).name + ' ' + p_models.Language.objects.get(pk=briefcase['language']).name + ' ' + \
                                briefcase['description']
            if (len(Briefcase.objects.filter(
                    language=briefcase['language'],
                    klass=briefcase['klass'],
                    school=user.libraryuser.school.id,
                    description=briefcase['description'])) >= 1):
                return JsonResponse({'error': True})
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
                    ret_data = BriefcaseSerializers(instance=serializer.instance).data
                    return Response(data=ret_data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.data.get('ready'):
            invoice = Briefcase.objects.get(pk=request.data.get('ready'))
            if invoice.school.id == request.user.libraryuser.school.id:

                if request.data.get('status_r'):
                    invoice_data = request.data.get('invoice')
                    if acces.date_invoice > invoice.date:
                        return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                        status=status.HTTP_403_FORBIDDEN)
                    invoice_data['school'] = invoice.school.id
                    invoice_data['author'] = request.user.id
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
                    invoice_data = request.data.get('invoice')
                    if acces.date_invoice > invoice.date:
                        return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                        status=status.HTTP_403_FORBIDDEN)
                    invoice_data['school'] = invoice.school.id
                    invoice_data['author'] = request.user.id
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
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'deleted' in request.data:
            if request.user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                    school_id=request.user.libraryuser.school.id, edit_status=1).exists():
                invoice = Briefcase.objects.get(pk=request.data['deleted'],
                                                school=request.user.libraryuser.school)
                if acces.date_invoice > invoice.date:
                    return Response({'errors': 'Редактирование запрещено. Документ в закрытом периоде'},
                                    status=status.HTTP_403_FORBIDDEN)
                invoice.deleted = request.data['set_status']
                invoice.save()
                data = BriefcaseSerializers(invoice).data
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

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


class ConsolidatedRegistry(APIView):
    def get(self, request, format=None):
        try:
            user = get_object_or_404(User, auth_token=request.headers['Token'])
            AccessToEdit.objects.get(school=user.libraryuser.school)
        except AccessToEdit.DoesNotExist:
            return JsonResponse({'errors': 'Нет доступа'}, status=400)

        if request.method == 'GET':
            data = {}
            plan_tituls = PlannedTitle.objects.filter(school=user.libraryuser.school, deleted=False)

            if request.GET.get('get_years'):
                data['years'] = DateObjectsSerializer(
                    p_models.DateObjects.objects.filter(pk__in=plan_tituls.values_list('year')), many=True).data

            if request.GET.get('get_reestr_year'):

                plan_tituls = plan_tituls.filter(year__id=request.GET.get('get_reestr_year'))
                number_books = NumberBooks.objects.filter(school=user.libraryuser.school).values('edition', 'summ',
                                                                                                 'in_warehouse')
                brief_cases = Briefcase.objects.filter(school=user.libraryuser.school).order_by('klass')
                briefcases = b_case_serializers.GetConsolidatedSerializer(brief_cases, many=True).data
                data['b_klasses'] = sorted(
                    list(set([x for x in brief_cases.values_list('klass', flat=True) if type(x) == type(1)])))
                plantituls = plan_tituls.values('briefcase', 'planned_quantity')

                for b in briefcases:
                    b['klasses'] = sorted([f"{n}{l}" for n, l in plan_tituls.filter(
                        id__in=b['plan_tituls']).values_list('klass', 'liter__name')])
                    b['students'] = sum([x for x in plan_tituls.filter(
                        id__in=b['plan_tituls']).values_list('planned_quantity', flat=True)])
                all_students = 0
                for b in briefcases:
                    count_plan_tituls = 0
                    for p in plantituls:
                        if b['id'] == p['briefcase']:
                            all_students += p['planned_quantity']
                            count_plan_tituls += p['planned_quantity']

                    for e in b['editions']:
                        if e['surplus'] < 100:
                            e['need'] = math.ceil((count_plan_tituls * e['surplus']) / 100)
                        else:
                            e['need'] = count_plan_tituls
                        for n in number_books:
                            if e['edition']['id'] == n['edition']:
                                e['availability'] = n['on_hands'] + n['in_warehouse']
                                e['order'] = e['need'] - e['availability']
                data['all_students'] = all_students
                data['table'] = briefcases
                p_t = PlanEditionTeacher.objects.filter(
                    year__id=request.GET.get('get_reestr_year'),
                    school=user.libraryuser.school).order_by('edition__klass')
                data['tables'] = data['table']
                data['klasses_t'] = [dict(t) for t in set(
                    [tuple(d.items()) for d in p_t.values(
                        'edition__klass', 'edition__language', 'edition__language__name_{}'.format(
                            translation.get_language()))
                     ])]
                data['lang_en'] = p_models.Language.objects.get(id=3).name
                data['teacher_classes'] = b_case_serializers.GetPlanEditionTeacher(
                    p_t, many=True).data
                briefcases_ides = list(
                    set(Briefcase.objects.filter(school=user.libraryuser.school).values_list('id', flat=True)))
                all_editios_br_l = EditionBriefcase.objects.filter(briefcase__id__in=briefcases_ides,
                                                                   edition__metodology_complex=1).order_by(
                    'edition__klass', 'edition__name')

            return Response(data)

    def post(self, request, format=None):
        try:
            user = get_object_or_404(User, auth_token=request.data['token'])
            access = AccessToEdit.objects.get(school=user.libraryuser.school, edit_status=1)
        except AccessToEdit.DoesNotExist:
            return JsonResponse({'errors': 'Нет доступа'}, status=400)

        if request.data.get('access'):
            data = {}
            access.edit_status = 0
            access.save()
            data['access_success'] = True
            return Response(data)
        else:
            return JsonResponse({'errors': 'Нет доступа'}, status=400)


def getexel(request):
    h = httplib2.Http()
    AUTH = 'cmVwb3J0ZXI6cXhydDU='
    HEADERS = {
        'Authorization': 'Basic ' + AUTH
    }

    a, data = h.request(
        uri=BASE_1C_PATH + "/eponortfoliohz/hs/otchet/get_otchet/?school={}".format(
            request.user.libraryuser.school.pk),
        method="GET",
        headers=HEADERS,
    )
    response = HttpResponse(data, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=zakup.xlsx"
    return response


def get_brif_100(request):
    b = Briefcase.objects.filter(school=request.user.libraryuser.school).values_list('id', flat=True)
    for i in EditionBriefcase.objects.filter(briefcase__in=b):
        if i.surplus > 100:
            i.surplus = 100
            i.save()
    return HttpResponse('<h1>Сделано</h1>')
