from modeltranslation.translator import TranslationOptions, register
from .models import customPage


@register(customPage)
class CustomPageTranslationOptions(TranslationOptions):
    fields = ("title", "content")
