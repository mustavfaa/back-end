from django.db import models
from portfoli import models as p_models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from transmeta import TransMeta
from django.utils.functional import cached_property
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.utils.functional import cached_property
from django.db.models import F, Sum, ExpressionWrapper
from datetime import timedelta
from django.core.exceptions import ValidationError

STATUS = (
    (0, 'Не показывать'),
    (1, 'Показывать')
)


class StudyDirections(p_models.BaseCatalog):
    pass


class UMK(p_models.BaseCatalog):
    class Meta:
        ordering = ['name_ru']


class ApplicationR(p_models.BaseCatalog):
    pass


class EditionComplex(p_models.BaseCatalog):
    pass


class FundingСycle(p_models.BaseCatalog):
    pass


class CancellationReason(p_models.BaseCatalog):
    pass


class Liter(p_models.BaseRel):
    name = models.CharField(max_length=3,
                            verbose_name=_('Литер класса'),
                            default=None,
                            blank=True)
    sort = models.IntegerField(default=500, )

    class Meta:
        verbose_name = _('Литер класса')
        verbose_name_plural = _('Литеры класса')
        ordering = ['sort']

    def __str__(self):
        return '{}'.format(self.name)


class AuthorEdition(p_models.BaseRel):
    name = models.CharField(verbose_name=_('автор'), max_length=500, default='')

    class Meta:
        verbose_name = _('Автор издетельства')
        verbose_name_plural = _('Авторы издательства')
        ordering = ['name']

    def __str__(self):
        return '{}'.format(self.name)


class PublisherEdition(p_models.BaseCatalog, metaclass=TransMeta):
    name = models.CharField(verbose_name=_('Название издательства'), max_length=150)

    class Meta:
        translate = ('name',)
        verbose_name = _('Издетельство')
        verbose_name_plural = _('Издательства')

    def __str__(self):
        return '{}'.format(self.name)


class Year(p_models.BaseRel):
    year = models.CharField(verbose_name=_('год'), max_length=4, null=True, blank=True)
    status = models.IntegerField(choices=STATUS, null=True, blank=True)

    class Meta:
        verbose_name = _('Год')
        verbose_name_plural = _('Года')

    def __str__(self):
        return '{}'.format(self.year)


