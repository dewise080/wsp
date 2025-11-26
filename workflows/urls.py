from django.urls import path
from . import views

urlpatterns = [
    # Admin URLs
    path('admin/workflows', views.adminWorkflowList, name='adminWorkflowList'),
    path('admin/workflows/create', views.adminWorkflowCreate, name='adminWorkflowCreate'),
    path('admin/workflows/edit/<slug:slug>', views.adminWorkflowEdit, name='adminWorkflowEdit'),
    path('admin/workflows/modifier/<slug:slug>', views.adminWorkflowModifier, name='adminWorkflowModifier'),
    path('admin/workflows/delete/<int:id>', views.adminWorkflowDelete, name='adminWorkflowDelete'),
    path('admin/workflows/save-json/<slug:slug>', views.adminWorkflowSaveJson, name='adminWorkflowSaveJson'),
    path('admin/workflows/upload-json/<slug:slug>', views.adminWorkflowUploadJson, name='adminWorkflowUploadJson'),
    
    # Frontend URLs
    path('workflows/', views.workflowList, name='workflowList'),
    path('workflows/<slug:slug>/', views.workflowDetail, name='workflowDetail'),
    path('api/workflows/<slug:slug>/json/', views.workflowJsonApi, name='workflowJsonApi'),
    path('api/workflows/', views.api_workflows, name='api_workflows'),
]
