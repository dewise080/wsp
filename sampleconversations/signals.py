import logging

from django.core.management import call_command
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BlogSampleConversation

logger = logging.getLogger(__name__)


def _should_translate(update_fields, source_fields):
    # If update_fields is empty/None, treat as full save.
    if not update_fields:
        return True
    return not source_fields.isdisjoint(update_fields)


@receiver(post_save, sender=BlogSampleConversation)
def auto_translate_sample_conversation(sender, instance, created, update_fields, **kwargs):
    """
    Run translations synchronously when source fields change.
    Skip when only translation fields are being saved to avoid loops.
    """
    source_fields = {"title", "subtitle", "conversations", "conversations_en"}
    if not _should_translate(update_fields, source_fields):
        return

    if not any(
        [
            instance.title,
            instance.subtitle,
            bool(instance.conversations),
            bool(instance.conversations_en),
        ]
    ):
        return

    try:
        call_command(
            "auto_translate_models",
            model="sampleconversations.blogsampleconversation",
            pks=[str(instance.pk)],
            force=True,
            verbosity=0,
        )
    except Exception as exc:
        logger.warning("Auto-translate failed for BlogSampleConversation#%s: %s", instance.pk, exc)
