from rest_framework import serializers
from .models import NumberBooks, SchoolTitul, StudyDirections, \
    Edition, Liter, Year, PlannedTitle, \
    AuthorEdition, PublisherEdition, UMK, Provider, EditionInvoice,\
    Invoice, PaperInvoice, EditionPaperInvoice, \
    RequestEdition, CheckidRequestEdition, ActWriteOff, EditionActWrite, IncomeExpense, \
    EditionInitialBalance, \
    SchoolTitulHead, SchoolTitulPlannedHead, InitialBalance, BooksOrder, EditionBooksOrder, BooksRecall, \
    BooksMovingHead, BooksMovingEdition,Briefcase,EditionBriefcase
from portfoli import models as p_models
from django.contrib.auth.models import User
from account import serializers as accaunt_serializers, models as ac_models
from portfoli import models as p_models
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import ugettext as _
#from .b_case_serializers import BriefcaseSerializers

class SchoolS(serializers.ModelSerializer):
    class Meta:
        model = p_models.AlmaMater
        fields = ('id', 'name_ru')


# User
class UserSerializers(serializers.ModelSerializer):
    # groups = accaunt_serializers.RolesSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['name'] = instance.portfolio.name + ' / ' + instance.email
        data['name_only'] = instance.portfolio.name
        return data

    # portfolio = PortfolioSerializers()
    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'first_name', 'email',
                  # 'groups',
                  'portfolio')


# сериализация для выставления ролей
class PortfolioSerializers(serializers.ModelSerializer):
    user = UserSerializers(read_only=True)

    # id = serializers.IntegerField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = instance.user.id
        data['name'] = instance.name + ' / ' + instance.email
        return data

    class Meta:
        model = p_models.Portfolio
        fields = ('user', 'avatar',)