class Edition(p_models.BaseRel):
    name = models.CharField(verbose_name=_('название'),
                            max_length=500,
                            blank=True)

    klass = models.ForeignKey(p_models.Klass,
                              null=True,
                              blank=False,
                              on_delete=models.CASCADE,
                              verbose_name=_('класс'))
    study_direction = models.ForeignKey(StudyDirections,
                                        on_delete=models.CASCADE,
                                        verbose_name=_('направления обучения'),
                                        null=True)
    subject = models.ForeignKey(p_models.Subject,
                                on_delete=models.CASCADE,
                                verbose_name=_('предмет'),
                                null=True)
    language = models.ForeignKey(p_models.Language,
                                 null=True,
                                 blank=False,
                                 on_delete=models.CASCADE,
                                 verbose_name=_('язык'))

    author = models.ForeignKey(AuthorEdition,
                               null=True,
                               on_delete=models.CASCADE,
                               verbose_name=_('автор'),
                               blank=True)
    publisher = models.ForeignKey(PublisherEdition,
                                  on_delete=models.CASCADE,
                                  null=True,
                                  verbose_name=_('издатель'),
                                  blank=True)
    publish_date = models.ForeignKey(Year,
                                     on_delete=models.CASCADE,
                                     null=True,
                                     related_name='publish_date',
                                     verbose_name=_('год издания'),
                                     blank=True)
    series_by_year = models.ForeignKey(Year,
                                       on_delete=models.CASCADE,
                                       related_name='series_by_year',
                                       verbose_name=_('серия по годам'),
                                       null=True,
                                       blank=True)
    metodology_complex = models.ForeignKey(UMK,
                                           on_delete=models.CASCADE,
                                           verbose_name=_('Учебно-методический комплекс'),
                                           null=True)
    application_recommendations = models.ForeignKey(ApplicationR,
                                                    on_delete=models.CASCADE,
                                                    verbose_name=_('рекомендации по применению'),
                                                    null=True)
    funding_cycle = models.ForeignKey(FundingСycle,
                                      null=True,
                                      blank=False,
                                      on_delete=models.CASCADE,
                                      verbose_name=_('цикл финансирования'))
    delivery_date = models.DateField(verbose_name=_('дата поставки'),
                                     blank=True,
                                     null=True)
    delivery_document = models.CharField(verbose_name=_('документ поставки'),
                                         max_length=200,
                                         default=0,
                                         blank=True)
    amount = models.FloatField(verbose_name=_('сумма'),
                               default=0,
                               blank=True)
    cancellation_date = models.DateField(verbose_name=_('дата отмены'),
                                         blank=True,
                                         null=True)
    cancellation_reason = models.ForeignKey(CancellationReason,
                                            blank=True,
                                            on_delete=models.CASCADE,
                                            verbose_name=_('причина отмены'),
                                            null=True)
    quality_claims = models.CharField(verbose_name=_('претензии по качеству'),
                                      max_length=200,
                                      blank=True)
    mistakes = models.CharField(verbose_name=_('ошибки'),
                                max_length=200,
                                blank=True)
    image = models.ImageField(verbose_name=_('изображение'),
                              upload_to='editions/',
                              null=True,
                              blank=True)
    isbn = models.CharField(verbose_name=_('ISBN код'),
                            max_length=500,
                            null=True,
                            blank=True)
    edition_complex = models.ForeignKey(EditionComplex,
                                        null=True,
                                        blank=True,
                                        on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('издание')
        verbose_name_plural = _('издания')
        ordering = ['klass__id', 'subject__sort', 'name']

    def __str__(self):
        return '{}'.format(self.name)


class NumberBooks(p_models.BaseRel):
    school = models.ForeignKey(p_models.AlmaMater,
                               on_delete=models.CASCADE,
                               verbose_name=_('школа'),
                               null=True,
                               blank=True)
    edition = models.ForeignKey(Edition,
                                on_delete=models.CASCADE,
                                verbose_name=_('издание'),
                                null=True,
                                blank=True)
    summ = models.IntegerField(verbose_name=_('сумма'), default=0, blank=True)
    in_warehouse = models.IntegerField(verbose_name=_('на складе'), default=0, blank=True)
    it_filled = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  null=True,
                                  verbose_name=_('заполнил'),
                                  blank=True)
    amounts = models.IntegerField(default=0, verbose_name='сумма', blank=True)
    in_register = models.BooleanField(default=False, verbose_name='В регистре')

    is_record_to_register = False

    class Meta:
        # unique_together = [['school', 'edition']]
        verbose_name = _('количество книг изданий')
        verbose_name_plural = _('количество книг изданий')

    def __str__(self):
        return '{}'.format(self.id)

    def save(self, *args, **kwargs):
        self.summ = round(self.summ, 2)

        if not self.is_record_to_register:
            self.in_register = False
        else:
            self.in_register = True

        super(NumberBooks, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        try:
            IncomeExpense.objects.get(
                number_book_id=self.pk,
            ).delete()
        except:
            pass
        super(NumberBooks, self).delete(self, *args, **kwargs)

    @property
    def results(self):
        res = dict()
        # try:
        values = IncomeExpense.objects.filter(
            edition=self.edition,
            school=self.school,
            object_id__isnull=False
        ).annotate(
            x=F('quantity') * F('type_of_movement'),
            s=ExpressionWrapper(F('summ') * F('type_of_movement'), output_field=models.FloatField()),
        ).aggregate(sum_q=Sum('x'), sum_s=Sum('s'))
        if values['sum_q']:
            res['quantity'] = values['sum_q'] + self.in_warehouse
        else:
            res['quantity'] = self.in_warehouse
        if values['sum_s']:
            res['summ'] = values['sum_s'] + self.summ
        else:
            res['summ'] = self.summ
        if res['summ'] and res['quantity']:
            res['amount'] = round(res['summ'] / res['quantity'], 2)
        else:
            res['amount'] = 0
        # except:
        #     res['quantity'] = self.in_warehouse
        #     res['summ'] = self.summ
        return res


# Портфель
class Briefcase(p_models.BaseRel):
    name = models.CharField(verbose_name=_('название портфеля'), max_length=70, blank=True)
    school = models.ForeignKey(p_models.AlmaMater, on_delete=models.CASCADE, verbose_name=_('школа'), blank=True)
    klass = models.ForeignKey(p_models.Klass, on_delete=models.CASCADE, verbose_name=_('класс'), null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('автор'), blank=True)
    description = models.CharField(verbose_name=_('описание'), max_length=50, blank=True)
    language = models.ForeignKey(p_models.Language, on_delete=models.CASCADE, verbose_name=_('язык обучения'),
                                 null=True, blank=True)
    year = models.ForeignKey(p_models.DateObjects,
                             on_delete=models.CASCADE,
                             verbose_name=_('Учебный год'),
                             null=True)
    status = models.BooleanField(default=False, blank=True, verbose_name=_('Статус'))
    date = models.DateField(auto_now_add=True, null=True)
    study_direction = models.ForeignKey(StudyDirections,
                                        on_delete=models.SET_NULL,
                                        verbose_name=_('направления обучения'),
                                        null=True, blank=True)

    class Meta:
        verbose_name = _('Портфель')
        verbose_name_plural = _("Портфели")
        ordering = ['school', 'author']

    @cached_property
    def editions_val(self):
        return self.editions.all()

    def __str__(self):
        return '{}'.format(self.name)


# Книги портфелей
class EditionBriefcase(p_models.BaseRel):
    briefcase = models.ForeignKey(Briefcase,
                                  on_delete=models.CASCADE,
                                  verbose_name=_('Портфель'),
                                  related_name='editions',
                                  blank=True)
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, verbose_name=_('Издание'), blank=True)
    surplus = models.SmallIntegerField(default=0, verbose_name=_('Процент обеспечения'))

    class Meta:
        verbose_name = _('Издание портфеля')
        verbose_name_plural = _("Издания портфелей")
        ordering = ['briefcase']

    def __str__(self):
        return '{} - {}'.format(self.briefcase.name, self.edition.name)


class SchoolTitulHead(p_models.BaseRel):
    date = models.DateField(auto_now_add=True)
    school = models.ForeignKey(p_models.AlmaMater,
                               on_delete=models.CASCADE,
                               verbose_name=_('школа'),
                               )
    klass = models.ForeignKey(p_models.Klass,
                              on_delete=models.CASCADE,
                              verbose_name=_('класс'))
    liter = models.ForeignKey(Liter,
                              on_delete=models.CASCADE,
                              verbose_name=_('Название класса'),
                              null=True
                              )
    year = models.ForeignKey(p_models.DateObjects,
                             on_delete=models.CASCADE,
                             verbose_name=_('Учебный год'),
                             )
    students = models.IntegerField(verbose_name=_('количество учащихся'), default=0,
                                   )

    status = models.BooleanField(default=False, blank=True, verbose_name=_('Статус'))
    language = models.ForeignKey(p_models.Language,
                                 on_delete=models.CASCADE, null=True,
                                 verbose_name=_('язык обучения'),
                                 )
    study_direction = models.ForeignKey(StudyDirections,
                                        on_delete=models.CASCADE,
                                        verbose_name=_('направления обучения'),
                                        null=True
                                        )
    kurator = models.ForeignKey(p_models.User, on_delete=models.CASCADE, null=True)
    briefcase = models.ForeignKey(Briefcase,
                                  on_delete=models.CASCADE,
                                  verbose_name=_('Титульный список'),
                                  null=True, blank=True,
                                  )

    class Meta:
        # unique_together = ['klass', 'school', 'liter', 'year', 'status']
        verbose_name = _('Титул школы заголовок')
        verbose_name_plural = _('Титулы школы заголовки')

    def __str__(self):
        return '{}'.format(self.id)

    def save(self, *args, **kwargs):
        if self.deleted:
            self.status = False

        super(SchoolTitulHead, self).save(*args, **kwargs)


