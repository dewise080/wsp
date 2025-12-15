from modeltranslation.translator import TranslationOptions, register
from .models import contactPageSEO


@register(contactPageSEO)
class ContactPageSEOTranslationOptions(TranslationOptions):
    fields = ("meta_title", "meta_description")
