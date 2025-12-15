from modeltranslation.translator import TranslationOptions, register
from .models import (
    sliderSection,
    serviceSection,
    aboutSection,
    funFactSection,
    projectCategory,
    projectSection,
    clientSection,
    testimonialsSection,
    homePageSEO,
)


@register(sliderSection)
class SliderSectionTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "subtitle",
        "description",
        "button1_text",
        "button2_text",
    )


@register(serviceSection)
class ServiceSectionTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "short_description",
        "detail_page_description",
    )


@register(aboutSection)
class AboutSectionTranslationOptions(TranslationOptions):
    fields = (
        "subtitle",
        "title",
        "short_description",
        "long_description",
        "tag_line",
        "experience",
    )


@register(funFactSection)
class FunFactSectionTranslationOptions(TranslationOptions):
    fields = ("title", "count_after")


@register(projectCategory)
class ProjectCategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(projectSection)
class ProjectSectionTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "description",
        "client",
        "company",
        "duration",
    )


@register(clientSection)
class ClientSectionTranslationOptions(TranslationOptions):
    fields = ("client_name",)


@register(testimonialsSection)
class TestimonialsSectionTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "position",
        "description",
    )


@register(homePageSEO)
class HomePageSEOTranslationOptions(TranslationOptions):
    fields = ("meta_title", "meta_description")
