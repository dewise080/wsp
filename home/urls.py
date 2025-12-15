from django.urls import path
from home.views import *

urlpatterns = [
    path('' , homePageFront, name='homePageFront'),
    path('api/services/', api_services, name='api_services'),
    path('api/testimonials/', api_testimonials, name='api_testimonials'),
    path('api/about/', api_about, name='api_about'),
    path('api/funfacts/', api_funfacts, name='api_funfacts'),
    path('api/clients/', api_clients, name='api_clients'),
    path('api/projects/', api_projects, name='api_projects'),
    path('api/project-categories/', api_project_categories, name='api_project_categories'),
    path('openapi.json', openapi_json, name='openapi_json'),
    path('docs/', openapi_docs, name='openapi_docs'),
]
