from django.urls import path
from legal.views import *

urlpatterns = [
    path('terms-&-conditions/' , termsPageFront, name='termsPageFront'),
    path('privacy-policy/' , policyPageFront, name='policyPageFront'),
]
