from PIL import Image
import uuid, datetime
from transmeta import TransMeta
from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils.translation import ugettext as trans

BLA = datetime.datetime.now()


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

    deleted = models.BooleanField(verbose_name='Deleted',
                                  default=False)
    date_added = models.DateTimeField(verbose_name='date_added',
                                      auto_now_add=True, null=True,
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


class UserActivity(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True,
                                editable=True)


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
    class Meta:
        ordering = ['id']


class DateObjects(BaseCatalog):
    pass


class Place(BaseCatalog):
    pass


class Scale(BaseCatalog):
    pass


class Address(BaseCatalog):
    pass


class EducationType(BaseCatalog):
    pass


class Sex(BaseCatalog):
    pass


class SchoolTypeGroup(BaseCatalog):
    pass


class CourseTheme(BaseCatalog):
    pass


class TeacherStatus(BaseCatalog):
    pass


class Speciality(BaseCatalog):
    pass


class Language(BaseCatalog):
    code = models.CharField(max_length=255, default='')

    class Meta:
        ordering = ['name_ru']


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


class HasTesting(BaseRel):
    pass


class QuerySection(BaseCatalog):
    pass


class Subject(BaseCatalog):
    is_estestv = models.BooleanField(default=False)

    class Meta:
        ordering = ['name_ru']


class Position(BaseCatalog):
    subject = models.ForeignKey(Subject,
                                null=True,
                                blank=False,
                                on_delete=models.CASCADE)
    attestation_period = models.IntegerField(default=5,
                                             verbose_name=u'Частота переаттестации')

class AwardScale(BaseCatalog):
    pass

class Country(BaseCatalog):
    kod = models.CharField(default='',
                           max_length=3, )
    abc2 = models.CharField(default='',
                            max_length=3, )
