from django import forms
from portfoli import models as p_models
from .models import NumberBooks, Edition, SchoolTitul, StudyDirections
from django.utils.translation import ugettext as _


class NumberBooksForm(forms.ModelForm):
    class Meta:
        model = NumberBooks
        fields = ['edition']


# class SchoolTitulForm(forms.ModelForm):
#     klass = forms.ModelChoiceField(
#         label=_('Класс'),
#         queryset=p_models.Klass.objects.all(),
#         widget=forms.Select(attrs={'class': 'floating-select', 'v-model': "schoolTitulForm.klass"})
#     )
#     liter = forms.CharField(
#         label=_('Литера класса'),
#         max_length=3,
#         widget=forms.TextInput(attrs={'class': 'floating-input', 'v-model': 'schoolTitulForm.liter'})
#     )
#     students = forms.IntegerField(
#         label=_('Кол-во учащих'),
#         widget=forms.NumberInput(attrs={'class': 'floating-input', 'min': 0, 'v-model': 'schoolTitulForm.students'})
#     )
#     year = forms.ModelChoiceField(
#         label=_('Учебные годы'),
#         queryset=p_models.DateObjects.objects.all(),
#         widget=forms.Select(attrs={'class': 'floating-select', 'v-model': 'schoolTitulForm.year'})
#     )
#     language = forms.ModelChoiceField(
#         label=_('Язык обучения'),
#         queryset=p_models.Language.objects.all(),
#         widget=forms.Select(attrs={'class': 'floating-select', 'v-model': 'schoolTitulForm.language'})
#     )
#     study_direction = forms.ModelChoiceField(
#         label=_('Форма обучения'),
#         queryset=StudyDirections.objects.all(),
#         widget=forms.Select(attrs={'class': 'floating-select', 'v-model': 'schoolTitulForm.study_direction'})
#     )
#
#     class Meta:
#         model = SchoolTitul
#         exclude = ['deleted', 'date_added', 'comment', 'exchange', 'is_exchange', 'school']
