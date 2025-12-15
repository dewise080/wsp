from modeltranslation.translator import TranslationOptions, register
from .models import servicePageSEO


@register(servicePageSEO)
class ServicePageSEOTranslationOptions(TranslationOptions):
    fields = ("meta_title", "meta_description")