#
# class PortfolioSerializers(serializers.ModelSerializer):
#     user = UserSerializers(read_only=True)
#     #id = serializers.IntegerField()
#
#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['id'] = instance.user.id
#         data['name'] = instance.name + ' / ' + instance.email
#         return data
#
#     class Meta:
#         model = p_models.Portfolio
#         fields = ('user', 'avatar', )
# Год
class YearSerializers(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = ('id', 'year')


class KlassSerializersID(serializers.ModelSerializer):
    class Meta:
        model = p_models.Klass
        fields = ('id', 'name',)


class AuthorEditionSerializers(serializers.ModelSerializer):
    class Meta:
        model = AuthorEdition
        fields = ('id', 'name',)


class PublisherEditionSerializers(serializers.ModelSerializer):
    class Meta:
        model = PublisherEdition
        fields = ('id', 'name',)


class MetodologyComplexSerializers(serializers.ModelSerializer):
    class Meta:
        model = UMK
        fields = ('name',)


class LanguageSerializerP(serializers.ModelSerializer):
    class Meta:
        model = p_models.Language
        fields = ('id', 'name')


class EditionSerializerCN(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    author = serializers.CharField()
    publisher = serializers.CharField()
    publish_date = serializers.CharField()
    series_by_year = serializers.CharField()
    metodology_complex = serializers.CharField()
    isbn = serializers.CharField()
    language = LanguageSerializerP()
    klass = serializers.CharField()
    subject = serializers.CharField()
    study_direction = serializers.CharField()

    class Meta:
        model = Edition
        fields = ('id', 'name', 'language', 'klass', 'subject', 'publish_date', 'series_by_year',
                  'author', 'publisher', 'metodology_complex', 'isbn', 'study_direction')


class EditionSerializerA(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    author = serializers.CharField()
    publisher = serializers.CharField()
    publish_date = serializers.CharField()
    series_by_year = serializers.CharField()
    metodology_complex = serializers.CharField()
    isbn = serializers.CharField()
    language = serializers.CharField()
    klass = serializers.CharField()
    subject = serializers.CharField()
    study_direction = serializers.CharField()
    amount = serializers.FloatField()

    class Meta:
        model = Edition
        fields = ('id', 'name', 'language', 'klass', 'subject', 'publish_date', 'series_by_year',
                  'author', 'publisher', 'metodology_complex', 'isbn', 'study_direction', 'amount')


class EditionSerializerB(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    author = serializers.CharField()
    publisher = serializers.CharField()
    publish_date = serializers.CharField()
    series_by_year = serializers.CharField()
    metodology_complex = serializers.CharField()
    isbn = serializers.CharField()
    language = LanguageSerializerP()
    subject = serializers.CharField()
    study_direction = serializers.CharField()

    class Meta:
        model = Edition
        fields = ('id', 'name', 'language', 'klass', 'subject', 'publish_date', 'series_by_year',
                  'author', 'publisher', 'metodology_complex', 'isbn', 'study_direction')


class EditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edition
        fields = ('id', 'name')


class NewEditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edition
        fields = ('id', 'name')


class NumberBooksSerializer(serializers.ModelSerializer):
    edition = EditionSerializer()

    class Meta:
        model = NumberBooks
        fields = ('id', 'school', 'edition', 'summ', 'in_warehouse')


class NumberBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumberBooks
        fields = ('school', 'edition', 'summ', 'in_warehouse', 'it_filled')


class DateObjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = p_models.DateObjects
        fields = ('id', 'name', 'year_number')


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = p_models.Language
        fields = ('id', 'name',)


class StudyDirectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyDirections
        fields = ('id', 'name',)


# Кабинет Зав Библиотекоря
class LiterSerializers(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Liter
        fields = ('id', 'name')


class GetHeadSchoolTitulSerializer(serializers.ModelSerializer):
    # liter = LiterSerializers()
    # klass = KlassSerializersID(read_only=True)
    # year = DateObjectsSerializer(read_only=True)
    # language = LanguageSerializer(read_only=True)
    # study_direction = StudyDirectionsSerializer()
    # class_teacher = UserSerializers()
    # date = serializers.DateField(read_only=True)
    school = SchoolS()
    kurator = UserSerializers()

    class Meta:
        model = SchoolTitulHead
        fields = ('id',
                  'school',
                  'klass',
                  'year',
                  'comment',
                  'date',
                  'status',
                  'deleted',
                  'liter',
                  'study_direction',
                  'students',
                  'kurator',
                  'language')



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


class BriefcaseSerializersShort(serializers.ModelSerializer):
    #  editions_val = PostEditionBriefcaseSerializers(many=True)
    #  editable = serializers.BooleanField(default=True, read_only=True)
    school = SchoolS()

    class Meta:
        model = Briefcase
        fields = (
            'id', 'name', 'school', 'author', 'description', 'klass', 'language', 'status', 'year',
            'date', 'study_direction',  'deleted')



class GetHeadSchoolTitulPlannedSerializer(serializers.ModelSerializer):
    # liter = LiterSerializers()
    # klass = KlassSerializersID(read_only=True)
    # year = DateObjectsSerializer(read_only=True)
    # language = LanguageSerializer(read_only=True)
    # study_direction = StudyDirectionsSerializer()
    # class_teacher = UserSerializers()
    # date = serializers.DateField(read_only=True)
    school = SchoolS()

    briefcase = BriefcaseSerializersShort()
    # kurator = UserSerializers()
    class Meta:
        model = SchoolTitulPlannedHead
        fields = ('id', 'school', 'klass', 'year', 'comment',
                  'date', 'status', 'deleted',
                  'liter', 'study_direction', 'briefcase',
                  'students',
                  'language')


class GetSchoolTitulSerializer(serializers.ModelSerializer):
    liter = LiterSerializers()
    klass = KlassSerializersID(read_only=True)
    year = DateObjectsSerializer(read_only=True)
    language = LanguageSerializer(read_only=True)
    study_direction = StudyDirectionsSerializer()
    class_teacher = UserSerializers()

    class Meta:
        model = SchoolTitul
        fields = (
            'id', 'school', 'klass', 'liter', 'students', 'year', 'language', 'study_direction', 'class_teacher',
            'deleted')


class GlobalSchoolTitulSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolTitul
        fields = ('id', 'school', 'year', 'klass', 'liter', 'students', 'language', 'study_direction')


class SchoolTitulSerializerForFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolTitul
        fields = ('liter', 'students', 'language', 'study_direction')


class GetSchoolTitulFullSerializer(serializers.ModelSerializer):
    # students = SchoolTitulSerializerForFullSerializer(many=True)
    editable = serializers.BooleanField(default=True, read_only=True)
    kurator = UserSerializers()

    class Meta:
        model = SchoolTitulHead
        fields = ('id', 'school', 'klass', 'year', 'comment', 'date', 'status',
                  'students',
                  'editable',
                  'deleted',
                  'language',
                  'kurator',
                  'liter',
                  'study_direction')


class GetSchoolTitulPlannedFullSerializer(serializers.ModelSerializer):
    # students = SchoolTitulSerializerForFullSerializer(many=True)
    editable = serializers.BooleanField(default=True, read_only=True)

    # kurator = UserSerializers()
    class Meta:
        model = SchoolTitulPlannedHead
        fields = ('id', 'school', 'klass', 'year', 'comment', 'date', 'status',
                  'students',
                  'editable',
                  'deleted',
                  'language',
                  # 'kurator',
                  'liter',
                  'study_direction')


class PostSchoolTitulSerializerForFullSerializer(serializers.Serializer):
    liter = serializers.IntegerField()
    students = serializers.IntegerField()
    language = serializers.IntegerField()
    study_direction = serializers.IntegerField()

    class Meta:
        fields = ('liter', 'students', 'language', 'study_direction')


class PostSchoolTitulFullSerializer(serializers.ModelSerializer):
    # students = PostSchoolTitulSerializerForFullSerializer(many=True, read_only=True)

    class Meta:
        model = SchoolTitulHead
        fields = ('school', 'klass', 'year', 'comment', 'date', 'id', 'status', 'language', 'liter', 'students',
                  'study_direction', 'kurator')


class PostSchoolTitulPlannedFullSerializer(serializers.ModelSerializer):
    # students = PostSchoolTitulSerializerForFullSerializer(many=True, read_only=True)

    class Meta:
        model = SchoolTitulPlannedHead
        fields = ('school', 'klass', 'year', 'comment', 'date',
                  'id',
                  'status',
                  'language',
                  'liter',
                  'students',
                  'study_direction')


class NumberBooksSerializerS(serializers.ModelSerializer):
    class Meta:
        model = NumberBooks
        fields = ('edition', 'summ', 'in_warehouse', 'school', 'it_filled')


class RegisterAPIList(serializers.ModelSerializer):
    edition = EditionSerializerA(read_only=True)

    class Meta:
        model = IncomeExpense
        fields = ('id', 'edition', 'summ', 'quantity', 'school', 'income', 'income_type')


class NumberBooksSerializerBooksAPIList(serializers.ModelSerializer):
    edition = EditionSerializerA(read_only=True)

    class Meta:
        model = NumberBooks
        fields = ('id', 'edition', 'summ', 'in_warehouse', 'school', 'it_filled', 'results')


class NumberBooksLibrianSerializer(serializers.ModelSerializer):
    # quantity = serializers.JSONField(read_only=True)
    edition = EditionSerializerA(read_only=True)

    class Meta:
        model = NumberBooks
        fields = ('id', 'edition', 'results', 'school', 'it_filled', 'in_warehouse', 'summ')


class NumberBooksSerializerPostBooksAPIList(serializers.ModelSerializer):
    class Meta:
        model = NumberBooks
        fields = ('id', 'edition', 'summ', 'in_warehouse', 'school', 'it_filled')


# Утвержденный по биб кабинету
class LangSerializers(serializers.ModelSerializer):
    class Meta:
        model = p_models.Language
        fields = ('name',)


class KlassSerializers(serializers.ModelSerializer):
    class Meta:
        model = p_models.Klass
        fields = ('name',)


class SubjectSerializers(serializers.ModelSerializer):
    class Meta:
        model = p_models.Subject
        fields = ('name',)


#  Cериализация для заполения УМК
class EditionsSerializerS(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    language = serializers.CharField()
    klass = serializers.CharField()
    author = serializers.CharField()
    publisher = serializers.CharField()
    series_by_year = serializers.CharField()
    publish_date = serializers.CharField()
    metodology_complex = serializers.CharField()
    isbn = serializers.CharField()
    subject = serializers.CharField()
    study_direction = serializers.CharField()
    summ = serializers.IntegerField(default=0, allow_null=True)
    in_warehouse = serializers.IntegerField(default=0, allow_null=True)


# сериализация для редактирвоания Классов
class SchoolTitulSerializers(serializers.ModelSerializer):
    class Meta:
        model = SchoolTitul
        fields = '__all__'


# сериализация для выставления ролей
class PortfolioSerializers(serializers.ModelSerializer):
    user = UserSerializers(read_only=True)

    # id = serializers.IntegerField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = instance.user_id
        data['name'] = instance.name + ' / ' + instance.email
        data['name_only'] = instance.name
        return data

    class Meta:
        model = p_models.Portfolio
        fields = ('user', 'avatar',)


# для планового титула
class PlanSchoolTitulSerializers(serializers.ModelSerializer):
    liter = LiterSerializers()
    language = LanguageSerializerP()
    year = DateObjectsSerializer()

    class Meta:
        model = PlannedTitle
        fields = ('id', 'school', 'klass', 'liter', 'students', 'year',
                  'language', 'study_direction', 'planned_quantity')


# для планового титула
class PostPlanSchoolTitulSerializers(serializers.ModelSerializer):
    class Meta:
        model = PlannedTitle
        fields = ('school', 'klass', 'liter', 'students', 'year', 'language', 'study_direction', 'planned_quantity',
                  'school_titul')


class PostPlanSchoolTitulDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = PlannedTitle
        fields = ('id', 'planned_quantity')


class ListPlanSchoolTitulSerializers(serializers.ModelSerializer):
    liter = LiterSerializers()
    language = LanguageSerializerP()

    class Meta:
        model = PlannedTitle
        fields = ('school', 'klass', 'liter', 'students', 'year', 'language', 'study_direction', 'planned_quantity',
                  'school_titul')


class ProviderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ('id', 'name')


class EditionInvoiceSerializers(serializers.ModelSerializer):
    edition = EditionSerializerA()

    class Meta:
        model = EditionInvoice
        fields = ('id', 'invoice', 'edition', 'quantity', 'planned_quantity', 'amount')


class EditionPInvoiceSerializers(serializers.ModelSerializer):
    edition = EditionSerializerA()

    class Meta:
        model = EditionInvoice
        fields = ('id', 'invoice', 'edition', 'quantity', 'amount')


class EditionInitialBalanceSerializers(serializers.ModelSerializer):
    edition = NewEditionSerializer()

    class Meta:
        model = EditionInitialBalance
        fields = ('id', 'invoice', 'edition', 'quantity', 'amount')


class EditionBooksOrderSerializers(serializers.ModelSerializer):
    edition = EditionSerializerA()

    class Meta:
        model = EditionInitialBalance
        fields = ('id', 'invoice', 'edition', 'quantity')


class PortfolioMSerializers(serializers.ModelSerializer):
    class Meta:
        model = p_models.Portfolio
        fields = ('id', 'last_name', 'first_name', 'patronymic_name')


class InvoiceSerializers(serializers.ModelSerializer):
    year = serializers.CharField()
    publisher = PublisherEditionSerializers()
    freight_carrier = ProviderSerializers()
    editions_val = EditionInvoiceSerializers(many=True)
    provider = ProviderSerializers()
    shipper = ProviderSerializers()
    school = serializers.CharField()
    confidant = PortfolioMSerializers()
    date = serializers.DateField(format='%d.%m.%Y')

    class Meta:
        model = Invoice
        fields = ('id', 'number', 'year', 'school', 'publisher', 'date', 'editions_val', 'provider',
                  'shipper', 'freight_carrier', 'power_of_attorney', 'school', 'amount',
                  'date_power_of_attorney', 'confidant', 'date_extracts', 'status')


class NumberProvider(serializers.Serializer):
    id = serializers.IntegerField()
    power_of_attorney = serializers.CharField()


class EditionPaperInvoiceSerializers(serializers.ModelSerializer):
    edition = EditionSerializerA()

    class Meta:
        model = EditionPaperInvoice
        fields = ('id', 'invoice', 'edition', 'quantity', 'amount')


class PostEditionPaperInvoiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = EditionPaperInvoice
        fields = ('id', 'invoice', 'edition', 'quantity', 'amount')


class PostEditionInitialbalanceSerializers(serializers.ModelSerializer):
    class Meta:
        model = EditionInitialBalance
        fields = ('id', 'invoice', 'edition', 'quantity', 'amount')


class PostEditionOrderBooksSerializers(serializers.ModelSerializer):
    class Meta:
        model = EditionBooksOrder
        fields = ('id', 'invoice', 'edition', 'quantity')


class PaperInvoiceSerializersForNewFront(serializers.ModelSerializer):
    # editions_val = EditionPInvoiceSerializers(many=True)
    school = serializers.CharField()
    author_fio = serializers.CharField()

    class Meta:
        model = PaperInvoice
        fields = ('id', 'idx', 'date', 'provider', 'bin', 'number', 'date_invoice', 'school',
                  'amount', 'status', 'deleted', 'author_fio', 'comment')


class PaperInvoiceSerializers(serializers.ModelSerializer):
    editions_val = EditionPInvoiceSerializers(many=True)
    school = serializers.CharField()
    author_fio = serializers.CharField()
    editable = serializers.BooleanField(default=True, read_only=True)

    class Meta:
        model = PaperInvoice
        fields = ('id', 'idx', 'date', 'provider', 'bin',
                  'number', 'date_invoice', 'school',
                  'amount', 'editions_val', 'author',
                  'status', 'deleted', 'comment',
                  'author_fio', 'editable')

class GetInitialBalanceSerializers(serializers.ModelSerializer):


    class Meta:
        model = InitialBalance
        fields = '__all__'
class InitialBalanceSerializers(serializers.ModelSerializer):
    editions_val = EditionInitialBalanceSerializers(many=True)
    school = serializers.CharField()
    author_fio = serializers.CharField()
    editable = serializers.BooleanField(default=True, read_only=True)

    class Meta:
        model = InitialBalance
        fields = ('id',
                  'date',
                  'school',
                  'status',
                  'amount',
                  'editions_val',
                  'deleted',
                  'comment',
                  'author',
                  'author_fio',
                  'editable')


class NewInitialBalanceSerializers(serializers.ModelSerializer):
    school = serializers.CharField()
    author_fio = serializers.CharField()
    school = SchoolS()

    class Meta:
        model = InitialBalance
        fields = ('id', 'date', 'school',
                  'status',
                  'amount', 'deleted',
                  'author_fio', 'comment')


class OrderBooksSerializers(serializers.ModelSerializer):
    editions_val = EditionBooksOrderSerializers(many=True)
    school = serializers.CharField()
    author_fio = serializers.CharField()
    editable = serializers.BooleanField(default=True, read_only=True)

    class Meta:
        model = BooksOrder
        fields = ('id', 'date', 'school', 'comment', 'status',
                  'editions_val', 'deleted', 'author', 'author_fio', 'comment', 'editable')


class ValidateConfidante(serializers.ModelSerializer):
    class Meta:
        model = PaperInvoice
        fields = ('confidant',)


class ValidateFreightCarrier(serializers.ModelSerializer):
    class Meta:
        model = PaperInvoice
        fields = ('freight_carrier',)


class ValidateNumber(serializers.Serializer):
    id = serializers.IntegerField()
    number = serializers.CharField()


class ValidateDateExtracts(serializers.Serializer):
    id = serializers.IntegerField()
    date_extracts = serializers.DateField()


class ValidateDatePowerOfAttorney(serializers.Serializer):
    id = serializers.IntegerField()
    date_power_of_attorney = serializers.DateField()


class PaperInvoiceSerializerPost(serializers.ModelSerializer):
    editable = serializers.BooleanField(default=True, read_only=True)

    class Meta:
        model = PaperInvoice
        fields = ['id', 'idx', 'date', 'provider', 'bin', 'number', 'date_invoice', 'school', 'author', 'status',
                  'comment', 'editable']

    def validate(self, attrs):
        try:
            data_st = ac_models.AccessToEdit.objects.filter(school_id=attrs['school'].id).first().date_invoice
            if len(attrs['bin']) != 12:
                raise serializers.ValidationError(_("Не правильно введен БИН"))
            if attrs['date'] < data_st or attrs['date'] > timezone.now().date():
                raise serializers.ValidationError(_("Не верная дата накладной"))
            if attrs['date_invoice'] < data_st or attrs['date_invoice'] > timezone.now().date():
                raise serializers.ValidationError(_("Не верная дата счет фактуры"))
            return attrs
        except:
            raise serializers.ValidationError(_("Нет разрешения"))
            return attrs


class InitialBalanceSerializerPost(serializers.ModelSerializer):
    editable = serializers.BooleanField(default=True, read_only=True)

    class Meta:
        model = InitialBalance
        fields = ['id', 'date', 'school', 'status', 'author', 'comment', 'editable']

    def validate(self, attrs):
        try:
            data_st = ac_models.AccessToEdit.objects.filter(school_id=attrs['school'].id).first().date_invoice
            # if attrs['date'] < data_st or attrs['date'] > timezone.now().date():
            #     raise serializers.ValidationError(_("Не верная дата накладной"))
            return attrs
        except:
            raise serializers.ValidationError(_("Нет разрешения"))
            return attrs


class BooksOrderSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = BooksOrder
        fields = ['id', 'date', 'school', 'author', 'comment', 'status']

    def validate(self, attrs):
        try:
            data_st = ac_models.AccessToEdit.objects.filter(school_id=attrs['school'].id).first().date_invoice
            return attrs
        except:
            raise serializers.ValidationError(_("Нет разрешения"))
            return attrs


class RequestEditionSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = RequestEdition
        fields = ('id', 'edition', 'provider', 'shipper', 'author', 'date_time', 'quantity')


class CheckidRequestEditionS2(serializers.ModelSerializer):
    class Meta:
        model = CheckidRequestEdition
        fields = ('id', 'request_edition', 'school', 'author', 'check', 'quantity')


class CheckidRequestEditionS(serializers.ModelSerializer):
    school = serializers.CharField()

    class Meta:
        model = CheckidRequestEdition
        fields = ('id', 'request_edition', 'school', 'author', 'date_time', 'check', 'date_time', 'quantity', 'check2')


class RequestEditionSerializerGet(serializers.ModelSerializer):
    edition = EditionSerializerA()
    scheckids = CheckidRequestEditionS(many=True, read_only=True)

    class Meta:
        model = RequestEdition
        fields = ('id', 'edition', 'provider', 'shipper', 'author', 'date_time', 'quantity', 'scheckids')


class RequestEditionSerializerGet2(serializers.ModelSerializer):
    edition = EditionSerializerA()

    class Meta:
        model = RequestEdition
        fields = ('id', 'edition', 'provider', 'shipper', 'author', 'date_time', 'quantity')


class CheckidRequestEditionS3(serializers.ModelSerializer):
    request_edition = RequestEditionSerializerGet2(read_only=True)

    class Meta:
        model = CheckidRequestEdition
        fields = ('id', 'request_edition', 'school', 'author', 'date_time', 'check', 'date_time', 'quantity', 'check2')


class EditionActWriteSerializers(serializers.ModelSerializer):
    edition = EditionSerializerA()

    class Meta:
        model = EditionActWrite
        fields = ('id', 'invoice', 'edition', 'quantity', 'price', 'amount', 'income', 'income_type', 'has', 'summ')


class ActWriteOffSerializers(serializers.ModelSerializer):
    editions_val = EditionActWriteSerializers(many=True)
    school = serializers.CharField()
    author_fio = serializers.CharField()
    editable = serializers.BooleanField(default=True, read_only=True)

    class Meta:
        model = ActWriteOff
        fields = ('id', 'idx', 'date', 'date_write', 'school', 'author', 'footing', 'members_of_commission', 'status',
                  'editions_val', 'amount', 'author_fio', 'comment', 'editable', 'deleted')


class NewActWriteOffSerializers(serializers.ModelSerializer):
    school = serializers.CharField()
    author_fio = serializers.CharField()

    class Meta:
        model = ActWriteOff
        fields = (
            'id', 'idx', 'date_write', 'school', 'author', 'author_fio', 'footing', 'members_of_commission', 'status',
            'amount', 'comment', 'deleted')


class PostActWriteOffSerializers(serializers.ModelSerializer):
    class Meta:
        model = ActWriteOff
        fields = (
            'id', 'idx', 'date_write', 'school', 'author', 'footing', 'members_of_commission', 'status', 'comment')

    # def validate(self, attrs):
    #     try:
    #         data_st = ac_models.AccessToEdit.objects.get(school=attrs['school']).date_invoice
    #         if attrs['date_write'] < data_st or attrs['date_write'] > timezone.now().date():
    #             raise serializers.ValidationError(_("Не верная дата"))
    #         return attrs
    #     except:
    #         raise serializers.ValidationError(_("Нет разрешения"))
    #         return attrs


class PostEditionActWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = EditionActWrite
        fields = ('id', 'invoice', 'edition', 'quantity', 'amount', 'income', 'income_type', 'price')


class ABOPortfolioMSerializers(serializers.ModelSerializer):
    class Meta:
        model = p_models.Portfolio
        fields = ('user', 'email', 'phone')


class ReadyInSchool(serializers.Serializer):
    has = serializers.IntegerField()
    school = serializers.IntegerField()

    class Meta:
        fields = ('has', 'school')


class AdminBooksOrders(serializers.ModelSerializer):
    school = serializers.IntegerField()
    author = serializers.IntegerField()
    author_fio = serializers.CharField()
    date = serializers.DateField()

    class Meta:
        model = EditionBooksOrder
        fields = ('invoice', 'edition', 'quantity', 'school', 'author', 'author_fio', 'date')


class BooksRecallSerializer(serializers.ModelSerializer):
    order_school = serializers.IntegerField(required=False)

    class Meta:
        model = BooksRecall
        fields = ('author', 'school', 'order', 'edition', 'quantity', 'order_school', 'deleted')


# class KontingentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Kontingent
#         fields = ('school', 'year', 'quantity')


class AdminBooksMovingEditonSerializers(serializers.ModelSerializer):
    class Meta:
        model = BooksMovingEdition
        fields = (
            'id', 'number', 'invoice', 'edition', 'quantity', 'price', 'amount', 'income', 'income_type', 'has', 'summ')


class AdminDetailBooksMovingEditonSerializers(serializers.ModelSerializer):
    edition = EditionSerializerA()

    class Meta:
        model = BooksMovingEdition
        fields = (
            'id', 'number', 'invoice', 'edition', 'quantity', 'price', 'amount', 'income', 'income_type', 'has', 'summ')


class AdminDetailBookMovingSerializer(serializers.ModelSerializer):
    editions_val = AdminDetailBooksMovingEditonSerializers(many=True)

    class Meta:
        model = BooksMovingHead
        fields = ('id',
                  'author',
                  'recipient_school',
                  'sender_school',
                  'date',
                  'status',
                  'recall',
                  'editions_val',
                  )


class AdminBookMovingSerializer(serializers.ModelSerializer):
    editions_val = AdminBooksMovingEditonSerializers(many=True)

    class Meta:
        model = BooksMovingHead
        fields = ('id',
                  'author',
                  'recipient_school',
                  'sender_school',
                  'date',
                  'status',
                  'recall',
                  'editions_val',
                  )
