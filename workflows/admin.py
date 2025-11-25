from django.contrib import admin
from .models import Workflow, WorkflowNode, WorkflowNodeItem, WorkflowEdge, WorkflowPageSEO


class WorkflowNodeItemInline(admin.TabularInline):
    model = WorkflowNodeItem
    extra = 1


class WorkflowNodeInline(admin.TabularInline):
    model = WorkflowNode
    extra = 1
    fields = ['node_id', 'node_type', 'label', 'description', 'icon_slug', 'icon_color']


class WorkflowEdgeInline(admin.TabularInline):
    model = WorkflowEdge
    extra = 1
    fk_name = 'workflow'


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [WorkflowNodeInline, WorkflowEdgeInline]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(WorkflowNode)
class WorkflowNodeAdmin(admin.ModelAdmin):
    list_display = ['workflow', 'node_id', 'node_type', 'label']
    list_filter = ['workflow', 'node_type']
    search_fields = ['label', 'description']
    inlines = [WorkflowNodeItemInline]


@admin.register(WorkflowNodeItem)
class WorkflowNodeItemAdmin(admin.ModelAdmin):
    list_display = ['node', 'slug', 'name', 'color', 'order']
    list_filter = ['node__workflow']
    search_fields = ['name', 'slug']


@admin.register(WorkflowEdge)
class WorkflowEdgeAdmin(admin.ModelAdmin):
    list_display = ['workflow', 'edge_id', 'source_node', 'target_node']
    list_filter = ['workflow']


@admin.register(WorkflowPageSEO)
class WorkflowPageSEOAdmin(admin.ModelAdmin):
    list_display = ['meta_title', 'meta_description']