#
# class SchoolTitulPlannedHead(p_models.BaseRel):
#
#     uid = models.UUIDField(null=True)
#
#     date = models.DateField(auto_now_add=True)
#     school = models.ForeignKey(p_models.AlmaMater,
#                                on_delete=models.CASCADE,
#                                verbose_name=_('школа'),
#                                )
#     klass = models.ForeignKey(p_models.Klass,
#                               on_delete=models.CASCADE,
#                               verbose_name=_('класс'))
#     liter = models.ForeignKey(Liter,
#                               on_delete=models.CASCADE,
#                               verbose_name=_('Название класса'),
#                               null=True
#                               )
#     year = models.ForeignKey(p_models.DateObjects,
#                              on_delete=models.CASCADE,
#                              verbose_name=_('Учебный год'),
#                              )
#     students = models.IntegerField(verbose_name=_('количество учащихся'), default=0,
#                                    )
#
#     status = models.BooleanField(default=False, blank=True, verbose_name=_('Статус'))
#     language = models.ForeignKey(p_models.Language,
#                                  on_delete=models.CASCADE,
#                                  verbose_name=_('язык обучения'),
#                                  )
#     study_direction = models.ForeignKey(StudyDirections,
#                                         on_delete=models.CASCADE,
#                                         verbose_name=_('направления обучения'),
#                                         null=True
#                                         )
#
#
#     class Meta:
#         # unique_together = ['klass', 'school', 'liter', 'year', 'status']
#         pass


class SchoolTitulPlannedHead(p_models.BaseRel):
    date = models.DateField(auto_now_add=True)
    school = models.ForeignKey(p_models.AlmaMater,
                               on_delete=models.CASCADE,
                               verbose_name=_('школа'),
                               )
    klass = models.ForeignKey(p_models.Klass,
                              on_delete=models.CASCADE,
                              verbose_name=_('класс'))
    liter = models.ForeignKey(Liter,
                              on_delete=models.CASCADE,
                              verbose_name=_('Название класса'),
                              null=True
                              )
    year = models.ForeignKey(p_models.DateObjects,
                             on_delete=models.CASCADE,
                             verbose_name=_('Учебный год'),
                             )
    students = models.IntegerField(verbose_name=_('количество учащихся'), default=0,
                                   )
    percent = models.IntegerField(verbose_name=_('Процент'), default=0, blank=True,
                                  )
    status = models.BooleanField(default=False, blank=True, verbose_name=_('Статус'))
    language = models.ForeignKey(p_models.Language,
                                 on_delete=models.CASCADE,
                                 verbose_name=_('язык обучения'),
                                 )
    study_direction = models.ForeignKey(StudyDirections,
                                        on_delete=models.CASCADE,
                                        verbose_name=_('направления обучения'),
                                        null=True
                                        )
    titul = models.ForeignKey(SchoolTitulHead,
                              on_delete=models.CASCADE,
                              verbose_name=_('Титульный список'),
                              null=True, blank=True,
                              )

    briefcase = models.ForeignKey(Briefcase,
                                  on_delete=models.CASCADE,
                                  verbose_name=_('Титульный список'),
                                  null=True, blank=True,
                                  )

    class Meta:
        # unique_together = ['klass', 'school', 'liter', 'year', 'status']
        verbose_name = _('Плановый Титул школы заголовок')
        verbose_name_plural = _('Плановый Титулы школы заголовки')

    def __str__(self):
        return '{}'.format(self.id)

    def save(self, *args, **kwargs):
        if self.deleted:
            self.status = False

        super(SchoolTitulPlannedHead, self).save(*args, **kwargs)


class SchoolTitul(p_models.BaseRel):
    titul_head = models.ForeignKey(SchoolTitulHead, related_name='school_titul',
                                   null=True, on_delete=models.SET_NULL,
                                   blank=True)
    school = models.ForeignKey(p_models.AlmaMater,
                               on_delete=models.CASCADE,
                               verbose_name=_('школа'),
                               null=True,
                               blank=True)
    klass = models.ForeignKey(p_models.Klass,
                              on_delete=models.CASCADE,
                              verbose_name=_('класс'))
    liter = models.ForeignKey(Liter,
                              on_delete=models.CASCADE,
                              verbose_name=_('Название класса'),
                              default=None,
                              null=True,
                              blank=True)
    students = models.IntegerField(verbose_name=_('количество учащихся'),
                                   blank=True)
    year = models.ForeignKey(p_models.DateObjects,
                             on_delete=models.CASCADE,
                             verbose_name=_('Учебный год'),
                             blank=True)
    language = models.ForeignKey(p_models.Language,
                                 on_delete=models.CASCADE,
                                 verbose_name=_('язык обучения'),
                                 blank=True)
    study_direction = models.ForeignKey(StudyDirections,
                                        on_delete=models.CASCADE,
                                        verbose_name=_('направления обучения'),
                                        null=True,
                                        blank=True)

    class Meta:
        verbose_name = _('Титул школы')
        verbose_name_plural = _('Титулы школы')

    def __str__(self):
        return '{}'.format(self.id)


