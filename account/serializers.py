from rest_framework import serializers
from .models import RoleHistory, LibraryUser
from portfoli import models as p_models
from django.utils.translation import ugettext as _
from portfoli import models as p_models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True,)
    password = serializers.CharField(required=True,)


class PortfolioSerializers(serializers.ModelSerializer):
    get_avatar = serializers.ReadOnlyField()

    class Meta:
        model = p_models.Portfolio
        fields = ('avatar', 'patronymic_name', 'get_avatar')


class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class AlmaMoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = p_models.AlmaMater
        fields = ('id', 'name')


class LibraryUserSerializers(serializers.ModelSerializer):
    school = AlmaMoterSerializer(read_only=True)

    class Meta:
        model = LibraryUser
        fields = ('school', 'get_avatar')


class UserSerializers(serializers.ModelSerializer):
    groups = RolesSerializer(many=True)
    libraryuser = LibraryUserSerializers(read_only=True)
    is_admin = serializers.BooleanField(default=False)
    # def to_representation(self, instance):
    #     self.libraryuser = p_models.PortfolioWorkTimeLine

    class Meta:
        model = User
        fields = (
        'id', 'username', 'last_name', 'first_name', 'email', 'groups', 'libraryuser', 'auth_token', 'is_admin')


class RoleHistorySerializers(serializers.ModelSerializer):
    user = UserSerializers(read_only=True)
    data_appointment = serializers.DateTimeField(format="%Y-%m-%d{}%H:%M".format(_('|')),
                                                 required=False,
                                                 read_only=True)
    data_end = serializers.DateTimeField(format="%Y-%m-%d{}%H:%M".format(_('|')),
                                         required=False,
                                         read_only=True)
    role = RolesSerializer(read_only=True)

    class Meta:
        model = RoleHistory
        fields = ('id', 'user', 'data_appointment', 'data_end', 'role')


class ClassTeacherSerializers(serializers.ModelSerializer):
    library = LibraryUserSerializers()

    class Meta:
        model = User
        fields = ('id', 'library')


class EducationTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = p_models.EducationType
        fields = ('id', 'name')


class SchoolTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = p_models.SchoolType
        fields = ('id', 'name', 'max_people', 'show_at_site')


class NewSchoolListSerializer(serializers.ModelSerializer):
    liberian_fio = serializers.CharField()

    class Meta:
        model = p_models.AlmaMater
        fields = ('id', 'name', 'liberian_fio')
