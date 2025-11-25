from django.urls import path
from service.views import *

urlpatterns = [
    path('services/', serviceFrontPage, name='serviceFrontPage'),
    path('service/details/<str:slug>/', serviceDetail, name='serviceDetail'),
]