class PlannedTitle(p_models.BaseRel):
    klass = models.ForeignKey(p_models.Klass, on_delete=models.CASCADE,
                              verbose_name=_('класс'), null=True)
    school_titul = models.ForeignKey(SchoolTitul, on_delete=models.CASCADE, verbose_name=_('титул школы'), null=True,
                                     blank=True)
    school = models.ForeignKey(p_models.AlmaMater, on_delete=models.CASCADE, verbose_name=_('школа'), blank=True)
    liter = models.ForeignKey(Liter, on_delete=models.CASCADE, verbose_name=_('Название класса'), null=True, blank=True)
    students = models.IntegerField(verbose_name=_('количество учащихся'), null=True, blank=True)
    year = models.ForeignKey(p_models.DateObjects, on_delete=models.SET_NULL, verbose_name=_('Учебный год'), null=True,
                             blank=True)
    language = models.ForeignKey(p_models.Language, on_delete=models.SET_NULL, verbose_name=_('язык обучения'),
                                 null=True, blank=True)
    study_direction = models.ForeignKey(StudyDirections,
                                        on_delete=models.SET_NULL,
                                        verbose_name=_('направления обучения'),
                                        null=True, blank=True)
    planned_quantity = models.IntegerField(verbose_name=_('плановое количество учащихся'), blank=True)
    briefcase = models.ForeignKey(Briefcase,
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True,
                                  related_name='plan_tituls',
                                  verbose_name=_('Портфель')
                                  )

    class Meta:
        verbose_name = _('плановый титул школы')
        verbose_name_plural = _("плановый титульный список")
        ordering = ['school', 'klass']

    def __str__(self):
        return '{}'.format(self.id)


class PlanEditionTeacher(p_models.BaseRel):
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, verbose_name=_('Издание'), blank=True)
    quantity = models.SmallIntegerField(default=99, verbose_name=_('Количество'))
    school = models.ForeignKey(p_models.AlmaMater, on_delete=models.CASCADE, verbose_name=_('школа'), blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('автор'), blank=True)
    year = models.ForeignKey(p_models.DateObjects, on_delete=models.SET_NULL, verbose_name=_('Учебный год'), null=True,
                             blank=True)

    class Meta:
        verbose_name = _('Издание для учителей')
        verbose_name_plural = _("Издания для учителей")
        ordering = ['edition']

    def __str__(self):
        return '{}'.format(self.edition.name)


class Provider(p_models.BaseRel):
    name = models.CharField(verbose_name=_('Наименование поставщика'), max_length=300)

    class Meta:
        verbose_name = _('Поставщик')
        verbose_name_plural = _("Поставщики")

    def __str__(self):
        return '{}'.format(self.name)


class Invoice(p_models.BaseRel):
    date = models.DateField(auto_now_add=True)
    number = models.CharField(verbose_name=_('Номер счет фактуры'),
                              max_length=300,
                              default='',
                              blank=True)
    year = models.ForeignKey(Year,
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True)
    school = models.ForeignKey(p_models.AlmaMater,
                               on_delete=models.CASCADE,
                               verbose_name=_('школа'),
                               blank=True)
    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               verbose_name=_('Автор'),
                               null=True,
                               blank=True)
    provider = models.ForeignKey(Provider,
                                 verbose_name=_('Поставщик'),
                                 on_delete=models.SET_NULL,
                                 related_name='provider_invoices',
                                 null=True,
                                 blank=True)
    publisher = models.ForeignKey(PublisherEdition,
                                  on_delete=models.CASCADE,
                                  null=True,
                                  verbose_name=_('издательство'),
                                  blank=True)
    power_of_attorney = models.CharField(verbose_name=_('номер доверенности'),
                                         max_length=300,
                                         null=True,
                                         blank=True)
    date_power_of_attorney = models.DateField(null=True,
                                              blank=True,
                                              verbose_name=_('Дата доверености'))
    confidant = models.ForeignKey(p_models.Portfolio,
                                  on_delete=models.SET_NULL,
                                  verbose_name=_('Доверенное лицо'),
                                  null=True,
                                  blank=True)
    date_extracts = models.DateField(verbose_name=_('дата выписки поставщика'),
                                     null=True,
                                     blank=True)
    shipper = models.ForeignKey(Provider,
                                verbose_name=_('Грузоотправитель'),
                                on_delete=models.SET_NULL,
                                related_name='shipper_invoices',
                                null=True,
                                blank=True)
    freight_carrier = models.ForeignKey(Provider,
                                        verbose_name=_('Грузоперевозчик'),
                                        related_name='freight_carrier_invoices',
                                        on_delete=models.SET_NULL,
                                        null=True,
                                        blank=True)
    number_provider = models.CharField(verbose_name=_('Номер поставщика'),
                                       max_length=300,
                                       default='',
                                       blank=True)
    status = models.BooleanField(default=False, blank=True, verbose_name=_('Статус'))

    class Meta:
        verbose_name = _('накладная')
        verbose_name_plural = _("накладные")
        ordering = ['-date', 'id']

    def __str__(self):
        return 'накладная от шк №{}'.format(self.school.name)

    @cached_property
    def editions_val(self):
        return self.editioninvoice_set.all()

    @cached_property
    def amount(self):
        amount = 0
        for obj in self.editioninvoice_set.all().values('amount', 'planned_quantity'):
            amount += obj['amount'] * obj['planned_quantity']
        return amount

    def save(self, *args, **kwargs):
        super(Invoice, self).save(*args, **kwargs)
        content_type = ContentType.objects.get_for_model(self)
        IncomeExpense.objects.filter(content_type=content_type, object_id=self.id).delete()
        if self.status:
            for eid in self.editioninvoice_set.all():
                IncomeExpense.objects.create(
                    ie_object=self,
                    school_id=self.school.id,
                    type_of_movement=1,
                    quantity=eid.quantity,
                    edition_id=eid.edition_id,
                    summ=eid.amount,
                    type=2,
                    date=self.date,
                    income=self.id,
                    income_type=1,
                )

    def delete(self, *args, **kwargs):
        content_type = ContentType.objects.get_for_model(self)
        IncomeExpense.objects.filter(content_type=content_type, object_id=self.id).delete()
        super(Invoice, self).delete(*args, **kwargs)


