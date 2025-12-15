from modeltranslation.translator import TranslationOptions, register

from .models import BlogSampleConversation


@register(BlogSampleConversation)
class BlogSampleConversationTranslationOptions(TranslationOptions):
    # Keep title/subtitle translated; conversations_* are handled as explicit fields.
    fields = ("title", "subtitle")
