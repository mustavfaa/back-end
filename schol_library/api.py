from account import serializers as account_serializers
from account.models import AccessToEdit
from django.http import JsonResponse, HttpResponse, Http404, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group
import datetime
from account.models import RoleHistory
from .models import NumberBooks, SchoolTitul,SchoolTitulHead, Edition, StudyDirections, Liter, Year, AuthorEdition, PublisherEdition, \
    UMK
import json
from portfoli import models as p_models
from rest_framework import status
from rest_framework.response import Response
from .serializers import NumberBooksSerializer, GetSchoolTitulSerializer, GetHeadSchoolTitulSerializer, EditionsSerializerS, NumberBooksSerializerS, \
    NumberBookSerializer, LiterSerializers
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from schol_library import serializers
from django.utils import translation
from django.core.cache import cache
from .permissions import AccessPermission, AccessPermissionS12
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from django.shortcuts import render
from schol_library import models


def cached_api(lang):
    cache_name = 'Editeds' + lang
    data = cache.get(cache_name)
    if data is None:
        data = {}
        data['years'] = serializers.YearSerializers(Year.objects.filter(deleted=False).order_by('year'), many=True).data
        data['authors'] = serializers.AuthorEditionSerializers(AuthorEdition.objects.all().order_by('name'),
                                                               many=True).data
        data['publishers'] = serializers.PublisherEditionSerializers(
            PublisherEdition.objects.filter(deleted=False).order_by('name_' + lang), many=True).data
        data['languages'] = serializers.LangSerializers(
            p_models.Language.objects.filter(deleted=False).order_by('name_' + lang), many=True).data
        data['klasss'] = serializers.KlassSerializers(p_models.Klass.objects.filter(deleted=False), many=True).data
        data['subjects'] = serializers.SubjectSerializers(
            p_models.Subject.objects.filter(deleted=False).order_by('name_' + lang), many=True).data
        data['metodology_complex'] = serializers.MetodologyComplexSerializers(
            UMK.objects.filter(deleted=False).order_by('name_' + lang), many=True).data
        data['study_direction'] = serializers.StudyDirectionsSerializer(
            StudyDirections.objects.filter(deleted=False).order_by('name_' + lang), many=True).data
        data['editions'] = serializers.EditionSerializerA(
            Edition.objects.select_related('klass',
                                           'publisher',
                                           'subject',
                                           'language',
                                           'author',
                                           'study_direction',
                                           'publish_date',
                                           'series_by_year',
                                           'metodology_complex').filter(deleted=False).order_by('name'), many=True).data
        cache.set(cache_name, data, 2592000)
    return data


