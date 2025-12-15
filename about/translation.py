from modeltranslation.translator import TranslationOptions, register
from .models import aboutPage, teamSection, aboutPageSEO


@register(aboutPage)
class AboutPageTranslationOptions(TranslationOptions):
    fields = (
        "subtitle",
        "title",
        "description",
        "feature1",
        "feature2",
        "feature3",
    )


@register(teamSection)
class TeamSectionTranslationOptions(TranslationOptions):
    fields = ("name", "position")


@register(aboutPageSEO)
class AboutPageSEOTranslationOptions(TranslationOptions):
    fields = ("meta_title", "meta_description")
