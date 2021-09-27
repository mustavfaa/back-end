from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext as _
from portfoli import models as p_models
from portfoli.models import Portfolio, AlmaMater
from schol_library.models import NumberBooks, EditionInvoice, EditionPaperInvoice, RequestEdition
from django.utils import timezone
from ekitaphana.settings import BASE_URL
def sum_quantity(value):
    d = dict()
    d['edition_id'] = value['edition_id']
    d['quantity'] = value['on_hands'] + value['in_warehouse']
    return d


class PageCabinet(p_models.BaseCatalog):
    class Meta:
        verbose_name = _('Страница кабинета для доступа')
        verbose_name_plural = _('Страницы кабинета для доступа')
        ordering = ['id']


class LibraryUser(models.Model):
    user = models.OneToOneField(User, verbose_name=_('пользователь'), on_delete=models.CASCADE)
    create_school = models.ForeignKey(AlmaMater, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = _('Портфолио Ekitaphana')
        verbose_name_plural =_('Портфолии Ekitaphana')

    def __str__(self):
        return '{}'.format(self.user.username)

    def avatar(self):
        try:
            return Portfolio.objects.filter(user=self.user).first()
        except self.user.portfolio_set.first().DoesNotExist:
            return None

    @property
    def get_avatar(self):
        try:
            return BASE_URL + '{}'.format(str(Portfolio.objects.filter(user=self.user).first().avatar.url)[6:])
            return Portfolio.objects.filter(user=self.user).first().avatar.url
        except self.user.portfolio_set.first().DoesNotExist:
            return None

    @property
    def school(self):
        try:
            if 6 in self.user.groups.values_list('id', flat=True) and self.create_school != None:
                return self.create_school
            else:
                return p_models.PortfolioWorkTimeLine.objects.filter(deleted=False,
                                                                     current=True,
                                                                     uvolen=False,
                                                                     portfolio__user=self.user).first().school
        except:
            return None


STATUS = (
    (0, _('Нет доступа')),
    (1, _('Есть доступ')),
)


class AccessToEdit(p_models.BaseRel):
    school = models.OneToOneField(p_models.AlmaMater, verbose_name=_('школа'), on_delete=models.CASCADE, blank=True)
    edit_status = models.SmallIntegerField(verbose_name=_('статус редактирования'), choices=STATUS, default=0, blank=True)
    date_invoice = models.DateField(verbose_name=_('Дата для накладных'), default=timezone.now, blank=True)
    status_12 = models.SmallIntegerField(verbose_name=_('статус для первой и второй страницы'), choices=STATUS, default=1, blank=True)

    class Meta:
        verbose_name = _('Доступ для редактирования')
        verbose_name_plural =_('Доступы для редактирования')

    def __str__(self):
        return '{}'.format(self.school.name)


# История назначения на должностей
class RoleHistory(p_models.BaseRel):
    user = models.ForeignKey(User, verbose_name=_('пользователь'), on_delete=models.CASCADE)
    school = models.ForeignKey(p_models.AlmaMater, verbose_name=_('школа'), on_delete=models.CASCADE)
    role = models.ForeignKey(Group, verbose_name=_('роль'), on_delete=models.CASCADE, null=True, blank=True)
    data_appointment = models.DateTimeField(verbose_name=_('Дата назначения на должность'), blank=True)
    data_end = models.DateTimeField(verbose_name=_('Дата окончания на должности'), null=True, blank=True)

    class Meta:
        verbose_name = _('Журнал назначений')
        verbose_name_plural = _('Журналы назначении')
        ordering = ['-data_appointment']

    def __str__(self):
        return '{}'.format(self.user.username)
