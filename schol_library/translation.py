from modeltranslation.translator import translator, TranslationOptions
from .models import Provider


class ProviderTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Provider, ProviderTranslationOptions)