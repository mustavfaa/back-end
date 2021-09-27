# -*- coding: utf-8 -*-
from PIL import Image
import uuid
import datetime
from transmeta import TransMeta
from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as trans

BLA = datetime.datetime.now()


def upload_test_avatar(instance, filename):
    return 'tmp/testavatar/' + str(datetime.date.today()) + '/' + filename


def upload_test_crop(instance, filename):
    return 'tmp/testcrop/' + str(datetime.date.today()) + '/' + filename


def upload_avatar_target(instance, filename):
    return 'usr/' + str(instance.pk) + '/' + filename


def upload_portfolio_dopfile_target(instance, filename):
    return 'usr/' \
           + str(instance.user.portfolio.id) \
           + '/dop_file/' + instance.model_name \
           + '/' + filename


def upload_portfolio_image_target(instance, filename):
    return 'usr/' \
           + str(instance.portfolio_id) \
           + '/' + instance._meta.model_name \
           + '/' + str(instance.pk) \
           + '/' + filename


def reindex_image(objekt, kwargs):
    if 'reindex' in kwargs:
        objekt.image_getted = True
        kwargs.pop('reindex')
    else:
        objekt.image_getted = False


def drop_cache():
    cache.set('left_school_menu_ru', None)
    cache.set('left_school_menu_en', None)
    cache.set('left_school_menu_kk', None)


def rename_img(self):
    try:
        old_obj = self._meta.model.objects.get(pk=self.pk)
    except:
        old_obj = self._meta.model()

    if old_obj.image.name != self.image.name:
        self.image.name = str(uuid.uuid4()) + '.jpg'


def resize_avatar(model_object):
    try:
        if model_object.image_getted:
            return

        thmb = Image.open(model_object.avatar.file.name.encode('utf8'))
        current_height = thmb.height

        if current_height > 800:
            current_height = 800

        height = current_height
        width = int(float(model_object.avatar.width) / (float(model_object.avatar.height) / float(height)))
        size = (width, height)

        if thmb.mode not in ('L', 'RGB'):
            thmb = thmb.convert('RGB')

        thmb = thmb.resize(size, Image.ANTIALIAS)
        thmb.save(model_object.avatar.file.name.encode('utf8'))

    except:
        pass


def resize_img(model_object):
    if model_object.image_getted:
        return

    thmb = Image.open(model_object.image.file.name.encode('utf8'))
    current_height = thmb.height

    if current_height > 1024:
        current_height = 1024

    height = current_height
    width = int(float(model_object.image.width) / (float(model_object.image.height) / float(height)))
    size = (width, height)

    if thmb.mode not in ('L', 'RGB'):
        thmb = thmb.convert('RGB')

    thmb = thmb.resize(size, Image.ANTIALIAS)
    thmb.save(model_object.image.file.name.encode('utf8'))


class BaseRel(models.Model):
    class Meta:
        abstract = True

    deleted = models.BooleanField(verbose_name=u'Deleted',
                                  default=False)
    date_added = models.DateTimeField(verbose_name=u'date_added',
                                      auto_now_add=True,
                                      null=True,
                                      editable=False)
    date_delete = models.DateField(verbose_name=u'date_delete',
                                   null=True,
                                   blank=True)
    comment = models.CharField(default='',
                               max_length=1000,
                               verbose_name=trans('Comment'),
                               blank=True)
    exchange = models.BooleanField(default=False)
    is_exchange = False


class CheckingFields(models.Model):
    checked = models.BooleanField(default=False)
    when_checked = models.DateTimeField(null=True,
                                        blank=True)

    class Meta:
        abstract = True


class BaseCatalog(BaseRel, metaclass=TransMeta):
    class Meta:
        abstract = True
        translate = ('name',)

    name = models.CharField(default='',
                            verbose_name='Название',
                            max_length=500,
                            blank=False,
                            null=False)
    sort = models.IntegerField(default=500, )
    uid = models.CharField(blank=True,
                           null=True,
                           max_length=36,
                           default='',
                           editable=True)

    def __str__(self):
        return self.name


class Region(BaseCatalog):
    pass


class Activate(BaseRel):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    uid = models.UUIDField(primary_key=True,
                           default=uuid.uuid4,
                           editable=False)
    new_method = models.BooleanField(default=True)
    sended = models.BooleanField(default=False)
    subject = models.CharField(default='',
                               max_length=4000)
    html_content = models.CharField(default='',
                                    max_length=1000000)
    admin_banned = models.BooleanField(default=False)


