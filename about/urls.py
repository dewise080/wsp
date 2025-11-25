from django.urls import path
from about.views import *

urlpatterns = [
    path('about-us/', aboutPageFront, name='aboutPageFront'),
]
