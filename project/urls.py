from django.urls import path
from project.views import *

urlpatterns = [
    path('projects/', projectPageFront, name='projectPageFront'),
    path('project/details/<str:slug>/', projectDetails, name='projectDetails'),
]
