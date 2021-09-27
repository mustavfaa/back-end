from .models_core import *

from django.utils.functional import cached_property
from uuid import uuid4
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


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
                              upload_to='usr/' + str(datetime.date.today()) + '/school_types')
    infocode = models.SmallIntegerField(default=0)

    def get_my_schools(self):
        return self.almamater_set.filter(deleted=False,
                                         author=None).order_by('sort')

    def save(self, *args, **kwargs):
        drop_cache()
        super(SchoolType, self).save(*args, **kwargs)


class Portfolio(BaseCatalog):
    blocked = models.BooleanField(default=False)
    checked = models.BooleanField(default=False)
    application = models.BooleanField(default=False)
    phone_checked = models.BooleanField(default=False)
    email_checked = models.BooleanField(default=False)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)

    old_fio = models.CharField(default='',
                               max_length=255,
                               blank=True,
                               # null=True,
                               verbose_name='OldName')

    last_name = models.CharField(default='',
                                 max_length=255,
                                 verbose_name='LastName')
    first_name = models.CharField(default='',
                                  max_length=255)
    patronymic_name = models.CharField(default='',
                                       max_length=255,
                                       blank=True,
                                       null=True)
    view_in_dat_pad = models.CharField(default='',
                                       null=True,
                                       max_length=500)
    view_in_dat_pad_kaz = models.CharField(default='',
                                           null=True,
                                           max_length=500)
    iin = models.CharField(default='',
                           max_length=255)
    sex = models.ForeignKey(Sex,
                            null=True,
                            on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True,
                               null=True,
                               default='nophoto.png',
                               upload_to='usr/' + str(datetime.date.today()) + '/portfolio/')
    image_getted = models.BooleanField(default=False)
    birthday = models.DateField()
    email = models.EmailField()
    main_expert = models.BooleanField(default=False)
    computer_skills = models.ManyToManyField(ComputerSkills,
                                             blank=True, )
    phone = models.CharField(default='',
                             max_length=255,
                             null=True,
                             blank=True)
    phone_clean = models.CharField(default='',
                                   max_length=255,
                                   null=True,
                                   blank=True)
    moderator = models.ManyToManyField(Position,
                                       blank=True)
    uo_admin = models.BooleanField(default=False)
    course_admin = models.BooleanField(default=False)
    uo_operator = models.BooleanField(default=False)
    uo_babushka = models.BooleanField(default=False)
    uo_kadr = models.BooleanField(default=False)
    in_dekret = models.BooleanField(default=False)
    date_dekret = models.DateField(verbose_name=trans('date_begin'),
                                   null=True,
                                   blank=True)
    ped_stazh = models.FloatField(default=0)
    current_category = models.ForeignKey(TeacherCategory,
                                         blank=True,
                                         null=True,
                                         on_delete=models.CASCADE)
    category_year = models.DateField(blank=True,
                                     null=True)
    english_level = models.ForeignKey(EnglishLevel,
                                      blank=True,
                                      null=True,
                                      on_delete=models.CASCADE)

    access_by_group = models.ManyToManyField(SchoolTypeGroup,
                                             blank=True)
    access_by_school_type = models.ManyToManyField(SchoolType,
                                                   blank=True)
    city = models.ForeignKey(Place,
                             null=True,
                             blank=False,
                             on_delete=models.CASCADE)
    current_language = models.ForeignKey(Language,
                                         null=True,
                                         on_delete=models.CASCADE)
    has_error_firtst_name = models.BooleanField(default=False)
    has_error_last_name = models.BooleanField(default=False)
    has_error_patronymic_name = models.BooleanField(default=False)
    has_error_iin = models.BooleanField(default=False)
    has_error_avatar = models.BooleanField(default=False)
    has_error_sex = models.BooleanField(default=False)
    has_error_view_in_dat_pad = models.BooleanField(default=False)
    has_error_view_in_dat_pad_kaz = models.BooleanField(default=False)
    has_error_education = models.BooleanField(default=False)
    has_error_education_slave = models.BooleanField(default=False)
    has_error_current_language = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    public_phone = models.BooleanField(default=False,
                                       verbose_name=trans('I allow you to see the phone number'))
    public_attesta = models.BooleanField(default=False,
                                         verbose_name=trans('I allow reviewing certification'))
    public_email = models.BooleanField(default=False,
                                       verbose_name=trans('I allow to see email'))
    public_bonus = models.BooleanField(default=False,
                                       verbose_name=trans('Let me review achievements'))
    public_bonus_student = models.BooleanField(default=False,
                                               verbose_name=trans('I allow to view student achievement'))
    public_list_observ = models.BooleanField(default=False,
                                             verbose_name=trans('I allow to view lesson sheets'))
    public_upwork = models.BooleanField(default=False,
                                        verbose_name=trans('I allow to view advanced training'))
    unical = models.CharField(max_length=255,
                              default='',
                              blank=True)
    wallpaper = models.ImageField(blank=True,
                                  default='nophoto.png',
                                  upload_to='usr/' + str(datetime.date.today()) + '/portfolio/')
    competition_kandidat = models.BooleanField(default=False)
    director = models.BooleanField(default=False)
    aspirant = models.BooleanField(default=False)
    voluntary_aspirant = models.BooleanField(default=False)

    dont_have_attestation = models.BooleanField(default=False)
    dont_have_upwork = models.BooleanField(default=False)
    dont_have_bonus = models.BooleanField(default=False)
    dont_have_bonus_student = models.BooleanField(default=False)
    dont_have_list_of_view = models.BooleanField(default=False)
    dont_have_studen_table = models.BooleanField(default=False)
    date_dont_have_attestation = models.DateTimeField(null=True, blank=True)
    date_dont_have_upwork = models.DateTimeField(null=True, blank=True)
    date_dont_have_bonus = models.DateTimeField(null=True, blank=True)
    date_dont_have_bonus_student = models.DateTimeField(null=True, blank=True)
    date_dont_have_list_of_view = models.DateTimeField(null=True, blank=True)
    date_dont_have_studen_table = models.DateTimeField(null=True, blank=True)

    attestation_responsible = models.BooleanField(default=False,
                                                  verbose_name=u'Ответственный за аттестацию')

    reindexed = models.BooleanField(default=False)
    reindexed_wtl = models.BooleanField(default=False)

    def get_current(self):
        qs = PortfolioWorkTimeLine.objects.filter(portfolio=self,
                                                  checked=True,
                                                  uvolen=False,
                                                  deleted=False,
                                                  current=True).order_by('-date_begin')
        return qs

    @property
    def get_avatar(self):
        return 'https://eportfolio.kz/static/images{}'.format(str(self.avatar))

    def save(self, *args, **kwargs):
        reindex_image(self, kwargs)
        super(Portfolio, self).save(*args, **kwargs)
        # resize_avatar(self)
        curr = self.get_current()
        for item in curr:
            cache.set('school_teachers' + str(item.school.id), None)
            cache.set('school_teachers1' + str(item.school.id), None)

    def delete(self, using=None, keep_parents=False):
        super(Portfolio, self).delete()


