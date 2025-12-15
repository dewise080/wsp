from modeltranslation.translator import TranslationOptions, register
from .models import projectPageSEO


@register(projectPageSEO)
class ProjectPageSEOTranslationOptions(TranslationOptions):
    fields = ("meta_title", "meta_description")
