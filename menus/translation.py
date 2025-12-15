from modeltranslation.translator import TranslationOptions, register
from .models import primaryMenu, subMenu


@register(primaryMenu)
class PrimaryMenuTranslationOptions(TranslationOptions):
    fields = ("name", "url")


@register(subMenu)
class SubMenuTranslationOptions(TranslationOptions):
    fields = ("name", "url")
