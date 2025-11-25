from django.urls import path 
from custompage.views import *

urlpatterns = [
    path('admin/custom-pages/', adminCustomPage.as_view(), name='adminCustomPage'),
    path('admin/create/custom-page/', adminCustomPageCreate.as_view(), name='adminCustomPageCreate'),
    path('admin/custom-pages/edit/<str:slug>', adminCustomPageEdit.as_view(), name='adminCustomPageEdit'),
    path('admin/custom-pages/<int:id>', adminCustomPageDelete, name='adminCustomPageDelete'),
    
    path('<str:slug>/', customPageFront, name='customPageFront')
]