class AlmaMater(BaseCatalog):
    place = models.ForeignKey(Place,
                              null=True,
                              on_delete=models.CASCADE)
    image = models.ImageField(default='nophoto.png',
                              upload_to='usr/' + str(datetime.date.today()) + '/almamater')
    nmr_user = models.ForeignKey(Portfolio,
                                 related_name="nmr_user",
                                 blank=True,
                                 null=True,
                                 on_delete=models.CASCADE)
    deputy_for_education = models.ForeignKey(Portfolio,
                                             related_name="deputy_for_education",
                                             blank=True,
                                             null=True,
                                             on_delete=models.CASCADE)
    director_user = models.ForeignKey(Portfolio,
                                      related_name="director_user",
                                      blank=True,
                                      null=True,
                                      on_delete=models.CASCADE)
    librarian_user = models.ForeignKey(Portfolio,
                                       related_name="librarian_user",
                                       blank=True,
                                       null=True,
                                       on_delete=models.CASCADE)
    librarian_zam = models.ForeignKey(Portfolio,
                                      related_name="librarian_zam",
                                      blank=True,
                                      null=True,
                                      on_delete=models.CASCADE)
    kadr_user = models.ForeignKey(Portfolio,
                                  related_name="kadr_user",
                                  blank=True,
                                  null=True,
                                  on_delete=models.CASCADE)

    short_code = models.CharField(default='',
                                  max_length=255,
                                  blank=True)
    school_type = models.ForeignKey(SchoolType,
                                    null=True,
                                    on_delete=models.CASCADE)
    address = models.CharField(default='',
                               max_length=255,
                               null=True, )
    user = models.ForeignKey(User,
                             related_name='user',
                             editable=False,
                             null=True,
                             blank=True,
                             on_delete=models.CASCADE)
    user_string = models.CharField(default='',
                                   max_length=255,
                                   blank=True)
    director = models.ForeignKey(User,
                                 editable=False,
                                 null=True,
                                 blank=True,
                                 on_delete=models.CASCADE)
    author = models.ForeignKey(Portfolio,
                               null=True,
                               editable=False,
                               blank=True,
                               on_delete=models.CASCADE)
    phone_director = models.CharField(default='',
                                      max_length=255,
                                      null=True,
                                      blank=True)
    phone_user = models.CharField(default='',
                                  max_length=255,
                                  null=True,
                                  blank=True)
    nash = models.BooleanField(default=False)
    reindexed = models.BooleanField(default=False)
    jew = models.BooleanField(default=False)

    phone_accounter = models.CharField(default='',
                                       max_length=255,
                                       null=True,
                                       blank=True)
    school_email = models.EmailField(default="",
                                     verbose_name=trans('email'),
                                     blank=True,
                                     null=True)

    phone_hr = models.CharField(default='',
                                max_length=255,
                                null=True,
                                blank=True)
    accounter_name = models.CharField(default='',
                                      max_length=255,
                                      null=True,
                                      blank=True)

    region = models.ForeignKey(Region, null=True, on_delete=models.CASCADE)

    speed_edit = False

    @property
    def zouch(self):
        return self.user.portfolio_set.first()

    @cached_property
    def all_vacans(self):
        return self.vacancies.all()

    @cached_property
    def all_news(self):
        return self.news_set.all()

    def save(self, *args, **kwargs):
        if not self.speed_edit:
            try:
                self.user = User.objects.get(username=self.user_string)
            except:
                self.user = User.objects.get(pk=7)
            if self.author != None:
                self.user = self.author.user
        drop_cache()
        if self.author == None:
            self.nash = True
        super(AlmaMater, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        super(AlmaMater, self).delete()


class AttestationResponsible(BaseRel):
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)
    attestation_responsible_region = models.ManyToManyField(Region, blank=True)


class RegistrationProcess(BaseRel):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    email_sended = models.BooleanField(default=False)
    email_checked = models.BooleanField(default=False)
    last_try = models.DateTimeField(null=True,
                                    blank=True)


class CheckingFields(models.Model):
    checked = models.BooleanField(default=False)
    when_checked = models.DateTimeField(null=True,
                                        blank=True)

    class Meta:
        abstract = True


class PortfolioEducation(BaseRel, CheckingFields):
    changer = models.ForeignKey(User,
                                null=True,
                                blank=True,
                                on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE
                                  )
    date_begin = models.DateField(blank=False,
                                  verbose_name=trans('Education date begin'))
    date_end = models.DateField(blank=False,
                                verbose_name=trans('Education date end'))
    image = models.ImageField(verbose_name=trans('i18 the diploma'),
                              upload_to='usr/' + str(datetime.date.today()) + '/education')
    image_getted = models.BooleanField(default=False)
    alma_mater_ref = models.ForeignKey(AlmaMater,
                                       null=True,
                                       blank=True,
                                       on_delete=models.CASCADE)
    alma_mater = models.CharField(default='',
                                  blank=False,
                                  verbose_name=trans('i18 educational institution'),
                                  max_length=1000)
    speciality = models.ManyToManyField(Speciality,
                                        blank=False,
                                        verbose_name=trans('select one or many'))
    quality = models.ManyToManyField(Quality,
                                     blank=False,
                                     verbose_name=trans('i18 quality'))
    language = models.ManyToManyField(Language,
                                      blank=False,
                                      verbose_name=trans('education language'))
    degree = models.ForeignKey(Degree,
                               null=True,
                               blank=False,
                               verbose_name=trans('i18 scientific degree'),
                               on_delete=models.CASCADE)
    education_type = models.ForeignKey(EducationType,
                                       null=True,
                                       blank=False,
                                       verbose_name=trans('Education type'),
                                       on_delete=models.CASCADE)
    quality_on_diplom = models.CharField(default='',
                                         blank=False,
                                         verbose_name=trans('Quality on diploma'),
                                         max_length=1000)
    speciality_handmade = models.CharField(default='',
                                           blank=False,
                                           verbose_name=trans('i18 specialty'),
                                           max_length=1000)
    who_checked = models.ForeignKey(Portfolio,
                                    null=True, blank=True,
                                    on_delete=models.CASCADE,
                                    related_name='whu_checked_education')

    def __unicode__(self):
        return self.alma_mater + ' -- ' + self.quality_on_diplom

    def save(self, *args, **kwargs):
        rename_img(self)
        reindex_image(self, kwargs)
        super(PortfolioEducation, self).save(*args, **kwargs)
        resize_img(self)
        p = self.portfolio
        p.reindexed = False
        p.save()

        wtl = PortfolioWorkTimeLine.objects.filter(portfolio=self.portfolio,
                                                   education=None)
        for item in wtl:
            item.education = self
            item.save()

    def delete(self, using=None, keep_parents=False):
        super(PortfolioEducation, self).delete()


class TelegramMessage(BaseRel):
    text = models.CharField(default='',
                            max_length=1000)
    sended = models.BooleanField(default=False)


class PortfolioWorkTimeLine(BaseRel):
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)
    date_begin = models.DateField(verbose_name=trans('Employment date'),
                                  blank=False)
    date_end = models.DateField(blank=True,
                                verbose_name=trans('Date of dismissal'),
                                null=True)
    changer = models.ForeignKey(User,
                                null=True,
                                blank=True,
                                on_delete=models.CASCADE)
    school = models.ForeignKey(AlmaMater,
                               blank=True,
                               null=True,
                               verbose_name=trans('Work place'),
                               on_delete=models.CASCADE)
    positions = models.ForeignKey(Position,
                                  verbose_name=trans('positions'),
                                  null=True,
                                  blank=True,
                                  on_delete=models.CASCADE)
    positions_string = models.CharField(max_length=255,
                                        default='',
                                        verbose_name=trans('positions'),
                                        blank=True)
    current = models.BooleanField(default=False)
    checked = models.BooleanField(default=False)
    not_checked = models.BooleanField(default=False)
    uvolen = models.BooleanField(default=False)
    language = models.ManyToManyField(Language,
                                      verbose_name=trans('language'), )
    education = models.ForeignKey(PortfolioEducation,
                                  null=True,
                                  blank=False,
                                  verbose_name=trans('Education to work'),
                                  on_delete=models.CASCADE)
    slave = models.ForeignKey(WorkType,
                              null=True,
                              blank=False,
                              verbose_name=trans('Type of position'),
                              on_delete=models.CASCADE)
    director = models.BooleanField(default=False)
    admin_editted = models.BooleanField(default=False)
    day_delta = models.IntegerField(default=0,
                                    null=True,
                                    blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if self.date_end is None:
            self.current = True
        else:
            self.current = False
        super(PortfolioWorkTimeLine, self).save()
        p = self.portfolio
        p.reindexed = False

        p.reindexed_wtl = False
        p.save()
        cache.set('school_teachers' + str(self.school.id), None)
        cache.set('school_teachers1' + str(self.school.id), None)


class PortfolioDekret(BaseRel):
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)
    date_begin = models.DateField(verbose_name=trans('date_begin'),
                                  blank=False)
    date_end = models.DateField(blank=True,
                                verbose_name=trans('date_end'),
                                null=True)
    changer = models.ForeignKey(User,
                                null=True,
                                blank=True,
                                on_delete=models.CASCADE)


