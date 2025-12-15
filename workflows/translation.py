from modeltranslation.translator import TranslationOptions, register
from .models import (
    Workflow,
    WorkflowNode,
    WorkflowNodeItem,
    WorkflowPageSEO,
)


@register(Workflow)
class WorkflowTranslationOptions(TranslationOptions):
    fields = ("name", "description")


@register(WorkflowNode)
class WorkflowNodeTranslationOptions(TranslationOptions):
    fields = ("label", "description", "icon_alt")


@register(WorkflowNodeItem)
class WorkflowNodeItemTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(WorkflowPageSEO)
class WorkflowPageSEOTranslationOptions(TranslationOptions):
    fields = ("meta_title", "meta_description")
