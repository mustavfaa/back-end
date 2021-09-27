from rest_framework import serializers
from .models import Briefcase, EditionBriefcase, PlannedTitle, PlanEditionTeacher
from .serializers import SchoolS, EditionSerializerA, EditionSerializerB, EditionSerializerCN
from schol_library import serializers as sl_serializers


class PostEditionBriefcaseSerializers(serializers.ModelSerializer):
    class Meta:
        model = EditionBriefcase
        fields = ('id', 'briefcase', 'edition', 'surplus')


class BriefcaseSerializers(serializers.ModelSerializer):
    editions_val = PostEditionBriefcaseSerializers(many=True)
    editable = serializers.BooleanField(default=True, read_only=True)
    school = SchoolS()

    class Meta:
        model = Briefcase
        fields = (
            'id', 'name', 'school', 'author', 'description', 'klass', 'language', 'status', 'year', 'editions_val',
            'date', 'study_direction', 'editable', 'deleted')


class BriefcaseSerializersSchoolID(serializers.ModelSerializer):
    editions_val = PostEditionBriefcaseSerializers(many=True)
    editable = serializers.BooleanField(default=True, read_only=True)

    # school = SchoolS()
    class Meta:
        model = Briefcase
        fields = (
            'id', 'name', 'school', 'author', 'description', 'klass', 'language', 'status', 'year', 'editions_val',
            'date', 'study_direction', 'editable', 'deleted')


class Post2EditionBriefcaseSerializers(serializers.Serializer):
    edition = serializers.IntegerField()
    surplus = serializers.IntegerField()

    class Meta:
        fields = ('edition', 'surplus')


class PostBriefcaseSerializers(serializers.ModelSerializer):
    editions_val = Post2EditionBriefcaseSerializers(many=True, read_only=True)

    # school = SchoolS()
    class Meta:
        model = Briefcase
        fields = (
            'id', 'name', 'school', 'author', 'description', 'klass', 'language', 'status', 'year', 'study_direction',
            'editions_val')


class EditionBriefcaseSerializers(serializers.ModelSerializer):
    edition = EditionSerializerA()

    class Meta:
        model = EditionBriefcase
        fields = '__all__'


class SchoolTitulListSerializer(serializers.ModelSerializer):
    liter = sl_serializers.LiterSerializers()
    year = sl_serializers.DateObjectsSerializer(read_only=True)
    language = sl_serializers.LanguageSerializer(read_only=True)
    study_direction = sl_serializers.StudyDirectionsSerializer()
    briefcase = BriefcaseSerializers()

    class Meta:
        model = PlannedTitle
        fields = ('id', 'school', 'klass', 'liter', 'students', 'year', 'language',
                  'students', 'planned_quantity', 'study_direction', 'briefcase')


class PlannedTitlePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlannedTitle
        fields = '__all__'


class PlanTitulSerializerInPlan(serializers.ModelSerializer):
    class Meta:
        model = PlannedTitle
        fields = ('id', 'school', 'klass', 'liter', 'students', 'year',
                  'language', 'students', 'planned_quantity', 'study_direction')


class PostPlanEditionTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanEditionTeacher
        fields = ('edition', 'quantity', 'school', 'author', 'year')


class GetPlanEditionTeacherSerializer(serializers.ModelSerializer):
    edition = EditionSerializerA(read_only=True)

    class Meta:
        model = PlanEditionTeacher
        fields = ('id', 'edition', 'quantity', 'school', 'author')


class PlanTitulBriefcaseSerializer(serializers.ModelSerializer):
    liter = serializers.CharField()

    class Meta:
        model = PlannedTitle
        fields = ('id', 'klass', 'liter', 'students', 'planned_quantity', 'briefcase')


class EditionBriefcaseSerializer(serializers.ModelSerializer):
    edition = EditionSerializerCN()

    class Meta:
        model = EditionBriefcase
        fields = ('edition', 'surplus')


class GetConsolidatedSerializer(serializers.ModelSerializer):
    editions = EditionBriefcaseSerializer(many=True, read_only=True)
    language = serializers.CharField()

    class Meta:
        model = Briefcase
        fields = ('id', 'name', 'klass', 'plan_tituls', 'editions', 'language')


class GetPlanEditionTeacher(serializers.ModelSerializer):
    edition = EditionSerializerB(read_only=True)

    class Meta:
        model = PlanEditionTeacher
        fields = ('edition', 'quantity')