class IncomeExpense(p_models.BaseRel):
    CHOICE = (
        (1, _('Остаток')),
        (2, _('Приход')),
        (3, _('Расход'))
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField(null=True)
    ie_object = GenericForeignKey("content_type", "object_id")
    school = models.ForeignKey(p_models.AlmaMater, verbose_name=_('школа'), on_delete=models.CASCADE, null=True,
                               blank=True)
    type_of_movement = models.IntegerField(verbose_name=_('вид движения'), blank=True, default=0)
    quantity = models.IntegerField(verbose_name=_('количество'), blank=True, default=0)
    summ = models.FloatField(verbose_name=_('Сумма'), blank=True, default=0)
    edition = models.ForeignKey(Edition, on_delete=models.SET_NULL, null=True, blank=True)
    number_book = models.ForeignKey(NumberBooks, on_delete=models.CASCADE, null=True, blank=True)
    type = models.SmallIntegerField(choices=CHOICE, null=True, blank=True)
    date = models.DateField(verbose_name='Дата накладной', null=True, blank=True)
    income = models.IntegerField(verbose_name=_('id_прихода'), default=0, blank=True)
    income_type = models.IntegerField(verbose_name=_('Тип приходного документа'), default=0,
                                      blank=True)  # 0 - ввод остатков  1 - электрон 2 - бумаж 3 - приход с перемещения

    class Meta:
        verbose_name = _('приход/расход')
        verbose_name_plural = _("приходы/расходы")
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.summ = round(self.summ, 2)
        # if not self.pk:
        #     n_boock, created = NumberBooks.objects.get_or_create(school=self.school, edition=self.edition)
        super(IncomeExpense, self).save(*args, **kwargs)


class EditionInvoice(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, verbose_name=_('Накладная'), null=True, blank=True)
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('издание'))
    quantity = models.IntegerField(verbose_name=_('количество'), default=0, blank=True)
    planned_quantity = models.IntegerField(verbose_name=_('плановое количество'), default=0, blank=True)
    amount = models.FloatField(verbose_name=_('Сумма'), default=0, blank=True)
    tags = GenericRelation(IncomeExpense, related_query_name='edition_invoice')

    class Meta:
        verbose_name = _('Книги накладной в издательстве')
        verbose_name_plural = _("Книги наглодных в издательстве")
        ordering = ['id']

    def __str__(self):
        return 'Книги для накладной №{}'.format(self.invoice.id)

    def save(self, *args, **kwargs):
        self.amount = round(self.amount, 2)
        super(EditionInvoice, self).save(*args, **kwargs)


def validate_bin_length(value):
    for i in value:
        try:
            int(i)
        except:
            raise ValidationError(
                _('Не верно указан БИН'),
                params={'value': value},
            )


class PaperInvoice(p_models.BaseRel):
    idx = models.CharField(verbose_name='Номер накладной', default=_("Нет номера на накладной"), max_length=300,
                           blank=True)
    date = models.DateField(verbose_name='Дата накладной')
    provider = models.CharField(verbose_name=_('Поставщик'), max_length=1000, blank=True)
    bin = models.CharField(verbose_name=_('БИН'), validators=[validate_bin_length], max_length=12)  # TODO CharField
    number = models.CharField(verbose_name=_('Номер счет фактуры'), max_length=300, default='', blank=True)
    date_invoice = models.DateField(verbose_name=_('дата счет фактуры'), blank=True)
    school = models.ForeignKey(p_models.AlmaMater,
                               on_delete=models.CASCADE,
                               verbose_name=_('школа'),
                               blank=True)
    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               verbose_name=_('Автор'),
                               null=True,
                               blank=True)
    status = models.BooleanField(default=False, blank=True, verbose_name=_('Статус'))

    class Meta:
        verbose_name = _('бумажная накладная')
        verbose_name_plural = _("бумажные накладные")

    def __str__(self):
        return 'бумажная накладная от шк №{}'.format(self.school.name)

    @cached_property
    def editions_val(self):
        return self.editions_invoice.all()

    @cached_property
    def amount(self):
        amount = sum(self.editions_invoice.all().values_list('amount', flat=True))
        # for obj in self.editions_invoice.all().values('amount', 'quantity'):
        #     amount += obj['amount'] * obj['quantity']
        return amount

    def clean(self):
        if 12 > len(self.bin) <= 0:
            raise ValidationError(_("Не правильно введен БИН"))
        # if self.date < timezone.now().date() - timedelta(days=3) or self.date > timezone.now().date():
        #     raise ValidationError(_("Время больше текущего дня или меньше на 3 дня"))

    def save(self, *args, **kwargs):
        if self.deleted:
            self.status = False
        super(PaperInvoice, self).save(*args, **kwargs)
        content_type = ContentType.objects.get_for_model(self)
        IncomeExpense.objects.filter(content_type=content_type, object_id=self.id).delete()

        if self.status:
            for eid in self.editions_invoice.all():
                IncomeExpense.objects.create(
                    ie_object=self,
                    school_id=self.school.id,
                    type_of_movement=1,
                    quantity=eid.quantity,
                    edition_id=eid.edition.id,
                    summ=eid.amount,
                    type=2,
                    date=self.date,
                    income=self.id,
                    income_type=2,
                )

    def delete(self, *args, **kwargs):
        content_type = ContentType.objects.get_for_model(self)
        IncomeExpense.objects.filter(content_type=content_type, object_id=self.id).delete()
        super(PaperInvoice, self).delete(*args, **kwargs)


class EditionPaperInvoice(models.Model):
    invoice = models.ForeignKey(PaperInvoice, related_name='editions_invoice', on_delete=models.CASCADE,
                                verbose_name=_('Накладная'), blank=True)
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, blank=True, verbose_name=_('издание'))
    quantity = models.IntegerField(verbose_name=_('количество'), default=0, blank=True)
    amount = models.FloatField(verbose_name=_('сумма'), default=0, blank=True)
    tags = GenericRelation(IncomeExpense, related_query_name='edition_paper_invoice')

    class Meta:
        # unique_together = ('invoice', 'edition')
        verbose_name = _('Книги для бумажной накладной в издательстве')
        verbose_name_plural = _("Книги для бумажных наглодных в издательстве")
        ordering = ['id']

    def __str__(self):
        return 'Книги для бумажной накладной №{}'.format(self.invoice.id)

    def save(self, *args, **kwargs):
        self.amount = round(self.amount, 2)
        super(EditionPaperInvoice, self).save(*args, **kwargs)