class PhoneActivate(BaseRel):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    code = models.CharField(max_length=6, )


class Degree(BaseCatalog):
    pass


class ComputerSkills(BaseCatalog):
    pass


class TypeOfAchievement(BaseCatalog):
    pass


class TypeOfAward(BaseCatalog):
    pass


class StudentTypeOfAchievement(BaseCatalog):
    pass


class EnglishLevel(BaseCatalog):
    pass


class TeacherCategory(BaseCatalog):
    pass


class Klass(BaseCatalog):

    CHOICES = (
        (1, 'Дошкольные классы'),
        (2, 'Школьные классы'),
        (3, 'Курсы в колледже'),
    )

    tech_code = models.CharField(max_length=255,
                                 default='0')
    table_sort = models.IntegerField(default=500)
    klass_type = models.IntegerField(default=2,
                                     choices=CHOICES)

    # klass_type_char = models.CharField()

    class Meta:
        ordering = ['sort']


class DateObjects(BaseCatalog):
    year_number = models.IntegerField(blank=False, unique=True)

    class Meta:
        ordering = ['sort']


class Obl(BaseCatalog):
    class Meta:
        ordering = ['sort']


class Place(BaseCatalog):
    obl = models.ForeignKey(Obl, on_delete=models.CASCADE,
                            null=True,
                            blank=True)

    class Meta:
        ordering = ['sort']


class Scale(BaseCatalog):
    class Meta:
        ordering = ['sort']


class AwardScale(BaseCatalog):
    pass


class Address(BaseCatalog):
    pass


class EducationType(BaseCatalog):
    pass


class Sex(BaseCatalog):
    pass


class SchoolTypeGroup(BaseCatalog):
    pass


class SchoolType(BaseCatalog):
    max_people = models.IntegerField(default=0,
                                     blank=False)
    edu_type = models.ForeignKey(EducationType,
                                 on_delete=models.CASCADE, )
    show_at_site = models.BooleanField(default=False)
    group = models.ForeignKey(SchoolTypeGroup,
                              null=True,
                              blank=True,
                              on_delete=models.CASCADE, )
    image = models.ImageField(default='/static/images/nophoto.png',
                              upload_to='usr/common/' + str(datetime.date.today()) + '/school_types')
    infocode = models.SmallIntegerField(default=0)

    def get_my_schools(self):
        return self.almamater_set.filter(deleted=False,
                                         author=None).order_by('sort')

    def save(self, *args, **kwargs):
        drop_cache()
        super(SchoolType, self).save(*args, **kwargs)


class CourseTheme(BaseCatalog):
    pass


class TeacherStatus(BaseCatalog):
    pass


class Speciality(BaseCatalog):
    pass


class Language(BaseCatalog):
    code = models.CharField(max_length=255,
                            default='')

    class Meta:
        ordering = ['sort']


class Quality(BaseCatalog):
    pass


class WorkType(BaseCatalog):
    pass


class VacancyStatus(BaseCatalog):
    pass


class DocType(BaseCatalog):
    pass


class SendedCerts(models.Model):
    code = models.CharField(blank=True,
                            default='',
                            null=True,
                            max_length=100)


class CompetitionVacancyStatus(BaseCatalog):
    pass


class HasTesting(BaseRel):
    pass


class StudentTableDest(BaseCatalog):
    pass


class QuerySection(BaseCatalog):
    pass

class Subject(BaseCatalog):
    is_estestv = models.BooleanField(default=False)


class Position(BaseCatalog):
    subject = models.ForeignKey(Subject,
                                null=True,
                                blank=False,
                                on_delete=models.CASCADE)
    attestation_period = models.IntegerField(default=5,
                                             verbose_name=u'Частота переаттестации')


class Country(BaseCatalog):
    kod = models.CharField(default='',
                           max_length=3, )
    abc2 = models.CharField(default='',
                            max_length=3, )


class Season(BaseCatalog):
    pass


class AttPeriod(BaseCatalog):
    season = models.ForeignKey(Season,
                               on_delete=models.CASCADE,
                               null=True)
    year = models.PositiveIntegerField(default=0)


