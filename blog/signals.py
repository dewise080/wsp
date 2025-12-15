from django.db.models.signals import post_save
from django.dispatch import receiver

from core.translation_hooks import trigger_auto_translate
from .models import Blogs, blogCategory


def _should_translate(update_fields, source_fields):
    """
    Return True when either update_fields is empty (full save)
    or when any of the source fields are being updated.
    """
    if not update_fields:
        return True
    return bool(source_fields.intersection(update_fields))


@receiver(post_save, sender=Blogs)
def auto_translate_blog(sender, instance, created, update_fields, **kwargs):
    source_fields = {"title", "description", "author"}
    # Skip if this save only touched translation fields.
    if not _should_translate(update_fields, source_fields):
        return
    trigger_auto_translate("blog.blogs", instance.pk)


@receiver(post_save, sender=blogCategory)
def auto_translate_blog_category(sender, instance, created, update_fields, **kwargs):
    source_fields = {"title"}
    if not _should_translate(update_fields, source_fields):
        return
    trigger_auto_translate("blog.blogcategory", instance.pk)