class RequestEdition(p_models.BaseRel):
    edition = models.ForeignKey(Edition,
                                on_delete=models.CASCADE,
                                blank=True,
                                verbose_name=_('издание'))
    shipper = models.ForeignKey(p_models.AlmaMater,
                                verbose_name=_('Школа получатель'),
                                on_delete=models.SET_NULL,
                                related_name='shipper',
                                null=True,
                                blank=True)
    provider = models.ForeignKey(p_models.AlmaMater,
                                 verbose_name=_('Школа поставщик'),
                                 on_delete=models.SET_NULL,
                                 related_name='provider',
                                 null=True,
                                 blank=True)
    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               verbose_name=_('Автор'),
                               null=True,
                               blank=True)
    date_time = models.DateTimeField(auto_now_add=True,
                                     blank=True,
                                     verbose_name=_('время заявки'))
    checkid = models.BooleanField(verbose_name=_('статус'), default=False, blank=True)
    quantity = models.IntegerField(verbose_name=_('количество'), default=0, blank=True)
    tags = GenericRelation(IncomeExpense, related_query_name='request_edition')

    class Meta:
        # unique_together = ('shipper', 'edition')
        verbose_name = _('Заявка на перемещение')
        verbose_name_plural = _("Заявки на перемешение")
        ordering = ['id']

    @cached_property
    def scheckids(self):
        return self.checkidrequestedition_set.all()


class CheckidRequestEdition(p_models.BaseRel):
    request_edition = models.ForeignKey(RequestEdition, on_delete=models.CASCADE, blank=True, verbose_name=_('Заявка'))
    school = models.ForeignKey(p_models.AlmaMater,
                               verbose_name=_('Школа'),
                               on_delete=models.SET_NULL,
                               related_name='school',
                               null=True,
                               blank=True)
    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               verbose_name=_('Автор'),
                               null=True,
                               blank=True)
    date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=_('время просмотра'))
    check = models.BooleanField(null=True, verbose_name=_('статус подверждение/отказ'), blank=True)
    check2 = models.BooleanField(verbose_name=_('статус'), default=False, blank=True)
    quantity = models.IntegerField(verbose_name=_('количество'), default=0, blank=True)

    # tags = GenericRelation(IncomeExpense, related_query_name='checkid_request')

    class Meta:
        unique_together = ('request_edition', 'school')
        verbose_name = _('Статус просмотра')
        verbose_name_plural = _("Статусы просмотра")
        ordering = ['id']


class ActWriteOff(p_models.BaseRel):
    idx = models.CharField(
        verbose_name='Номер акта',
        default=_("Нету номера акта"),
        max_length=300,
        blank=True
    )
    date = models.DateField(auto_now_add=True)
    date_write = models.DateField(verbose_name=_('дата на списание'), blank=True)
    school = models.ForeignKey(p_models.AlmaMater,
                               on_delete=models.CASCADE,
                               verbose_name=_('школа'),
                               blank=True)
    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               verbose_name=_('Автор'),
                               null=True,
                               blank=True)
    footing = models.TextField(null=True, verbose_name=_('Основание'))
    members_of_commission = models.TextField(null=True, verbose_name=_('члены комиссии'))
    status = models.BooleanField(default=False, blank=True, verbose_name=_('Статус'))
    amount = models.FloatField(verbose_name=_('Сумма'), default=0, blank=True)

    class Meta:
        ordering = ['date']
        verbose_name = _('Акт на списание')
        verbose_name_plural = _("Акты на списание")

    def __str__(self):
        return 'Акт на списание от шк №{}'.format(self.school.name)

    @cached_property
    def editions_val(self):
        return self.editions_invoice.all()

    # @cached_property
    # def amount(self):
    #     amount = 0
    #     for obj in self.editions_invoice.all().values('amount', 'quantity'):
    #         amount += obj['amount'] * obj['quantity']
    #     return amount

    def save(self, *args, **kwargs):
        if self.deleted:
            self.status = False
        self.amount = 0
        for eid in self.editions_invoice.all():
            self.amount += eid.amount
        super(ActWriteOff, self).save(*args, **kwargs)
        content_type = ContentType.objects.get_for_model(self)
        IncomeExpense.objects.filter(content_type=content_type, object_id=self.id).delete()

        if self.status:
            for eid in self.editions_invoice.all():
                IncomeExpense.objects.create(
                    ie_object=self,
                    school_id=self.school.id,
                    type_of_movement=-1,
                    quantity=eid.quantity,
                    edition_id=eid.edition.id,
                    summ=eid.amount,
                    type=3,
                    date=self.date,
                    income=eid.income,
                    income_type=eid.income_type,
                )

    def delete(self, *args, **kwargs):
        content_type = ContentType.objects.get_for_model(self)
        IncomeExpense.objects.filter(content_type=content_type, object_id=self.id).delete()
        super(ActWriteOff, self).delete(*args, **kwargs)


class EditionActWrite(models.Model):
    invoice = models.ForeignKey(ActWriteOff, related_name='editions_invoice', on_delete=models.CASCADE,
                                verbose_name=_('Акт на списание'), blank=True)
    number = models.CharField(verbose_name=_('Инвентарный номер'), max_length=1000, null=True, blank=True)
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, blank=True, verbose_name=_('издание'))
    quantity = models.IntegerField(verbose_name=_('количество'), default=0, blank=True)
    amount = models.FloatField(verbose_name=_('Сумма'), default=0, blank=True)
    has = models.FloatField(verbose_name=_('Кол ост'), default=0, blank=True)
    summ = models.FloatField(verbose_name=_('Сумма ост'), default=0, blank=True)
    price = models.FloatField(verbose_name=_('Цена'), default=0, blank=True)
    tags = GenericRelation(IncomeExpense, related_query_name='edition_act_write')
    income = models.IntegerField(verbose_name=_('id_прихода'), default=0, blank=True)
    income_type = models.IntegerField(verbose_name=_('id_типа_прихода'), default=0, blank=True)

    class Meta:
        unique_together = ('invoice', 'edition', 'income', 'income_type')
        verbose_name = _('Книга для акта на списание')
        verbose_name_plural = _("Книги для актов на списание")
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.amount = round(self.amount, 2)
        super(EditionActWrite, self).save(*args, **kwargs)

    def __str__(self):
        return 'Книги на списание №{}'.format(self.invoice.id)


