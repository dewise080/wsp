from modeltranslation.translator import TranslationOptions, register
from .models import blogCategory, Blogs, blogPageSEO


@register(blogCategory)
class BlogCategoryTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(Blogs)
class BlogsTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "description",
        "author",
    )


@register(blogPageSEO)
class BlogPageSEOTranslationOptions(TranslationOptions):
    fields = ("meta_title", "meta_description")