class CurrentWorkTimeLine(BaseRel):
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)
    wtl = models.ForeignKey(PortfolioWorkTimeLine,
                            on_delete=models.CASCADE)


class PortfolioWorkTimeLineUser(BaseRel):
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)
    date_begin = models.DateField(verbose_name=trans('date_begin'))
    date_end = models.DateField(blank=True,
                                verbose_name=trans('date_end'),
                                null=True)
    school = models.ForeignKey(AlmaMater,
                               null=True,
                               verbose_name=trans('school'),
                               on_delete=models.CASCADE)
    positions = models.ForeignKey(Position,
                                  verbose_name=trans('positions'),
                                  null=True,
                                  on_delete=models.CASCADE)
    current = models.BooleanField(default=False)
    language = models.ManyToManyField(Language,
                                      verbose_name=trans('language'))
    education = models.ForeignKey(PortfolioEducation,
                                  null=True,
                                  verbose_name=trans('i18 education'),
                                  on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(PortfolioWorkTimeLine, self).save()


class CourseType(BaseCatalog):
    free = models.BooleanField(default=False)
    must_vid = models.BooleanField(default=False)
    must_subject = models.BooleanField(default=False)
    must_level = models.BooleanField(default=False)
    description = models.CharField(default='',
                                   max_length=300,
                                   blank=False,
                                   verbose_name='Описание курса')
    is_active = models.BooleanField(default=False)
    image = models.ImageField(verbose_name=trans('Scan view'),
                              null=True,
                              upload_to='usr/' + str(datetime.date.today()) + '/coursetype')


class CourseVid(BaseCatalog):
    course_type = models.ForeignKey(CourseType,
                                    on_delete=models.CASCADE)
    school_type = models.ManyToManyField(SchoolType,
                                         blank=False)


class Upwork(BaseRel, CheckingFields):
    bl = True
    changer = models.ForeignKey(User,
                                null=True,
                                blank=True,
                                on_delete=models.CASCADE)
    course_type = models.ForeignKey(CourseType,
                                    verbose_name=trans('Course type'),
                                    null=True,
                                    blank=False,
                                    on_delete=models.CASCADE)
    scale = models.ForeignKey(Scale,
                              null=True,
                              blank=False,
                              verbose_name=trans('i18 Level'),
                              on_delete=models.CASCADE)
    course_vid = models.ForeignKey(CourseVid,
                                   verbose_name=trans(u'Уровень образования'),
                                   null=True,
                                   blank=bl,
                                   on_delete=models.CASCADE)
    course_subject = models.ForeignKey(Subject,
                                       verbose_name=trans('Course subject'),
                                       null=True,
                                       blank=bl,
                                       on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)
    positions = models.ForeignKey(Position,
                                  verbose_name=trans('i18 positions'),
                                  blank=False,
                                  null=True,
                                  on_delete=models.CASCADE)
    date_begin = models.DateField(verbose_name=trans('date_begin'))
    course_theme_str = models.CharField(default='',
                                        null=True,
                                        max_length=500,
                                        blank=False,
                                        verbose_name=trans('Course theme'))
    country = models.ForeignKey(Country,
                                null=True,
                                blank=False,
                                verbose_name=trans('Country'),
                                on_delete=models.CASCADE)
    city = models.CharField(default='',
                            null=True,
                            max_length=500,
                            blank=bl,
                            verbose_name=trans('City'))
    language = models.ForeignKey(Language,
                                 blank=False,
                                 null=True,
                                 verbose_name=trans('education language'),
                                 on_delete=models.CASCADE)
    course_theme = models.ForeignKey(CourseTheme,
                                     null=True,
                                     blank=True,
                                     verbose_name=trans('Course theme'),
                                     on_delete=models.CASCADE)
    date_end = models.DateField(verbose_name=trans('date_end'))
    school = models.ForeignKey(AlmaMater,
                               null=True,
                               blank=True,
                               verbose_name=trans('Organization of upwork courses'),
                               on_delete=models.CASCADE)
    englishlevel = models.ForeignKey(EnglishLevel, blank=True,
                                     verbose_name=trans('i18 englishlevel'),
                                     null=True,
                                     on_delete=models.CASCADE)

    image = models.ImageField(verbose_name=trans('i18 the diploma'),
                              upload_to='usr/' + str(datetime.date.today()) + '/upwork')
    hours = models.IntegerField(verbose_name=trans('Hours'),
                                default=0,
                                blank=True)
    image_getted = models.BooleanField(default=False)
    who_checked = models.ForeignKey(Portfolio,
                                    null=True, blank=True,
                                    on_delete=models.CASCADE,
                                    related_name='whu_checked_upwork')

    def save(self, *args, **kwargs):

        if not self.course_type is None:
            if not self.course_type.must_level:
                self.englishlevel = None
            if not self.course_type.must_vid:
                self.course_vid = None
            if not self.course_type.must_subject:
                self.course_subject = None
        if not self.scale is None and self.scale.id != 2:
            self.country = Country.objects.get(kod='398')

        rename_img(self)
        reindex_image(self, kwargs)
        super(Upwork, self).save(*args, **kwargs)
        resize_img(self)

    def delete(self, using=None, keep_parents=False):
        super(Upwork, self).delete()


class Attestation(BaseRel, CheckingFields):
    changer = models.ForeignKey(User,
                                null=True,
                                blank=True,
                                on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE
                                  )
    category = models.ForeignKey(TeacherCategory,
                                 verbose_name=trans('i18 category'),
                                 on_delete=models.CASCADE)
    date = models.DateField(verbose_name=trans('Attestation date'))

    image = models.ImageField(verbose_name=trans('i18 the diploma'),
                              upload_to='usr/' + str(datetime.date.today()) + '/attestation')

    image_getted = models.BooleanField(default=False)
    school = models.ForeignKey(AlmaMater,
                               null=True,
                               blank=True,
                               verbose_name=trans('i18 advanced studies'),
                               on_delete=models.CASCADE)

    positions = models.ManyToManyField(Position,
                                       related_name='pos',
                                       verbose_name=trans('positions'))

    certificate = models.CharField(default='',
                                   max_length=255,
                                   verbose_name=trans('i18 certificate'))
    who_checked = models.ForeignKey(Portfolio,
                                    null=True, blank=True,
                                    on_delete=models.CASCADE,
                                    related_name='whu_checked_attestation')

    def save(self, *args, **kwargs):
        rename_img(self)
        reindex_image(self, kwargs)
        super(Attestation, self).save(*args, **kwargs)
        resize_img(self)
        p = self.portfolio
        p.reindexed = False
        p.save()

    def delete(self, using=None, keep_parents=False):
        super(Attestation, self).delete()


class PortfolioBonus(BaseRel, CheckingFields):
    changer = models.ForeignKey(User,
                                null=True,
                                blank=True,
                                on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)
    date = models.DateField(
        verbose_name=trans('Date_bonus')
    )
    image = models.ImageField(verbose_name=trans('i18 the diploma'),
                              upload_to='usr/' + str(datetime.date.today()) + '/bonus')
    image_getted = models.BooleanField(default=False)
    type_of_achievement = models.ForeignKey(TypeOfAchievement,
                                            verbose_name=trans('i18 type_of_achievement'),
                                            on_delete=models.CASCADE)
    scale = models.ForeignKey(Scale,
                              verbose_name=trans('i18 Level'),
                              on_delete=models.CASCADE)
    who_checked = models.ForeignKey(Portfolio,
                                    null=True, blank=True,
                                    on_delete=models.CASCADE,
                                    related_name='whu_checked_bonus')

    def save(self, *args, **kwargs):
        rename_img(self)
        reindex_image(self, kwargs)
        super(PortfolioBonus, self).save(*args, **kwargs)
        resize_img(self)

    def delete(self, using=None, keep_parents=False):
        super(PortfolioBonus, self).delete()



class PortfolioAward(BaseRel):
    changer = models.ForeignKey(User,
                                null=True,
                                blank=True,
                                on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)
    date = models.DateField(
        verbose_name=trans('Date_bonus')
    )
    image = models.ImageField(verbose_name=trans('i18 the diploma'),
                              upload_to='usr/' + str(datetime.date.today()) + '/bonus')
    image_getted = models.BooleanField(default=False)

    type_of_award = models.ForeignKey(TypeOfAward,
                                      verbose_name=trans('i18 type_of_achievement'),
                                      on_delete=models.CASCADE)
    scale = models.ForeignKey(AwardScale,
                              verbose_name=trans('i18 Level'),
                              on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        rename_img(self)
        reindex_image(self, kwargs)
        super(PortfolioAward, self).save(*args, **kwargs)
        resize_img(self)

    def delete(self, using=None, keep_parents=False):
        super(PortfolioAward, self).delete()


class PortfolioListOfView(BaseRel, CheckingFields):
    changer = models.ForeignKey(User,
                                null=True,
                                blank=True,
                                on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)

    school = models.ForeignKey(AlmaMater,
                               null=True,
                               verbose_name=trans('School of lesson'),
                               on_delete=models.CASCADE)
    date = models.DateField(verbose_name=trans('Date'))
    image = models.ImageField(verbose_name=trans('Scan view'),
                              upload_to='usr/' + str(datetime.date.today()) + '/listobservation')
    image_getted = models.BooleanField(default=False)
    subject = models.ForeignKey(Subject,
                                verbose_name=trans('i18 subject'),
                                null=True,
                                on_delete=models.CASCADE)
    who_checked = models.ForeignKey(Portfolio,
                                    null=True, blank=True,
                                    on_delete=models.CASCADE,
                                    related_name='whu_checked_list_of_view')

    def save(self, *args, **kwargs):
        rename_img(self)
        reindex_image(self, kwargs)
        super(PortfolioListOfView, self).save(*args, **kwargs)
        resize_img(self)

    def delete(self, using=None, keep_parents=False):
        super(PortfolioListOfView, self).delete()


class PortfolioBonusStudent(BaseRel, CheckingFields):
    changer = models.ForeignKey(User,
                                null=True,
                                blank=True,
                                on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)
    date = models.DateField(verbose_name=trans('Date_bonus'))
    image = models.ImageField(verbose_name=trans('i18 the diploma'),
                              upload_to='usr/' + str(datetime.date.today()) + '/bonus', )
    scale = models.ForeignKey(Scale,
                              verbose_name=trans('i18 Level'),
                              on_delete=models.CASCADE)
    student_type_achievement = models.ForeignKey(StudentTypeOfAchievement,
                                                 verbose_name=trans('i18 type_of_achievement'),
                                                 blank=False,
                                                 null=True,
                                                 on_delete=models.CASCADE)

    image_getted = models.BooleanField(default=False)
    who_checked = models.ForeignKey(Portfolio,
                                    null=True, blank=True,
                                    on_delete=models.CASCADE,
                                    related_name='whu_checked_bonus_student')

    def save(self, *args, **kwargs):
        rename_img(self)
        reindex_image(self, kwargs)
        super(PortfolioBonusStudent, self).save(*args, **kwargs)
        resize_img(self)

    def delete(self, using=None, keep_parents=False):
        super(PortfolioBonusStudent, self).delete()

class PortfolioEvaluationCriteria(BaseCatalog):
    pass

class TeacherAttestation(BaseCatalog):
    svid_temp = models.TextField(default='',
                                 blank=False)
    rebuilded_testers = models.BooleanField(default=False)
    svid_date = models.DateField(null=True,
                                 verbose_name=trans('Svid publication date'))
    svid_date_by_kaz = models.CharField(default='',
                                        blank=True,
                                        null=True,
                                        max_length=50,
                                        verbose_name=trans('Svid publication date by kaz'))
    prikaz_number = models.CharField(default='',
                                     blank=False,
                                     max_length=50,
                                     verbose_name=trans('Prikaz Num'))

    attestation_center = models.ForeignKey(AlmaMater,
                                           null=True,
                                           blank=False,
                                           on_delete=models.CASCADE,
                                           verbose_name=u'Центр аттестации')

    finished = models.BooleanField(default=False)
    ready_to_cert = models.BooleanField(default=False)
    uo_blocked = models.BooleanField(default=False)

    main_text_kaz = models.TextField(default='',
                                     verbose_name=trans('Main text kaz'))
    main_text_rus = models.TextField(default='',
                                     verbose_name=trans('Main text rus'))
    predsedatel = models.CharField(default='',
                                   verbose_name=trans('Predsedatel'),
                                   max_length=500,
                                   blank=False,
                                   null=True)
    sekretar = models.CharField(default='',
                                verbose_name=trans('Sekretar'),
                                max_length=500,
                                blank=False,
                                null=True)
    school_type = models.ManyToManyField(SchoolType,
                                         blank=False)
    dead_line = models.DateField(null=True)
    region = models.ManyToManyField(Region,
                                    blank=True)
    author = models.ForeignKey(Portfolio,
                               on_delete=models.CASCADE,
                               null=True,
                               related_name='teacher_attestation_author')
    app_start_date = models.DateField(null=True,
                                          verbose_name= u'Дата начала подачи заявлений',
                                        blank=True)
    evaluation_criteria = models.ManyToManyField(PortfolioEvaluationCriteria,
                                            verbose_name=u'Критерии оценки портфолио',)
    operators = models.ManyToManyField(Portfolio,
                                       related_name='teacher_attestation_operators')




class AttestationProtocol(BaseRel):
    attestation = models.ManyToManyField(TeacherAttestation,
                                         verbose_name=trans('Attestation'))
    file = models.FileField(null=True,
                            blank=True,
                            upload_to='att_prot/')


class TeacherScale(BaseCatalog):
    attestation = models.ForeignKey(TeacherAttestation,
                                    null=True,
                                    on_delete=models.CASCADE)
    val = models.IntegerField(default=0)
    min_value = models.IntegerField(default=1)


class Note(BaseCatalog):
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(default="")
    portfolio = models.ForeignKey(Portfolio,
                                  null=True,
                                  on_delete=models.CASCADE)
    ocenka = models.ForeignKey(TeacherScale,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    tester = models.ForeignKey(User,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    ocenka_type = models.IntegerField(null=True,
                                      blank=True)


class News(BaseCatalog):
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(default="")
    text_short = models.TextField(default="")
    school = models.ForeignKey(AlmaMater,
                               null=True,
                               on_delete=models.CASCADE)
    user = models.ForeignKey(Portfolio,
                             null=True,
                             on_delete=models.CASCADE)
    meta_keywords = models.CharField(blank=True,
                                     default='',
                                     max_length=200)
    meta_description = models.TextField(blank=True,
                                        max_length=250)


class SchoolBonus(BaseRel):
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)
    date = models.DateField()
    image_getted = models.BooleanField(default=False)
    image = models.ImageField(default='/static/images/nophoto.png',
                              upload_to='usr/' + str(datetime.date.today()) + '/bonus')

    school = models.ForeignKey(AlmaMater,
                               null=True,
                               on_delete=models.CASCADE)

    achievements = models.TextField(default="")

    def save(self, *args, **kwargs):
        rename_img(self)
        reindex_image(self, kwargs)
        super(SchoolBonus, self).save(*args, **kwargs)
        resize_img(self)


class ForgetPasswordRec(BaseRel):
    user = models.ForeignKey(User,
                             verbose_name='user',
                             on_delete=models.CASCADE)
    uid = models.UUIDField(primary_key=True,
                           default=uuid.uuid4,
                           editable=False)


class AdsAttestation(BaseRel):
    date_begin = models.DateField(null=True, )
    date_end = models.DateField(null=True, )

    institute = models.ForeignKey(AlmaMater,
                                  null=True,
                                  on_delete=models.CASCADE)
    header = models.CharField(max_length=255,
                              blank=True)

    text = models.TextField(default="")
    user = models.ForeignKey(Portfolio,
                             null=True,
                             on_delete=models.CASCADE)


class StudenTtable(BaseRel, CheckingFields):
    language_objects = models.ForeignKey(Language,
                                         null=True,
                                         on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                null=True,
                                on_delete=models.CASCADE)
    date_objects = models.ForeignKey(DateObjects,
                                     null=True,
                                     on_delete=models.CASCADE)
    klass = models.ForeignKey(Klass,
                              null=True,
                              on_delete=models.CASCADE)
    persent = models.TextField(default="")
    persent_float = models.FloatField(default=0)
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)
    ocenka = models.ForeignKey(TeacherScale,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    tester = models.ForeignKey(User,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    who_checked = models.ForeignKey(Portfolio,
                                    null=True, blank=True,
                                    on_delete=models.CASCADE,
                                    related_name='whu_checked_ttable')


class ListObservations(BaseRel):
    changer = models.ForeignKey(User,
                                null=True,
                                blank=True,
                                on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)
    date = models.DateField()
    image_getted = models.BooleanField(default=False)
    image = models.ImageField(default='/static/images/nophoto.png',
                              upload_to='usr/' + str(datetime.date.today()) + '/listobservation')
    school = models.ForeignKey(AlmaMater,
                               null=True,
                               on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                null=True,
                                on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        rename_img(self)
        reindex_image(self, kwargs)
        super(ListObservations, self).save(*args, **kwargs)
        resize_img(self)


class ApplicationAds(BaseRel):
    portfolio = models.ForeignKey(Portfolio,
                                  null=True,
                                  on_delete=models.CASCADE)
    ads_attestation = models.ForeignKey(AdsAttestation,
                                        null=True,
                                        on_delete=models.CASCADE)
    checked = models.BooleanField(default=False)
    ignored = models.BooleanField(default=False)


class TestAvatar(BaseRel):
    user = models.ForeignKey(User,
                             verbose_name='user',
                             on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True,
                               null=True,
                               default='/static/images/nophoto.png',
                               upload_to='usr/' + str(datetime.date.today()) + '/testavatar')

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = TestAvatar.objects.get(id=self.id)
            if this.avatar != self.avatar:
                this.avatar.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        self.avatar.name = self.avatar.name + '.jpg'
        super(TestAvatar, self).save(*args, **kwargs)
        # resize_avatar(self)
        # resize_avatar(self)

    # def delete(self, using=None, keep_parents=False):
    #
    #     if using == True:
    #         pass
    #     else:
    #         self.avatar.delete(save=False)
    #
    #     super(TestAvatar, self).delete()


class TestSchool(BaseRel):
    user = models.ForeignKey(User,
                             verbose_name='user',
                             on_delete=models.CASCADE)
    image = models.ImageField(default='/static/images/nophoto.png',
                              upload_to='usr/' + str(datetime.date.today()) + '/testalmamater')

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = TestSchool.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        self.image.name = self.image.name + '.jpg'
        super(TestSchool, self).save(*args, **kwargs)
        # resize_img(self)

    def delete(self, using=None, keep_parents=False):

        if using == True:
            pass
        else:
            self.image.delete(save=False)

        super(TestSchool, self).delete()


class BlockHistory(BaseRel):
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)
    who = models.ForeignKey(User,
                            on_delete=models.CASCADE)
    status = models.BooleanField(default=True)


class ChangeResponsibleHistory(BaseRel):
    school = models.ForeignKey(AlmaMater,
                               on_delete=models.CASCADE,
                               null=True)
    before = models.EmailField(default="", )
    after = models.EmailField(default="", )
    who = models.ForeignKey(User,
                            on_delete=models.CASCADE,
                            null=True)


class TeacherAttestationUser(BaseRel):
    attestation = models.ForeignKey(TeacherAttestation,
                                    on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    portfolio_expert = models.ForeignKey(Portfolio,
                                         null=True,
                                         blank=True,
                                         on_delete=models.CASCADE)
    position = models.ManyToManyField(Position,
                                      blank=True, )
    category = models.ManyToManyField(TeacherCategory,
                                      blank=True, )

    date_end = models.DateField(verbose_name=trans('date_end'),
                                null=True,
                                blank=False)

    def __unicode__(self):
        return self.user.username


class Verdikt(BaseCatalog):
    uo_ru = models.CharField(blank=False,
                             default='',
                             max_length=255)
    uo_kk = models.CharField(blank=False,
                             default='',
                             max_length=255)

    def __unicode__(self):
        return self.name




class PrivateDocument(BaseRel):
    portfolio = models.ForeignKey(Portfolio,
                                  null=True,
                                  on_delete=models.CASCADE)
    image = models.ImageField(upload_to='usr/' + str(datetime.date.today()) + '/private_docs/')
    doc_type = models.ForeignKey(DocType,
                                 verbose_name='Тип документа',
                                 on_delete=models.CASCADE)


class PortfolioStatement(BaseRel):
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)
    fio = models.CharField(default='',
                           verbose_name=trans('Full name'),
                           max_length=1000,
                           blank=False,
                           null=True)
    bonuses = models.ManyToManyField(PortfolioBonus,
                                     blank=True,
                                     verbose_name=trans('i18 student awards'))
    bonuses_for_degree = models.ManyToManyField(PortfolioBonus,
                                                blank=True,
                                                related_name='bonuses_for_degree',
                                                verbose_name=trans('i18 student awards'))
    bonus_students = models.ManyToManyField(PortfolioBonusStudent,
                                            blank=True,
                                            verbose_name=trans('i18 student student'))
    current_status = models.ForeignKey(TeacherCategory,
                                       null=True,
                                       verbose_name='Текущая категория',
                                       blank=True,
                                       on_delete=models.CASCADE)
    method = models.ForeignKey(TeacherAttestationMethod,
                               null=True,
                               verbose_name='Подтверждение/присвоение',
                               blank=False,
                               on_delete=models.CASCADE)
    status = models.ForeignKey(TeacherStatus,
                               null=True,
                               verbose_name='Претендуемая категория',
                               blank=False,
                               on_delete=models.CASCADE)

    attestation = models.ForeignKey(TeacherAttestation,
                                    null=False,
                                    verbose_name=trans('Attestation'),
                                    blank=False,
                                    on_delete=models.CASCADE)

    positions_old = models.ForeignKey(Position,
                                      blank=True,
                                      verbose_name=trans('positions'),
                                      null=True,
                                      on_delete=models.CASCADE)
    positions = models.ManyToManyField(Position,
                                       blank=False,
                                       related_name='positions',
                                       verbose_name=trans('positions'),
                                       )
    date_end = models.DateField(verbose_name='Дата подачи заявления в УО',
                                null=True,
                                blank=False)
    school = models.ForeignKey(AlmaMater,
                               null=False,
                               blank=False,
                               verbose_name=trans('Work place'),
                               on_delete=models.CASCADE)
    view_in_dat_pad = models.CharField(default='',
                                       null=True,
                                       blank=False,
                                       verbose_name=trans('View in dat pad'),
                                       max_length=500)
    view_in_dat_pad_kaz = models.CharField(default='',
                                           verbose_name=trans('View in dat pad kaz'),
                                           null=True,
                                           blank=False,
                                           max_length=500)
    checked = models.BooleanField(default=False)
    not_checked = models.BooleanField(default=False)
    in_protocol = models.BooleanField(default=False)
    documents = models.ManyToManyField(PrivateDocument,
                                       blank=True)
    experience_spec = models.FloatField(verbose_name=trans('experience_spec'),
                                        default=0)
    experience_ped = models.FloatField(verbose_name=trans('experience_ped'),
                                       default=0)
    experience_in_org = models.FloatField(verbose_name=trans('experience_in_org'),
                                          default=0)


class Kandidat(BaseRel):
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)
    status = models.ForeignKey(TeacherStatus,
                               on_delete=models.CASCADE)
    attestation = models.ForeignKey(TeacherAttestation,
                                    on_delete=models.CASCADE)
    tester = models.ForeignKey(User,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    started = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    date_begin = models.DateTimeField(null=True,
                                      blank=True)
    date_end = models.DateTimeField(null=True,
                                    blank=True)
    verdikt_cmo = models.ForeignKey(Verdikt,
                                    related_name='verdikt_cmo',
                                    null=True,
                                    blank=True,
                                    on_delete=models.CASCADE)
    verdikt = models.ForeignKey(Verdikt,
                                null=True,
                                related_name='verdict_uo',
                                blank=True,
                                on_delete=models.CASCADE)
    svid_num = models.CharField(default='',
                                null=True,
                                db_index=True,
                                blank=True,
                                max_length=6)
    svid_date = models.DateField(null=True,
                                 blank=True)
    position = models.ManyToManyField(Position, )

    school = models.ForeignKey(AlmaMater,
                               null=True,
                               on_delete=models.CASCADE)
    method = models.ForeignKey(TeacherAttestationMethod,
                               null=True,
                               on_delete=models.CASCADE)
    statement = models.ForeignKey(PortfolioStatement,
                                  null=True,
                                  on_delete=models.CASCADE)
    correct_svid = models.BooleanField(default=False)
    uncorrect_svid = models.BooleanField(default=False)
    view_in_dat_pad = models.CharField(default='',
                                       null=True,
                                       blank=False,
                                       verbose_name=trans('View in dat pad'),
                                       max_length=500)
    view_in_dat_pad_kaz = models.CharField(default='',
                                           verbose_name=trans('View in dat pad kaz'),
                                           null=True,
                                           blank=False,
                                           max_length=500)

    def __unicode__(self):
        return self.portfolio.name


class KandidatVerdiktHistory(BaseRel):
    kandidat = models.ForeignKey(Kandidat,
                                 on_delete=models.CASCADE)
    verdikt = models.ForeignKey(Verdikt,
                                null=True,
                                on_delete=models.CASCADE)
    who = models.ForeignKey(User,
                            on_delete=models.CASCADE)


class KandidatStatusHistory(BaseRel):
    kandidat = models.ForeignKey(Kandidat,
                                 on_delete=models.CASCADE)
    who = models.ForeignKey(User,
                            on_delete=models.CASCADE)
    status = models.ForeignKey(TeacherStatus,
                               on_delete=models.CASCADE)


class TeacherScaleSettings(BaseRel):
    status = models.ForeignKey(TeacherStatus,
                               on_delete=models.CASCADE)
    scale = models.ForeignKey(TeacherScale,
                              on_delete=models.CASCADE)
    destination = models.CharField(choices=(('PortfolioListOfView', 'PortfolioListOfView'),
                                            ('PortfolioBonus', 'PortfolioBonus'),
                                            ('PortfolioBonusStudent', 'PortfolioBonusStudent'),
                                            ('Upwork', 'Upwork'),
                                            ('StudentTable', 'StudentTable')),
                                   default='',
                                   max_length=100,
                                   db_index=True)


class TeacherAttestationUserHistory(BaseRel):
    attestation = models.ForeignKey(TeacherAttestation,
                                    on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    portfolio_expert = models.ForeignKey(Portfolio,
                                         null=True,
                                         blank=True,
                                         on_delete=models.CASCADE)
    operation = models.CharField(default='',
                                 max_length=10,
                                 db_index=True)


class Testing(BaseRel):
    deactivated = models.BooleanField(default=False)
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)
    kandidat = models.ForeignKey(Kandidat,
                                 on_delete=models.CASCADE)
    status = models.ForeignKey(TeacherStatus,
                               on_delete=models.CASCADE)
    attestation = models.ForeignKey(TeacherAttestation,
                                    on_delete=models.CASCADE)
    tester = models.ForeignKey(User,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    started = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    date_begin = models.DateTimeField(null=True,
                                      blank=True)
    date_end = models.DateTimeField(null=True,
                                    blank=True)
    verdikt = models.ForeignKey(Verdikt,
                                null=True,
                                blank=True,
                                on_delete=models.CASCADE)
    verdikt_system = models.ForeignKey(Verdikt,
                                       related_name='verdikt',
                                       null=True,
                                       on_delete=models.CASCADE)
    dead = models.NullBooleanField(default=None)


class TestingPortfolioListOfView(BaseRel):
    target = models.ForeignKey(PortfolioListOfView,
                               on_delete=models.CASCADE)
    ocenka = models.ForeignKey(TeacherScale,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    tester = models.ForeignKey(User,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    kandidat = models.ForeignKey(Kandidat,
                                 on_delete=models.CASCADE)


class TestingPortfolioBonus(BaseRel):
    target = models.ForeignKey(PortfolioBonus,
                               on_delete=models.CASCADE)
    ocenka = models.ForeignKey(TeacherScale,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    tester = models.ForeignKey(User,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    kandidat = models.ForeignKey(Kandidat,
                                 on_delete=models.CASCADE)


class TestingUpwork(BaseRel):
    target = models.ForeignKey(Upwork,
                               on_delete=models.CASCADE)
    ocenka = models.ForeignKey(TeacherScale,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    tester = models.ForeignKey(User,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    kandidat = models.ForeignKey(Kandidat,
                                 on_delete=models.CASCADE)


class TestingPortfolioBonusStudent(BaseRel):
    target = models.ForeignKey(PortfolioBonusStudent,
                               on_delete=models.CASCADE)
    ocenka = models.ForeignKey(TeacherScale,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    tester = models.ForeignKey(User,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    kandidat = models.ForeignKey(Kandidat,
                                 on_delete=models.CASCADE)


class TestingNote(BaseRel):
    target = models.ForeignKey(Note,
                               on_delete=models.CASCADE)
    ocenka = models.ForeignKey(TeacherScale,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    tester = models.ForeignKey(User,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    ocenka_type = models.IntegerField(null=True,
                                      blank=True)
    kandidat = models.ForeignKey(Kandidat,
                                 on_delete=models.CASCADE)


class TestingStudentTable(BaseRel):
    language = models.ForeignKey(Language,
                                 on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                on_delete=models.CASCADE)
    ocenka = models.ForeignKey(TeacherScale,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    tester = models.ForeignKey(User,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    kandidat = models.ForeignKey(Kandidat,
                                 on_delete=models.CASCADE)




class ErrorMessage(BaseRel):
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)
    error_message = models.TextField()
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    sended = models.BooleanField(default=False)


class Protocol(BaseRel):
    kandidat = models.ForeignKey(Kandidat,
                                 on_delete=models.CASCADE)
    tester = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    file = models.FileField(upload_to='usr/' + str(datetime.date.today()) + '/protocol')

    def save(self, *args, **kwargs):
        super(Protocol, self).save(*args, **kwargs)


class ChangeEmailTask(BaseRel):
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)
    email = models.CharField(default='',
                             max_length=255)
    old_email = models.CharField(default='',
                                 max_length=255)
    who = models.ForeignKey(User,
                            on_delete=models.CASCADE)


class StatementProtocol(BaseRel):
    school = models.ForeignKey(AlmaMater,
                               on_delete=models.CASCADE)
    attestation = models.ForeignKey(TeacherAttestation,
                                    null=False,
                                    verbose_name=trans('Attestation'),
                                    blank=False,
                                    on_delete=models.CASCADE)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    checked = models.BooleanField(default=False)
    not_checked = models.BooleanField(default=False)
    signature = models.TextField(default="")
    signed = models.BooleanField(default=False)


class StatementProtocolRecord(BaseRel):
    protocol = models.ForeignKey(StatementProtocol,
                                 on_delete=models.CASCADE)
    statement = models.ForeignKey(PortfolioStatement,
                                  on_delete=models.CASCADE)


class KandidatTester(BaseRel):
    kandidat = models.ForeignKey(Kandidat,
                                 on_delete=models.CASCADE)
    tester = models.ForeignKey(TeacherAttestationUser,
                               on_delete=models.CASCADE)
    attestation = models.ForeignKey(TeacherAttestation,
                                    on_delete=models.CASCADE)
    testing = models.ForeignKey(Testing,
                                null=True,
                                blank=True,
                                on_delete=models.CASCADE)


class GosCourse(BaseCatalog):
    course_type = models.ForeignKey(CourseType,
                                    verbose_name='Тип курса',
                                    on_delete=models.CASCADE)
    course_vid = models.ForeignKey(CourseVid,
                                   verbose_name='Уровень образования',
                                   null=True,
                                   blank=True,
                                   on_delete=models.CASCADE)
    course_subject = models.ManyToManyField(Subject,
                                            verbose_name='Предмет',
                                            # null=True,
                                            blank=True)
    center = models.ForeignKey(AlmaMater,
                               verbose_name='ЦПК',
                               on_delete=models.CASCADE)
    date_begin = models.DateField(verbose_name='Дата начала')
    date_end = models.DateField(verbose_name='Дата окончания')
    is_active = models.BooleanField(default=False,
                                    verbose_name='Активен')
    description = models.CharField(verbose_name='Описание курса',
                                   max_length=500,
                                   default='')
    slot_count = models.IntegerField(default=0,
                                     blank=False)
    address = models.CharField(default='',
                               max_length=300,
                               blank=False,
                               verbose_name='Адрес места проведения курса')
    begin_time = models.TimeField(blank=False,
                                  default="00:00",
                                  verbose_name='Время начала')
    end_time = models.TimeField(blank=False,
                                default="00:00",
                                verbose_name='Время окончания')
    slot_zan = models.IntegerField(default=0,
                                   blank=True)
    nabor = models.BooleanField(default=True,
                                verbose_name='Набор')
    study_language = models.ForeignKey(Language,
                                       verbose_name='Язык обучения',
                                       null=True,
                                       blank=False,
                                       on_delete=models.CASCADE)
    author = models.ForeignKey(User,
                               verbose_name='Автор курса',
                               blank=True,
                               null=True,
                               on_delete=models.CASCADE)


class CourseStatement(BaseRel):
    portfolio = models.ForeignKey(Portfolio,
                                  verbose_name='Учитель',
                                  on_delete=models.CASCADE)
    gos_course = models.ForeignKey(GosCourse,
                                   on_delete=models.CASCADE)
    checked = models.BooleanField(default=False)
    zavuch_checked = models.BooleanField(default=False)
    banned = models.BooleanField(default=False)
    school = models.ForeignKey(AlmaMater,
                               null=True,
                               verbose_name=trans('school'),
                               on_delete=models.CASCADE)
    priority = models.FloatField(default=0,
                                 blank=False)


class VacancySchool(BaseRel):
    class Meta:
        verbose_name = trans('vacancy school')
        verbose_name_plural = trans('vacancies school')

    vacancy_school = models.ForeignKey(AlmaMater,
                                       verbose_name=trans('school'),
                                       on_delete=models.CASCADE)
    position = models.ForeignKey(Position,
                                 verbose_name=trans('positions'),
                                 blank=False,
                                 max_length=200,
                                 on_delete=models.CASCADE)
    category_teacher = models.ManyToManyField(TeacherCategory,
                                              verbose_name='Требуемые категории',
                                              # verbose_name=trans('teacher category'),
                                              blank=True)
    english_level = models.ForeignKey(EnglishLevel,
                                      verbose_name='Требуемый уровень владения английским языком',
                                      null=True,
                                      #  verbose_name=trans('teacher category'),
                                      blank=True,
                                      on_delete=models.CASCADE)
    study_language = models.ManyToManyField(Language,
                                            verbose_name='Предполагаемое преподавание на языках',
                                            # verbose_name=trans('teacher category'),
                                            blank=False)
    load = models.FloatField(verbose_name='Нагрузка, ч',
                             default=0,
                             #  verbose_name=trans('load in hours')
                             )
    description = models.TextField(verbose_name=trans('description'),
                                   blank=True)
    author = models.ForeignKey(User,
                               blank=True,
                               on_delete=models.CASCADE)
    oklad = models.IntegerField(default=0,
                                null=True,
                                verbose_name='Оклад, KZT',
                                blank=True)
    status = models.ForeignKey(VacancyStatus,
                               verbose_name='Статус вакансии',
                               blank=False,
                               default=1,
                               on_delete=models.CASCADE)
    degree = models.ForeignKey(Degree,
                               verbose_name='Требуемая ученая степень',
                               null=True,
                               #  verbose_name=trans('teacher category'),
                               blank=True,
                               on_delete=models.CASCADE)
    stazh = models.FloatField(verbose_name='Стаж, лет',
                              default=0,
                              #  verbose_name=trans('load in hours')
                              )
    klass_ruk = models.BooleanField(default=False,
                                    verbose_name='Классное руководство')
    prov_tetr = models.BooleanField(default=False,
                                    verbose_name='Проверка тетрадей')


class VacancyStatement(BaseRel):
    vacancy = models.ForeignKey(VacancySchool,
                                null=True,
                                on_delete=models.CASCADE)

    phone_number = models.CharField(verbose_name='Номер телефона',
                                    max_length=20)
    portfolio = models.CharField(verbose_name='ФИО',
                                 max_length=70)
    email = models.EmailField(default="",
                              verbose_name='EMAIL')

    category_teacher = models.ManyToManyField(TeacherCategory,
                                              verbose_name='Ваша категория',
                                              # verbose_name=trans('teacher category'),
                                              blank=True)
    english_level = models.ForeignKey(EnglishLevel,
                                      null=True,
                                      #  verbose_name=trans('teacher category'),
                                      blank=True,
                                      on_delete=models.CASCADE)
    study_language = models.ManyToManyField(Language,
                                            verbose_name='На каких языках Вы преподаете',
                                            # verbose_name=trans('teacher category'),
                                            blank=False)

    description = models.TextField(verbose_name=trans('description'),
                                   blank=True)

    degree = models.ForeignKey(Degree,
                               null=True,
                               #  verbose_name=trans('teacher category'),
                               blank=True,
                               on_delete=models.CASCADE)
    stazh = models.FloatField(default=0,
                              #  verbose_name=trans('load in hours')
                              )


class VacancyStatementAuth(BaseRel):
    vacancy = models.ForeignKey(VacancySchool,
                                null=True,
                                on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio,
                                  null=True,
                                  on_delete=models.CASCADE)


class CategoryToCategory(models.Model):
    old = models.ForeignKey(TeacherCategory,
                            on_delete=models.CASCADE)
    new = models.ForeignKey(TeacherStatus,
                            on_delete=models.CASCADE)


class CPK(models.Model):  # Какая из школ входит в список центров повышения квалификации
    school = models.ForeignKey(AlmaMater,
                               on_delete=models.CASCADE)


class NotificationStatus(BaseCatalog):
    color = models.CharField(max_length=100,
                             default='')


class NotificationMessage(BaseCatalog):
    author = models.ForeignKey(Portfolio,
                               null=True,
                               related_name='author',
                               on_delete=models.CASCADE)
    announce = models.TextField(default='')
    detail = models.TextField(default='')
    recipient = models.ManyToManyField(Portfolio)
    status = models.ForeignKey(NotificationStatus,
                               null=True,
                               on_delete=models.CASCADE)
    parent = models.ForeignKey('self',
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)


class NotificationFile(BaseRel):
    notification = models.ForeignKey(NotificationMessage,
                                     null=True,
                                     on_delete=models.CASCADE)
    file = models.FileField(upload_to='usr/' + str(datetime.date.today()) + '/notifications')
    file_name = models.CharField(max_length=255,
                                 default='',
                                 blank=False)


class NotificationReader(BaseRel):
    user = models.ForeignKey(Portfolio,
                             on_delete=models.CASCADE)
    notification = models.ForeignKey(NotificationMessage,
                                     on_delete=models.CASCADE)
    hidden = models.BooleanField(default=False)


class PortfolioDopFile(BaseRel):
    obj_pk = models.IntegerField(default=0)
    file = models.FileField(upload_to='usr/' + str(datetime.date.today()) + '/dop_file/')
    model_name = models.CharField(default='',
                                  max_length=255)
    user = models.ForeignKey(User,
                             null=True,
                             on_delete=models.CASCADE)


class PortfolioArchive(BaseRel):
    kandidat = models.ForeignKey(Kandidat,
                                 null=True,
                                 on_delete=models.CASCADE)
    file = models.TextField(default='')


class PortfolioPedStazh(BaseRel):
    class Meta:
        unique_together = ['portfolio',
                           'position']

    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)
    position = models.ForeignKey(Position,
                                 on_delete=models.CASCADE)
    ped_stazh = models.FloatField(default=0)


class CompetitionVacancyStatus(BaseCatalog):
    pass


class CompetitionVacancy(BaseCatalog):
    school = models.ForeignKey(AlmaMater,
                               on_delete=models.CASCADE)
    position = models.ForeignKey(Position,
                                 on_delete=models.CASCADE)
    status = models.ForeignKey(CompetitionVacancyStatus,
                               blank=False,
                               null=True,
                               on_delete=models.CASCADE)


class CompetitionVacancyStatement(BaseRel):
    place_residence_fact = models.CharField(default='',
                                            verbose_name=trans('Location'),
                                            max_length=255)
    place_residence = models.CharField(default='',
                                       verbose_name=trans('Place of registration'),
                                       max_length=255)
    experience = models.IntegerField(default=0,
                                     verbose_name=trans('Experience'))

    experience_spec = models.IntegerField(default=0, verbose_name=trans('Professional experience'))

    experience_ped = models.IntegerField(default=0, verbose_name=trans('Pedagogical experience'))

    experience_this_school = models.IntegerField(default=0,
                                                 verbose_name=trans('Experience at the current (past) place of work'))
    vacancy = models.ForeignKey(CompetitionVacancy,
                                verbose_name=trans('Job'),
                                on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)
    checked = models.BooleanField(default=False)
    not_checked = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    not_accepeted = models.BooleanField(default=False)
    documents = models.ManyToManyField(PrivateDocument,
                                       blank=True)


class RegisterSchool(BaseCatalog):
    fio_rukovod = models.CharField(default='',
                                   max_length=255,
                                   verbose_name='ФИО')
    school_bin = models.CharField(default='',
                                  max_length=255,
                                  verbose_name='БИН')
    school_type = models.ForeignKey(SchoolType,
                                    null=True,
                                    on_delete=models.CASCADE,
                                    verbose_name='Тип организации'
                                    )
    school_phone = models.CharField(default='',
                                    max_length=255,
                                    verbose_name='Номер телефона'
                                    )
    school_email = models.CharField(default='',
                                    max_length=255,
                                    verbose_name='Адрес электронной почты')
    address = models.CharField(default='',
                               max_length=255,
                               verbose_name='Адрес'
                               )
    fio_otvetstv = models.CharField(default='',
                                    max_length=255,
                                    verbose_name='ФИО')
    phone_otvetstv = models.CharField(default='',
                                      max_length=255,
                                      verbose_name='Номер телефона')
    email_otvetstv = models.CharField(default='',
                                      max_length=255,
                                      verbose_name='Адрес электронной почты'
                                      )
    hash = models.TextField(verbose_name='хэш заявки',
                            blank=True)
    signature_iin = models.CharField(default='',
                                     max_length=255)
    signature_fio = models.CharField(default='',
                                     max_length=255)

    image = models.ImageField(upload_to='usr/' + str(datetime.date.today()) + '/responisble_statement',
                              verbose_name='Приказ')


class Recall(BaseRel):
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)
    text = models.TextField(default='',
                            verbose_name=trans('Leave your feedback'))


class RecallComment(BaseRel):
    recall = models.ForeignKey(Recall,
                               on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)
    text = models.TextField(default='',
                            verbose_name=trans('Leave your comment'))


class RecallLike(BaseRel):
    recall = models.ForeignKey(Recall,
                               on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)


class RecallDisLike(BaseRel):
    recall = models.ForeignKey(Recall,
                               on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)


class PortfolioCurrentCategory(BaseRel):
    class Meta:
        unique_together = ['portfolio', 'position']

    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)
    position = models.ForeignKey(Position,
                                 on_delete=models.CASCADE)
    category = models.ForeignKey(TeacherCategory,
                                 on_delete=models.CASCADE)
    category_year = models.DateTimeField(null=True)




class Contract(BaseRel):
    contract_number = models.CharField(default='', null=False, blank=False, max_length=255)
    school = models.ForeignKey(AlmaMater,
                               on_delete=models.CASCADE)
    date_begin = models.DateField(null=True)
    date_end = models.DateField(null=True)
    price = models.FloatField(default=0)
    discount = models.FloatField(default=0)


class Payment(BaseRel):
    contract = models.ForeignKey(Contract,
                                 on_delete=models.CASCADE)
    price = models.FloatField(default=0)


class PublicPortfolioPublications(BaseCatalog):
    text = models.TextField(default='')
    announce = models.TextField(default='')
    tags = models.CharField(default='',
                            max_length=255,
                            null=True,
                            blank=True)
    author = models.ForeignKey(Portfolio,
                               on_delete=models.CASCADE)


class PublicPortfolioPublicationComment(BaseRel):
    publication = models.ForeignKey(PublicPortfolioPublications,
                                    on_delete=models.CASCADE)
    author = models.ForeignKey(Portfolio,
                               on_delete=models.CASCADE)
    text = models.TextField(default='',
                            verbose_name=u'Комментарий')
    send_to = models.ForeignKey("self",
                                on_delete=models.CASCADE,
                                null=True)


class PublicaPortfolioPublicationWathcer(BaseRel):
    publication = models.ForeignKey(PublicPortfolioPublications,
                                    on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)


## sapirant change statart
class AspirantResume(BaseRel):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    text = models.CharField(max_length=255,
                            verbose_name=u'Описание',
                            null=False,
                            blank=False)
    positions = models.ManyToManyField(Position)
    category = models.ManyToManyField(TeacherCategory,
                                      blank=True)


class AspirantPrivate(BaseRel):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    text = models.CharField(max_length=255,
                            verbose_name=u'Описание',
                            null=True,
                            blank=True)
    image = models.ImageField(upload_to='usr/' + str(datetime.date.today()) + '/private_docs/',
                              verbose_name=u'Изображение')


## sapirant change end


class StatementToKill(BaseRel):
    statement = models.ForeignKey(PortfolioStatement,
                                  on_delete=models.CASCADE)


class DontHaveRecord(BaseRel):
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     null=True)
    user = models.ForeignKey(User,
                             null=True,
                             on_delete=models.CASCADE)
    pane = models.CharField(default='',
                            max_length=50,
                            blank=True)
    page_title = models.CharField(default='',
                                  max_length=50,
                                  blank=True)
    checked = models.BooleanField(default=False)
    anulirovan = models.BooleanField(default=False)



class DontHaveRecordRecord(models.Model):
    dhr = models.ForeignKey(DontHaveRecord,
                            on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class CheckRecordStatus(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE
                             )
    portfolio = models.ForeignKey(Portfolio,
                                  on_delete=models.CASCADE
                                  )
    pane = models.CharField(default='',
                            max_length=50,
                            blank=True)
    object_id = models.IntegerField(default=0)

    class Meta:
        unique_together = ['user',
                           'pane',
                           'object_id']

class AttestationProtocol1(BaseRel):
    attestation = models.ManyToManyField(TeacherAttestation,
                                         verbose_name=trans('Attestation'))
    text1 = models.TextField(default='')
    text2 = models.TextField(default='')
    text3 = models.TextField(default='')
    author = models.ForeignKey(Portfolio,
                               on_delete=models.CASCADE)

    file = models.FileField(null=True,
                            blank=True,
                            upload_to='att_prot/')
    uniq = models.CharField(max_length=255,
                            default='')


class TestCroperMain(BaseRel):
    image = models.ImageField(upload_to='usr/' + str(datetime.date.today()) + '/testcropers')
    model_name = models.CharField(max_length=255)
    object_pk = models.IntegerField()


class Meeting(BaseCatalog):
    uid = models.UUIDField(default=uuid4,
                           verbose_name='UUID')
    author = models.ForeignKey(Portfolio,
                               on_delete=models.CASCADE)
    attendeePW = models.UUIDField(default=uuid4,
                                  verbose_name='attendeer_PW')
    moderatorPW = models.UUIDField(default=uuid4,
                                   verbose_name='moderatorPW')
    school = models.ForeignKey(AlmaMater,
                               on_delete=models.CASCADE)
    date_begin = models.DateTimeField(null=True,
                                      blank=True)
    date_end = models.DateTimeField(null=True,
                                    blank=True)
    abuse_count = models.IntegerField(default=0)
    planned_date = models.DateTimeField(null=True,
                                        blank=False)
    server_id = models.IntegerField(default=0)
