from django.urls import path
from pricing.views import pricingPageFront

urlpatterns = [
    path('pricing/', pricingPageFront, name='pricingPageFront'),
]