class InitialBalance(p_models.BaseRel):
    school = models.ForeignKey(p_models.AlmaMater,
                               on_delete=models.CASCADE,
                               verbose_name=_('школа'),
                               blank=True)
    date = models.DateField(verbose_name='Дата ввода остатков',
                            null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('автор'),
                               blank=True,
                               null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('начальный остаток')
        verbose_name_plural = _("начальные остатки")

    def __str__(self):
        return 'начальный остаток от шк №{}'.format(self.school.name)

    @cached_property
    def editions_val(self):
        return self.editions_invoice.all()

    @cached_property
    def amount(self):
        amount = sum(self.editions_invoice.all().values_list('amount', flat=True))
        # for obj in self.editions_invoice.all().values('amount', 'quantity'):
        #     amount += obj['amount'] * obj['quantity']
        return amount

    def save(self, *args, **kwargs):

        if self.deleted:
            self.status = False

        super(InitialBalance, self).save(*args, **kwargs)
        content_type = ContentType.objects.get_for_model(self)
        IncomeExpense.objects.filter(content_type=content_type, object_id=self.id).delete()
        if self.status:
            objs = self.editions_invoice.all()
            for eid in objs:
                # if eid.amount == 0:
                #     eid.amount = eid.edition.amount*eid.quantity
                #     eid.save()
                IncomeExpense.objects.create(
                    ie_object=self,
                    school_id=self.school.id,
                    type_of_movement=1,
                    quantity=eid.quantity,
                    edition_id=eid.edition.id,
                    summ=eid.amount,
                    type=1,
                    income=self.id,
                    income_type=0,
                    date=self.date
                )
                # print(eid)

    def delete(self, *args, **kwargs):
        content_type = ContentType.objects.get_for_model(self)
        IncomeExpense.objects.filter(content_type=content_type, object_id=self.id).delete()
        super(InitialBalance, self).delete(*args, **kwargs)


class EditionInitialBalance(models.Model):
    invoice = models.ForeignKey(InitialBalance, related_name='editions_invoice', on_delete=models.CASCADE,
                                verbose_name=_('Начальный остаток'), blank=True)
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, blank=True, verbose_name=_('издание'))
    quantity = models.IntegerField(verbose_name=_('количество'), default=0, blank=True)
    amount = models.FloatField(verbose_name=_('сумма'), default=0, blank=True)
    tags = GenericRelation(IncomeExpense, related_query_name='edition_initial_balance')

    class Meta:
        # unique_together = ('invoice', 'edition')
        verbose_name = _('Книги для начальных остатков в издательстве')
        verbose_name_plural = _("Книги для начальных остатковх в издательстве")
        ordering = ['id']

    def __str__(self):
        return 'Книги для начальных остатков №{}'.format(self.invoice.id)

    def save(self, *args, **kwargs):
        self.amount = round(self.amount, 2)
        super(EditionInitialBalance, self).save(*args, **kwargs)


class BooksOrder(p_models.BaseRel):
    school = models.ForeignKey(p_models.AlmaMater,
                               on_delete=models.CASCADE,
                               verbose_name=_('школа'),
                               blank=True)
    date = models.DateField(verbose_name='Дата ввода остатков',
                            null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name=_('автор'),
                               blank=True,
                               null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Заявка на книги')
        verbose_name_plural = _("Заявки на книги")

    @cached_property
    def editions_val(self):
        return self.editions_invoice.all()

    def save(self, *args, **kwargs):
        if self.deleted:
            self.status = False
        super(BooksOrder, self).save(*args, **kwargs)


class EditionBooksOrder(models.Model):
    invoice = models.ForeignKey(BooksOrder, related_name='editions_invoice', on_delete=models.CASCADE,
                                verbose_name=_('Заявка на книги'), blank=True)
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, blank=True, verbose_name=_('издание'))
    quantity = models.IntegerField(verbose_name=_('количество'), default=0, blank=True)

    class Meta:
        # unique_together = ('invoice', 'edition')
        verbose_name = _('Книги для заявки')
        verbose_name_plural = _("Книги для заявок")
        ordering = ['id']


