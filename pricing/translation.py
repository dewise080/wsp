from modeltranslation.translator import TranslationOptions, register
from .models import pricingSection, pricingPageSEO


@register(pricingSection)
class PricingSectionTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "subtitle",
        "price",
        "description",
        "button_text",
        "button_url",
        "featured_text",
    )


@register(pricingPageSEO)
class PricingPageSEOTranslationOptions(TranslationOptions):
    fields = ("meta_title", "meta_description")
