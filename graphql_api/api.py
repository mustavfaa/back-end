import graphene
from ekitaphana.settings import DEBUG
from graphene_django.types import ObjectType, DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from account.models import AccessToEdit
from portfoli import models as pf_models
from schol_library.models import PublisherEdition, \
    ActWriteOff, \
    EditionActWrite, \
    PaperInvoice, \
    EditionPaperInvoice, \
    Edition, \
    AuthorEdition, \
    Year, \
    UMK, \
    EditionComplex, \
    StudyDirections, \
    InitialBalance, \
    EditionInitialBalance
from portfoli.models import Klass, \
    Subject, \
    Language


class UMKType(DjangoObjectType):
    class Meta:
        model = UMK

class StudyDirectionsType(DjangoObjectType):
    class Meta:
        model = StudyDirections


class EditionComplexType(DjangoObjectType):
    class Meta:
        model = EditionComplex


class YearType(DjangoObjectType):
    class Meta:
        model = Year


class AuthorType(DjangoObjectType):
    class Meta:
        model = AuthorEdition


class SubjectType(DjangoObjectType):
    class Meta:
        model = Subject


class LanguageType(DjangoObjectType):
    class Meta:
        model = Language


class KlassType(DjangoObjectType):
    class Meta:
        model = Klass


class PublisherType(DjangoObjectType):
    class Meta:
        model = PublisherEdition

class AlmaMaterType(DjangoObjectType):
    class Meta:
        model = pf_models.AlmaMater


class ActWriteOfType(DjangoObjectType):
    class Meta:
        model = ActWriteOff

        # Тесты с фильтром
        # filter_fields = '__all__'
        # interfaces = (graphene.relay.Node,)


class InitialBalanceType(DjangoObjectType):
    class Meta:
        model = InitialBalance


class EditionInitialBalanceType(DjangoObjectType):
    class Meta:
        model = EditionInitialBalance


class EditionActWriteType(DjangoObjectType):
    class Meta:
        model = EditionActWrite
        # Тесты с фильтром
        # filter_fields = {'edition'}
        # interfaces = (graphene.relay.Node,)


class PaperInvoiceType(DjangoObjectType):
    class Meta:
        model = PaperInvoice


class EditionPaperInvoiceType(DjangoObjectType):
    class Meta:
        model = EditionPaperInvoice


class EditionType(DjangoObjectType):
    class Meta:
        model = Edition

        # Тесты с фильтром
        # filter_fields = {'klass__id':['exact'],
        #                  'subject__name_ru': ['exact'],
        #                  'subject': ['exact'],
        #                  'name': ['exact'],
        #                  }
        # interfaces = (graphene.relay.Node,)



class EditionPaperInfoiceInput(graphene.InputObjectType):
    edition = graphene.ID()
    quantity = graphene.Float()
    amout = graphene.Float()


class EditionInitialBalanceInput(graphene.InputObjectType):
    edition = graphene.ID()
    quantity = graphene.Float()
    amout = graphene.Float()


class PaperInvoiceInput(graphene.InputObjectType):
    id = graphene.ID(required=False)
    idx = graphene.String()
    provider = graphene.String()
    date = graphene.Date()
    date_invoice = graphene.Date()
    bin = graphene.String()
    number = graphene.String()
    edition = graphene.List(EditionPaperInfoiceInput)


class InitialBalanceInput(graphene.InputObjectType):
    id = graphene.ID()
    date = graphene.Date()
    edition = graphene.List(EditionInitialBalanceInput)

