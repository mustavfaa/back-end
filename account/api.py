from account.models import AccessToEdit, LibraryUser
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics
from django.core.cache import cache
from django.utils import translation
from account import serializers
from django.db.models import Count
from portfoli import models as p_models
from rest_framework.authtoken.models import Token


class ClosePage(APIView):
    def post(self, request, format=None):
        try:
            user = get_object_or_404(User, auth_token=request.data['token'])
            AccessToEdit.objects.get(school=user.libraryuser.school, edit_status=1)
        except AccessToEdit.DoesNotExist:
            return JsonResponse({'errors': 'Нет доступа'}, status=400)

        if request.data.get('page'):
            return Response({'close': True}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Ощибка'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Логин"""
    permission_classes = ()
    authentication_classes = ()
    serializer_class = serializers.LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            cd = serializer.validated_data
            user = authenticate(request, username=cd["username"], password=cd["password"])
            if user is not None:
                if user.is_superuser or user.groups.filter(id=6).exists():
                    user.is_admin = True
                try:
                    lu = user.libraryuser
                except:
                    lu = LibraryUser()
                    lu.user = user
                    lu.save()
                user_data = serializers.UserSerializers(user).data
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                user_data['token'] = token.key
                return Response(user_data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "wrong_username_or_password"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class GetSchool(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer = serializers.SchoolTypeSerializers

    def get(self, request):
        context = dict()
        school_menu = cache.get('left_school_menus' + translation.get_language())
        if school_menu == None:
            school_types_for_render = p_models.SchoolType.objects.filter(
                show_at_site=True, deleted=False).order_by(
                'sort')

            for item in school_types_for_render:
                item.my_schools = item.get_my_schools()
                item.my_schools_len = item.my_schools.__len__()
                item.teacher_len = 0
                for sch in item.my_schools:
                    sch.teacher_len = 0
                    wtls = sch.portfolioworktimeline_set.filter(current=True,
                                                                portfolio__deleted=False,
                                                                checked=True,
                                                                uvolen=False,
                                                                deleted=False).values(
                        'portfolio').annotate(kount=Count('portfolio', distinct=True))

                    for wtl in wtls:
                        sch.teacher_len = sch.teacher_len + wtl['kount']
                        item.teacher_len = item.teacher_len + wtl['kount']

            groups = []
            for item in school_types_for_render:
                group = item.group
                if item.group is None:
                    groups.append({
                        'group': False,
                        'data': self.serializer(item).data
                    })
                else:
                    ind = None
                    for i in range(0, groups.__len__()):
                        if groups[i]['group'] and groups[i]['data'] == item.group:
                            ind = i
                            break
                    if ind is None:
                        groups.append({
                            'group': True,
                            'data': self.serializer(group).data,
                            'list': [self.serializer(item).data],
                            'my_schools_len': item.my_schools_len,
                            'teacher_len': item.teacher_len
                        })
                    else:
                        groups[ind]['list'].append(self.serializer(item).data)
                        groups[ind]['my_schools_len'] = groups[ind]['my_schools_len'] + item.my_schools_len
                        groups[ind]['teacher_len'] = groups[ind]['teacher_len'] + item.teacher_len

            context['groups'] = groups
        return Response(context, status=status.HTTP_200_OK)


class NewGetSchool(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer = serializers.SchoolTypeSerializers

    def get(self, request):
        context = dict()
        lu = LibraryUser
        from schol_library.user_utils import user_schools

        schools = user_schools(request.user)

        # if request.user.is_superuser or request.user.groups.filter(id=6).exists():
        #     schools2 = p_models.AlmaMater.objects.select_related('user').filter(nash=True).order_by('sort')
        # else:
        schools = schools.values_list('school', flat=True)
        schools2 = p_models.AlmaMater.objects.select_related('user').filter(id__in=schools.values_list('school', flat=True)).distinct()

        for i in schools2:
            i.liberian_fio = i.user.get_full_name()

        serializer = serializers.NewSchoolListSerializer
        context['schools'] = serializer(schools2, many=True).data

        return Response(context, status=status.HTTP_200_OK)