class CriteriaZam(BaseCatalog):
    category = models.ForeignKey(TeacherStatus,
                                 on_delete=models.CASCADE, )


class ExpertType(BaseCatalog):
    pass


class CriteriaDirGroup(BaseCatalog):
    pass


class CriteriaDir(BaseCatalog):
    dest = models.ManyToManyField(SchoolTypeGroup,
                                  blank=False,
                                  )
    criteria_group = models.ForeignKey(CriteriaDirGroup, on_delete=models.CASCADE,
                                       null=True)
    category = models.ManyToManyField(TeacherStatus,
                                      blank=False, )


class Webinar(BaseRel):
    finished = models.BooleanField(default=True)
    moderator = models.CharField(max_length=255)
    webinar_id = models.CharField(max_length=3)

    for_all = models.BooleanField(default=True)
    for_zavuch = models.BooleanField(default=True)
    for_region_otv = models.BooleanField(default=True)


class PollCampaign(BaseCatalog):
    users = models.ManyToManyField(User, blank=True)


class TeacherAttestationMethod(BaseCatalog):
    header_ru = models.CharField(default='',
                                 max_length=255)
    header_kz = models.CharField(default='',
                                 max_length=255)
    in_text_ru = models.CharField(default='',
                                  max_length=255)
    in_text_kz = models.CharField(default='',
                                  max_length=255)
    in_text1_ru = models.CharField(default='',
                                   max_length=255)
    in_text1_kz = models.CharField(default='',
                                   max_length=255)


class PokazatelZam(BaseCatalog):
    value = models.FloatField(default=0)


class PokazatelDir(BaseCatalog):
    criteria = models.ForeignKey(CriteriaDir,
                                 on_delete=models.CASCADE, )
    value = models.FloatField(default=0)


class PortfolioEvaluationCriteria(BaseCatalog):
    pass


class TelegramMessage(BaseRel):
    text = models.CharField(default='',
                            max_length=1000)
    sended = models.BooleanField(default=False)


class AnaliticQuery(BaseCatalog):
    query_text = models.TextField(default='',
                                  blank=False)
    query_template = models.TextField(default='',
                                      blank=False)
    query_controller = models.TextField(default='',
                                        blank=False)
    hh = models.BooleanField(default=False)
    lang = models.CharField(default='ru',
                            max_length=255)
    section = models.ManyToManyField(QuerySection,
                                     blank=True)
    has_custom_module = models.BooleanField(default=False)
    module_name = models.CharField(default='',
                                   max_length=255)


class CourseType(BaseCatalog):
    free = models.BooleanField(default=False)
    must_vid = models.BooleanField(default=False)
    must_subject = models.BooleanField(default=False)
    must_level = models.BooleanField(default=False)
    description = models.CharField(default='',
                                   max_length=300,
                                   blank=False,
                                   verbose_name=u'Описание курса')
    is_active = models.BooleanField(default=False)
    image = models.ImageField(verbose_name=trans('Scan view'),
                              null=True,
                              upload_to='usr/common/' + str(datetime.date.today()) + '/coursetype')


class CourseVid(BaseCatalog):
    course_type = models.ForeignKey(CourseType,
                                    on_delete=models.CASCADE)
    school_type = models.ManyToManyField(SchoolType,
                                         blank=False)


class TeacherAttestationTemplate(BaseCatalog):
    text = models.TextField(default='')


class ForgetPasswordRec(BaseRel):
    user = models.ForeignKey(User,
                             verbose_name='user',
                             on_delete=models.CASCADE)
    uid = models.UUIDField(primary_key=True,
                           default=uuid.uuid4,
                           editable=False)


class TestAvatar(BaseRel):
    user = models.ForeignKey(User,
                             verbose_name='user',
                             on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True,
                               null=True,
                               upload_to=upload_test_avatar)

    def save(self, *args, **kwargs):
        try:
            this = TestAvatar.objects.get(id=self.id)
            if this.avatar != self.avatar:
                this.avatar.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        self.avatar.name = self.avatar.name + '.jpg'

        super(TestAvatar, self).save(*args, **kwargs)


class MeetingInfoRecord(BaseRel):
    server_id = models.IntegerField()
    attenders = models.IntegerField()
    live_meetings = models.IntegerField()
    attenders_ep = models.IntegerField(default=0)
    live_meetings_ep = models.IntegerField(default=0)
