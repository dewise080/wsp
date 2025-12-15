from modeltranslation.translator import TranslationOptions, register
from .models import Terms, Policy


@register(Terms)
class TermsTranslationOptions(TranslationOptions):
    fields = ("term_texts",)


@register(Policy)
class PolicyTranslationOptions(TranslationOptions):
    fields = ("policy_texts",)
