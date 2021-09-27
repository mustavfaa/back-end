from django.contrib import admin
from .models import Edition, NumberBooks, SchoolTitul, StudyDirections, UMK, ApplicationR, FundingСycle, \
    CancellationReason, Liter, Year, PlannedTitle, AuthorEdition, PublisherEdition, Briefcase, EditionBriefcase, \
    PlanEditionTeacher, Invoice, Provider, EditionInvoice, PaperInvoice, EditionPaperInvoice, IncomeExpense, \
    RequestEdition, CheckidRequestEdition, ActWriteOff, EditionActWrite, InitialBalance, CatVer, \
    EditionInitialBalance, \
    BooksOrder, EditionBooksOrder, BooksRecall, SchoolTitulHead, SchoolTitulPlannedHead, BooksMovingEdition, \
    BooksMovingHead
from modeltranslation.admin import TranslationAdmin


class SchoolTitulAdmin(admin.ModelAdmin):
    autocomplete_fields = ['school']
    list_display = ('klass', 'liter', 'school', 'year', 'study_direction')
    search_fields = ['school', 'id']


class BriefcaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'klass', 'school_id', 'language')
    search_fields = ['school_id', 'id']


class EditionBriefcaseAdmin(admin.ModelAdmin):
    list_display = ('edition', 'briefcase_id')
    search_fields = ['briefcase_id', 'id']


class EditionInvoiceInline(admin.TabularInline):
    model = EditionInvoice


class InvoiceAdmin(admin.ModelAdmin):
    inlines = [EditionInvoiceInline]
    list_display = ('__str__', 'id', 'school', 'publisher')


class EditionPaperInvoiceInline(admin.TabularInline):
    autocomplete_fields = ['edition']
    model = EditionPaperInvoice


class EditionInitialBalanceInline(admin.TabularInline):
    autocomplete_fields = ['edition']
    model = EditionInitialBalance


class CheckidRequestEditionInline(admin.TabularInline):
    model = CheckidRequestEdition


class EditionBooksOrderInline(admin.TabularInline):
    autocomplete_fields = ['edition']
    model = EditionBooksOrder


@admin.register(RequestEdition)
class RequestEditionAdmin(admin.ModelAdmin):
    list_display = ['quantity', 'id', 'provider', 'shipper']
    inlines = [CheckidRequestEditionInline]


@admin.register(PaperInvoice)
class PaperInvoiceAdmin(admin.ModelAdmin):
    inlines = [EditionPaperInvoiceInline]
    search_fields = ('school', 'author')
    autocomplete_fields = ['school', 'author']
    list_display = ('__str__', 'id', 'school')


@admin.register(InitialBalance)
class InitialBalanceAdmin(admin.ModelAdmin):
    inlines = [EditionInitialBalanceInline]
    search_fields = ('school',)
    autocomplete_fields = ['school']
    list_display = ('__str__', 'id', 'school', 'date_added')


@admin.register(BooksOrder)
class BooksOrder(admin.ModelAdmin):
    inlines = [EditionBooksOrderInline]
    search_fields = ('school',)
    autocomplete_fields = ['school']
    list_display = ('__str__', 'id', 'school')


class ProviderAdmin(TranslationAdmin, admin.ModelAdmin):
    list_display = ('id', 'name')

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
        'id',
        'publisher__name'
    ]

    list_display = [
        'name',
        'id',
        'isbn',
        'klass',
        'study_direction',
        'subject',
        'language',
        'metodology_complex',
        'publisher',
        'series_by_year',
        'edition_complex'
    ]

    list_filter = [
        'klass',
        'language',
        'series_by_year',
        'publisher',
        'study_direction'
    ]


@admin.register(NumberBooks)
class NumberBooksAdmin(admin.ModelAdmin):
    search_fields = ('school', 'edition')
    autocomplete_fields = ['school', 'edition', 'it_filled']

    list_display = ['id', 'edition', 'edition_id', 'school', 'in_warehouse', 'in_register', 'amounts', 'summ']
    list_filter = ['in_register', 'school', 'edition']


@admin.register(BooksRecall)
class BooksRecallAdmin(admin.ModelAdmin):
    search_fields = ('school', 'order', 'edition')
    list_display = ['id', 'edition', 'school', 'quantity']


@admin.register(Liter)
class LiterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sort']
    list_editable = ['sort']


@admin.register(SchoolTitulHead)
class SchoolTitulHeadAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'school',
        'year',
        'klass',
        'liter',
        'language',
        'study_direction',
        'students',
        'kurator',
    ]
    list_filter = [
        #    'school',
        'klass',
        'year',
        'language']


@admin.register(SchoolTitulPlannedHead)
class SchoolTitulPlannedHeadAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'school',
        'year',
        'klass',
        'liter',
        'language',
        'study_direction',
        'students',

    ]
    list_filter = [
        #    'school',
        'klass',
        'year',
        'language']
    autocomplete_fields = ['school']


# admin.site.register(SchoolTitulPlannedHead)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(ApplicationR)
admin.site.register(AuthorEdition)
admin.site.register(Briefcase, BriefcaseAdmin)
admin.site.register(CancellationReason)
admin.site.register(FundingСycle)
# admin.site.register(Liter)
admin.site.register(PlannedTitle, SchoolTitulAdmin)
admin.site.register(PublisherEdition)
admin.site.register(SchoolTitul, SchoolTitulAdmin)
admin.site.register(StudyDirections)
admin.site.register(Year)
admin.site.register(UMK)
admin.site.register(EditionBriefcase, EditionBriefcaseAdmin)
admin.site.register(PlanEditionTeacher)
admin.site.register(EditionPaperInvoice)
admin.site.register(IncomeExpense)
admin.site.register(ActWriteOff)
admin.site.register(EditionActWrite)

admin.site.register(BooksMovingHead)
admin.site.register(CatVer)
admin.site.register(BooksMovingEdition)
# admin.site.register(Kontingent)
