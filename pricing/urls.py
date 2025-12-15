from django.urls import path
from pricing.views import pricingPageFront, api_pricings

urlpatterns = [
    path('pricing/', pricingPageFront, name='pricingPageFront'),
    path('api/pricings/', api_pricings, name='api_pricings'),
]