class CreatePaperInvoice(graphene.Mutation):
    class Arguments:
        input = PaperInvoiceInput(required=True)

    ok = graphene.Boolean()
    invoice = graphene.Field(PaperInvoiceType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        user = info.context.user
        user_school = user.libraryuser.school
        paper_invoice = graphene.Field(PaperInvoiceType)
        if input.id == None:
            paper_instance_instance = PaperInvoice(
                idx=input.idx,
                provider=input.provider,
                date=input.date,
                date_invoice=input.date_invoice,
                number=input.number,
                bin=input.bin,
                school=user_school,
                author=user
            )
        else:
            paper_instance_instance = PaperInvoice.objects.get(pk=input.id)
            acces = AccessToEdit.objects.filter(school=user_school, edit_status=1).exists()
            if not paper_instance_instance.school == user_school or not acces:
                return CreatePaperInvoice(ok=False)
            paper_instance_instance.date = input.date
            paper_instance_instance.idx = input.idx
            paper_instance_instance.bin = input.bin
            paper_instance_instance.date_invoice = input.date_invoice
            paper_instance_instance.provider = input.provider
            EditionPaperInvoice.objects.filter(invoice_id=input.id).delete()



        paper_instance_instance.save()
        for edition in input.edition:
            new_ed = EditionPaperInvoice()
            new_ed.invoice_id = paper_instance_instance.pk
            new_ed.edition = Edition.objects.get(pk=edition.edition)
            new_ed.quantity = edition.quantity
            new_ed.amount = edition.amout
            new_ed.save()
        # paper_instance_instance.save()  Сейвить еще раз чтобы в регистр записалось?  #TODO

        return CreatePaperInvoice(ok=ok)


class EditInitialBalance(graphene.Mutation):
    class Arguments:
        input = InitialBalanceInput(required=True)

    ok = graphene.Boolean()
    invoice = graphene.Field(InitialBalanceType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        user = info.context.user
        user_school = user.libraryuser.school
        paper_invoice = graphene.Field(InitialBalanceType)
        if input.id == None:
            initial_balance_instance = InitialBalance(
                school=user_school,
            )
        else:
            initial_balance_instance = InitialBalance.objects.get(pk=input.id)

        acces = AccessToEdit.objects.filter(school=user_school, edit_status=1).exists()
        if not initial_balance_instance.school == user_school or not acces:
            return EditInitialBalance(ok=False)
        EditionInitialBalance.objects.filter(invoice=initial_balance_instance).delete()

        initial_balance_instance.date = input.date
        initial_balance_instance.save()
        for edition in input.edition:
            new_ed = EditionInitialBalance()
            new_ed.invoice_id = initial_balance_instance.pk
            new_ed.edition = Edition.objects.get(pk=edition.edition)
            new_ed.quantity = edition.quantity
            new_ed.amount = edition.amout
            new_ed.save()

        # paper_instance_instance.save()  Сейвить еще раз чтобы в регистр записалось?  #TODO

        return EditInitialBalance(ok=ok)

class Mutation(graphene.ObjectType):
    create_paper_invoice = CreatePaperInvoice.Field()
    edit_initial_balance = EditInitialBalance.Field()


class Query(object):
    acts_write_off = graphene.List(ActWriteOfType)
    act_write_off_editions = graphene.List(EditionActWriteType)

    # Тесты с фильтром
    # acts_write_off = DjangoFilterConnectionField(ActWriteOfType)
    # act_write_off_editions = graphene.relay.Node.Field(EditionActWriteType)
    # all_editions = DjangoFilterConnectionField(EditionType)
    # editions = graphene.relay.Node.Field(EditionType)
    initial_balance = graphene.List(InitialBalanceType)
    paper_invoices = graphene.List(PaperInvoiceType)
    paper_invoices_editions = graphene.List(EditionPaperInvoiceType)

    editions = graphene.List(EditionType)

    def resolve_acts_write_off(self, info, **kwargs):
        return ActWriteOff.objects.all()

    def resolve_act_write_off_editions(self, info, **kwargs):
        return EditionActWrite.objects.select_related('invoice').all()

    def resolve_initial_balance(self, info, **kwargs):
        my_school = info.context.user.libraryuser.school
        acces = AccessToEdit.objects.filter(school=my_school, edit_status=1).exists()
        if acces:
            return InitialBalance.objects.filter(school=my_school)
        return []


    def resolve_paper_invoices(self, info, **kwargs):
        my_school = info.context.user.libraryuser.school
        acces = AccessToEdit.objects.filter(school=my_school, edit_status=1).exists()
        if acces:
            return PaperInvoice.objects.filter(school=info.context.user.libraryuser.school)
        else:
            return []

    def resolve_paper_invoices_editions(self, info, **kwargs):
        return EditionPaperInvoice.objects.select_related('invoice', 'invoice_edition').all()

    def resolve_editions(self, info, **kwargs):
        qs = Edition.objects.select_related('klass',
                                              'publisher',
                                              'subject',
                                              'language',
                                              'author',
                                              'study_direction',
                                              'publish_date',
                                              'series_by_year',
                                              'metodology_complex').filter(deleted=False)

        if DEBUG:
            qs = qs[:30]

        return qs