# Демо Апи кабинет Зав.Бибилотекоря
@api_view(["GET"])
def number_books_list(request):
    if request.method == 'GET':
        token = get_object_or_404(Token, key=request.GET['token'])
        user = User.objects.filter(username=token.user).first()
        snippets = NumberBooks.objects.filter(school=user.libraryuser.school, it_filled=user).order_by('-id')
        serializer = NumberBooksSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def add_number_books(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(auth_token=request.data['token'])
            if not user.groups.filter(id=6).exists():
                AccessToEdit.objects.get(school=user.libraryuser.school, edit_status=1)
                data = json.loads(request.body.decode('utf-8'))
                user = get_object_or_404(User, auth_token=data['token'])
                if {'id': 1} in user.groups.values('id'):
                    data.update({'school': user.libraryuser.school.id})
                    data.update({'it_filled': user.id})
                    data.pop('token')
                    qs = NumberBookSerializer(data=data)
                    if qs.is_valid():
                        qs.save()
                        qs = NumberBooks.objects.filter(school=user.libraryuser.school)
                        serializer = NumberBooksSerializer(qs, many=True)
                        return JsonResponse(serializer.data, safe=False)
                    return JsonResponse({'errors': 'Ошибка'}, status=400)
                return JsonResponse({'errors': 'Нет доступа'}, status=400)
            else:
                return JsonResponse({'errors': 'Нет доступа'}, status=400)
        except AccessToEdit.DoesNotExist:
            return JsonResponse({'errors': 'Нет доступа'}, status=400)
    return JsonResponse({'errors': 'Ошибка'}, status=400)


@api_view(['GET', 'DELETE'])
def number_books_delete(request, pk):
    try:
        number_book = NumberBooks.objects.get(pk=pk)
    except NumberBooks.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        try:
            user = get_object_or_404(User, auth_token=request.GET['token'])
            AccessToEdit.objects.get(school=user.libraryuser.school, edit_status=1)
        except AccessToEdit.DoesNotExist:
            return JsonResponse({'errors': 'Нет доступа'}, status=400)

        if user:
            number_book.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


# кабинет зав.библиотекоря
class BooksAPIList(APIView):
    permission_classes = [AccessPermission|AccessPermissionS12]

    def get(self, request, format=None):
        user = User.objects.get(auth_token=request.headers['Token'])
        if request.method == 'GET':
            data = cached_api(lang=translation.get_language())
            snippets = NumberBooks.objects.filter(school=user.libraryuser.school)
            serializer = serializers.NumberBooksSerializerBooksAPIList(snippets, many=True)
            data['books'] = serializer.data
            return Response(data)

    def post(self, request, format=None):
        try:
            data = request.data['boocks']
            context = dict()
            context['errors'] = list()
            NumberBooks.objects.filter(id__in=request.data['del_data']).delete()
            models.IncomeExpense.objects.filter(number_book_id__in=request.data['del_data']).delete()
            for i in data:
                try:
                    number_book = NumberBooks.objects.get(id=i['id'])
                    number_book.summ = i['summ']
                    number_book.in_warehouse = i['in_warehouse']
                    number_book.save()
                except:
                    context['errors'].append('Не записался с id {}'.format(i.get('id')))
            return Response(context, status=status.HTTP_201_CREATED)
        except AccessToEdit.DoesNotExist:
            return JsonResponse({'errors': 'Нет доступа'}, status=400)


@csrf_exempt
def demo_add_number_books(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            user = User.objects.get(auth_token=data['token'])
            if not user.groups.filter(id=6).exists():
                data['warning'] = AccessToEdit.objects.get(school=user.libraryuser.school, edit_status=1).edit_status
        except:
            return JsonResponse({'errors': 'Нет доступа', 'warning': 0}, status=400)

        if 1 in user.groups.values_list('id', flat=True) or 6 in user.groups.values_list('id', flat=True):
            data_p = data['book']
            data_p['school'] = user.libraryuser.school.id
            data_p['it_filled'] = user.id

            serializer = NumberBooksSerializerS(data=data_p)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, safe=False)
            else:
                return JsonResponse({'errors': 'Не валидна'}, status=401)
        else:
            return JsonResponse({'errors': 'Нет доступа'}, status=402)
    return JsonResponse({'errors': 'Ошибка'}, status=403)


@api_view(["GET"])
def editions_list(request):
    if request.method == 'GET':
        user = get_object_or_404(User, auth_token=request.headers['Token'])
        cache_name = 'eds' + str(translation.get_language())
        data = cache.get(cache_name)
        if data is None:
            data = {}
            data['books'] = EditionsSerializerS(Edition.objects.filter(deleted=False).order_by('name'), many=True).data
            data['years'] = serializers.YearSerializers(Year.objects.filter(deleted=False).order_by('year'), many=True).data
            data['authors'] = serializers.AuthorEditionSerializers(AuthorEdition.objects.filter(deleted=False).order_by('name').iterator(), many=True).data
            data['publishers'] = serializers.PublisherEditionSerializers(
                PublisherEdition.objects.filter(deleted=False).order_by('name_' + str(translation.get_language())), many=True).data
            data['languages'] = serializers.LangSerializers(
                p_models.Language.objects.filter(deleted=False).order_by('name_' + str(translation.get_language())), many=True).data
            data['klasss'] = serializers.KlassSerializers(p_models.Klass.objects.filter(deleted=False), many=True).data
            data['subjects'] = serializers.SubjectSerializers(
                p_models.Subject.objects.filter(deleted=False).order_by('name_' + str(translation.get_language())), many=True).data
            data['metodology_complex'] = serializers.MetodologyComplexSerializers(
                UMK.objects.filter(deleted=False).order_by('name_' + str(translation.get_language())), many=True).data
            data['study_direction'] = serializers.StudyDirectionsSerializer(
                StudyDirections.objects.filter(deleted=False).order_by('name_' + str(translation.get_language())), many=True).data
            cache.set(cache_name, data, 2592000)
        data['number_books'] = list(NumberBooks.objects.filter(
            school=user.libraryuser.school).values_list('edition', flat=True))
        if not user.groups.filter(id=6).exists():
            if AccessToEdit.objects.get(school=user.libraryuser.school).edit_status > 0:
                data['warning'] = False
            else:
                data['warning'] = True
        else:
            data['warning'] = False
        return JsonResponse(data, safe=False)


# Кабинет зав директора
@api_view(["GET"])
def school_titul_list(request):
    if request.method == 'GET':
        try:
            data = {}
            user = request.user
            if not user.groups.filter(id=6).exists():
                if AccessToEdit.objects.get(school=user.libraryuser.school).edit_status > 0:
                    data['warning'] = False
                else:
                    data['warning'] = True
            else:
                data['warning'] = False
            snippets = SchoolTitulHead.objects.filter(school=user.libraryuser.school).order_by('-year','klass')  # , 'study_direction')
            work_places = p_models.PortfolioWorkTimeLine.objects.filter(current=True,
                                                                        portfolio__deleted=False,
                                                                        deleted=False,
                                                                        checked=True,
                                                                        school=user.libraryuser.school) \
                .values_list('portfolio', flat=True)

            portfolios = p_models.Portfolio.objects.filter(pk__in=work_places)
            data['users'] = serializers.PortfolioSerializers(portfolios, many=True).data
            data['liters'] = LiterSerializers(Liter.objects.filter(deleted=False), many=True).data
            data['data'] = GetHeadSchoolTitulSerializer(snippets, many=True).data
            data['languages'] = serializers.LanguageSerializer(p_models.Language.objects.filter(deleted=False), many=True).data
            data['studyDirections'] = serializers.StudyDirectionsSerializer(StudyDirections.objects.filter(deleted=False), many=True).data
            data['klasss'] = serializers.KlassSerializersID(p_models.Klass.objects.filter(deleted=False), many=True).data
            data['datas'] = serializers.DateObjectsSerializer(p_models.DateObjects.objects.filter(deleted=False).order_by('id'),many=True).data
            return JsonResponse(data)

        except AccessToEdit.DoesNotExist:
            return JsonResponse({'errors': 'Нет доступа', 'warning': 0}, status=400)


@csrf_exempt
def add_school_titul(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            user = get_object_or_404(User, auth_token=data['token'])
            if not user.groups.filter(id=6).exists():
                AccessToEdit.objects.get(school=user.libraryuser.school, edit_status=1)
        except:
            return JsonResponse({'errors': 'Нет доступа'}, status=400)

        if 2 in user.groups.values_list('id', flat=True) or 6 in user.groups.values_list('id', flat=True):
            qs = SchoolTitul(
                school_id=user.libraryuser.school.id,
                klass_id=data['klass'],
                liter_id=data['liter'],
                students=data['students'],
                year_id=data['year'],
                language_id=data['language'],
                study_direction_id=data['study_direction'],
                class_teacher=None
                # class_teacher_id=data['class_teacher']
            )
            qs.save()
            qs = SchoolTitul.objects.filter(school_id=user.libraryuser.school.id)
            serializer = GetSchoolTitulSerializer(qs, many=True)
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse({'errors': 'Нет доступа'}, status=400)
    return JsonResponse({'errors': 'Ошибка'}, status=400)


@csrf_exempt
def school_titul_delete(request, pk=None):
    try:
        data = json.loads(request.body.decode('utf-8'))
        user = User.objects.get(auth_token=data['token'])
        data.pop('token')
        school_titul = SchoolTitul.objects.get(pk=pk)
        if not user.groups.filter(id=6).exists():
            AccessToEdit.objects.get(school=user.libraryuser.school, edit_status=1)
    except:
        return JsonResponse({'errors': 'Нет доступа'}, status=400)

    if request.method == 'PUT':
        serializer = serializers.SchoolTitulSerializers(school_titul, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        school_titul.deleted = True
        school_titul.save()
        return HttpResponse(status=204)


# кабинет зав.библиотекоря
class LibraryBooksAPIList(APIView):
    authentication_classes = [BasicAuthentication, TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated|AccessPermission]
    # permission_classes = [AccessPermission]
    template_name = 'schol_library/librarian/librarian.html'

    def get(self, request, format=None):
        if request.GET.get('all'):
            data = cached_api(lang=translation.get_language())
            snippets = NumberBooks.objects.filter(school=request.user.libraryuser.school).order_by('edition__name')
            serializer = serializers.NumberBooksLibrianSerializer(snippets, many=True)
            data['books'] = serializer.data
            data['number_books'] = snippets.values_list('edition', flat=True)
            return Response(data)
        return render(request, template_name=self.template_name, content_type={"user": request.user})


# Кабинет Зав.библиотекоря: Высталвение ролей для зам.директора по учебоной работе
class RoleAssignmentAPI(APIView):
    permission_classes = [AccessPermission]

    def get(self, request, format=None):
        try:
            user = get_object_or_404(User, auth_token=request.headers['Token'])
        except User.DoesNotExist:
            return JsonResponse({'errors': 'Нет доступа'}, status=400)

        if request.method == 'GET':
            data = {}
            work_places = p_models.PortfolioWorkTimeLine.objects.filter(current=True,
                                                                        portfolio__deleted=False,
                                                                        deleted=False,
                                                                        checked=True,
                                                                        school=user.libraryuser.school) \
                .values_list('portfolio', flat=True)
            portfolios = p_models.Portfolio.objects.filter(pk__in=work_places)
            role_history = RoleHistory.objects.filter(school=user.libraryuser.school).exclude(role=1).exclude(
                data_end=None).order_by('role')
            role_list = RoleHistory.objects.filter(school=user.libraryuser.school, data_end=None).exclude(
                role=1).order_by('role')
            data['role_list'] = account_serializers.RoleHistorySerializers(role_list, many=True).data
            data['groups'] = account_serializers.RolesSerializer(Group.objects.filter(pk__in=[2, 3, 4]), many=True).data
            data['role_history'] = account_serializers.RoleHistorySerializers(role_history, many=True).data
            data['users'] = serializers.PortfolioSerializers(portfolios, many=True).data
            return Response(data)

    def post(self, request, format=None):
        user = User.objects.get(auth_token=request.data['token'])
        if user.groups.filter(id__in=[1, 6]).exists():
            appointment_user = User.objects.get(id=request.data['user']['id'])
            groups = request.data['groups']
            if {'role': 1} in groups:
                groups.pop(groups.index({'role': 1}))
            roles = RoleHistory.objects.filter(school=user.libraryuser.school,
                                               user=request.data['user']['id'], data_end=None).values('role')

            not_roles = [i for i in groups if i not in roles]
            yes_roles = [i for i in roles if i not in groups]

            if len(not_roles) > 0:
                for i in not_roles:
                    data_appointment = RoleHistory(user=appointment_user,
                                                   school=user.libraryuser.school,
                                                   role_id=i['role'],
                                                   data_appointment=datetime.datetime.now())
                    data_appointment.save()

                    appointment_user.groups.add(i['role'])

            if len(yes_roles) > 0:
                for i in yes_roles:
                    data_end = RoleHistory.objects.filter(school=user.libraryuser.school,
                                                          user=appointment_user,
                                                          data_end=None,
                                                          role_id=i['role']).first()

                    data_end.data_end = datetime.datetime.now()
                    data_end.save()
                    appointment_user.groups.remove(i['role'])

            role_history = RoleHistory.objects.filter(school=user.libraryuser.school).exclude(role=1).order_by('role')
            data = account_serializers.RoleHistorySerializers(role_history, many=True).data
            return Response(data)
        else:
            return JsonResponse({'net dostupa'}, status=400)


class RoleEndAPI(APIView):
    permission_classes = [AccessPermission]

    def post(self, request, format=None):
        if request.method == 'POST':
            role = RoleHistory.objects.filter(id=request.data['role']['id']).first()
            role.data_end = datetime.datetime.now()
            role.user.groups.remove(role.role.id)
            role.save()
            return JsonResponse({'yes': 'Завершена'}, status=200)
        else:
            return JsonResponse({'error': 'net dostupa'}, status=400)