class BooksRecall(p_models.BaseRel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    school = models.ForeignKey(p_models.AlmaMater, on_delete=models.CASCADE)
    order = models.ForeignKey(BooksOrder, on_delete=models.CASCADE,
                              null=True,
                              blank=False)
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    quanity_after_recall = models.IntegerField(default=0,
                                               blank=True)

    def save(self, *args, **kwargs):
        super(BooksRecall, self).save(*args, **kwargs)


class BooksMovingHead(p_models.BaseRel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient_school = models.ForeignKey(p_models.AlmaMater,
                                         on_delete=models.CASCADE,
                                         related_name='recipient_school')
    sender_school = models.ForeignKey(p_models.AlmaMater,
                                      on_delete=models.CASCADE,
                                      related_name='sender_school')
    date = models.DateField(verbose_name='Дата перемещения',
                            null=True)
    status = models.BooleanField(default=False)
    recall = models.ForeignKey(BooksRecall,
                               on_delete=models.CASCADE,
                               null=True)

    class Meta:
        verbose_name = _('Перемещение')
        verbose_name_plural = _("Перемещения")
        ordering = ['id']

    def save(self, *args, **kwargs):
        if self.deleted:
            self.status = False
        super(BooksMovingHead, self).save(*args, **kwargs)
        content_type = ContentType.objects.get_for_model(self)
        IncomeExpense.objects.filter(content_type=content_type, object_id=self.id).delete()
        if self.status:
            for eid in self.editions_val.all():
                IncomeExpense.objects.create(
                    ie_object=self,
                    school_id=self.sender_school.id,
                    type_of_movement=-1,
                    quantity=eid.quantity,
                    edition_id=eid.edition.id,
                    summ=eid.amount,
                    type=3,
                    date=self.date,
                    income=eid.income,
                    income_type=eid.income_type, )
                IncomeExpense.objects.create(
                    ie_object=self,
                    school_id=self.recipient_school.id,
                    type_of_movement=1,
                    quantity=eid.quantity,
                    edition_id=eid.edition.id,
                    summ=eid.amount,
                    type=2,
                    date=self.date,
                    income=self.id,
                    income_type=3, )

    def delete(self, *args, **kwargs):
        content_type = ContentType.objects.get_for_model(self)
        IncomeExpense.objects.filter(content_type=content_type, object_id=self.id).delete()
        super(BooksMovingHead, self).delete(*args, **kwargs)


class BooksMovingEdition(models.Model):
    invoice = models.ForeignKey(BooksMovingHead,
                                related_name='editions_val',
                                on_delete=models.CASCADE)
    number = models.CharField(verbose_name=_('Инвентарный номер'), max_length=1000, null=True, blank=True)
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, blank=True, verbose_name=_('издание'))
    quantity = models.IntegerField(verbose_name=_('количество'), default=0, blank=True)
    amount = models.FloatField(verbose_name=_('Сумма'), default=0, blank=True)
    has = models.FloatField(verbose_name=_('Кол ост'), default=0, blank=True)
    summ = models.FloatField(verbose_name=_('Сумма ост'), default=0, blank=True)
    price = models.FloatField(verbose_name=_('Цена'), default=0, blank=True)
    tags = GenericRelation(IncomeExpense, related_query_name='edition_act_write')
    income = models.IntegerField(verbose_name=_('id_прихода'), default=0, blank=True)
    income_type = models.IntegerField(verbose_name=_('id_типа_прихода'), default=0, blank=True)

    class Meta:
        verbose_name = _('Книга для перемещения')
        verbose_name_plural = _("Книги для перемещения")
        ordering = ['id']


from django.core.cache import cache


class CatVer(models.Model):
    ver = models.CharField(default='0', max_length=255)

    def save(self, *args, **kwargs):
        cache.set('all_editions_for_api', None)
        super(CatVer, self).save(*args, **kwargs)

#
# class InitialBalance1(p_models.BaseRel):
#     school = models.ForeignKey(p_models.AlmaMater,
#                                on_delete=models.CASCADE,
#                                verbose_name=_('школа'),
#                                blank=True)
#     date = models.DateField(verbose_name='Дата ввода остатков',
#                             null=True)
#     author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('автор'),
#                                blank=True,
#                                null=True)
#     status = models.BooleanField(default=False)
#
#     class Meta:
#         verbose_name = _('начальный остаток')
#         verbose_name_plural = _("начальные остатки")
#
#     def __str__(self):
#         return 'начальный остаток от шк №{}'.format(self.school.name)
#
#     @cached_property
#     def editions_val(self):
#         return self.editions_invoice.all()
#
#     @cached_property
#     def amount(self):
#         amount = sum(self.editions_invoice.all().values_list('amount', flat=True))
#         # for obj in self.editions_invoice.all().values('amount', 'quantity'):
#         #     amount += obj['amount'] * obj['quantity']
#         return amount
#
#     def save(self, *args, **kwargs):
#         super(InitialBalance1, self).save(*args, **kwargs)
#         content_type = ContentType.objects.get_for_model(self)
#         IncomeExpense.objects.filter(content_type=content_type, object_id=self.id).delete()
#
#         for eid in self.editions_invoice.all():
#             IncomeExpense.objects.create(
#                 ie_object=self,
#                 school_id=self.school.id,
#                 type_of_movement=1,
#                 quantity=eid.quantity,
#                 edition_id=eid.edition.id,
#                 summ=eid.amount,
#                 type=1,
#                 income=self.id,
#                 income_type=0,
#                 date=self.date
#             )
#
#     def delete(self, *args, **kwargs):
#         content_type = ContentType.objects.get_for_model(self)
#         IncomeExpense.objects.filter(content_type=content_type, object_id=self.id).delete()
#         super(InitialBalance1, self).delete(*args, **kwargs)
#
#
# class EditionInitialBalance1(models.Model):
#     invoice = models.ForeignKey(InitialBalance1, related_name='editions_invoice', on_delete=models.CASCADE,
#                                 verbose_name=_('Начальный остаток'), blank=True)
#     edition = models.ForeignKey(Edition, on_delete=models.CASCADE, blank=True, verbose_name=_('издание'))
#     quantity = models.IntegerField(verbose_name=_('количество'), default=0, blank=True)
#     amount = models.FloatField(verbose_name=_('сумма'), default=0, blank=True)
#     tags = GenericRelation(IncomeExpense, related_query_name='edition_initial_balance')
#
#     class Meta:
#         unique_together = ('invoice', 'edition')
#         verbose_name = _('Книги для начальных остатков в издательстве')
#         verbose_name_plural = _("Книги для начальных остатковх в издательстве")
#         ordering = ['id']
#
#     def __str__(self):
#         return 'Книги для начальных остатков №{}'.format(self.invoice.id)
#
#     def save(self, *args, **kwargs):
#         self.amount = round(self.amount, 2)
#         super(EditionInitialBalance, self).save(*args, **kwargs)
#

#
# class Kontingent(p_models.BaseRel):
#     school = models.ForeignKey(p_models.AlmaMater,
#                                on_delete=models.CASCADE)
#     year = models.ForeignKey(p_models.DateObjects,
#                              on_delete=models.CASCADE,
#                              verbose_name=_('Учебный год'),
#                              blank=True)
#     quantity = models.IntegerField(default=0)
#     class Meta:
#         unique_together=['school','year']
#
