from django.urls import path
from home.views import *

urlpatterns = [
    path('' , homePageFront, name='homePageFront'),
    path('api/services/', api_services, name='api_services'),
    path('api/projects/', api_projects, name='api_projects'),
    path('api/project-categories/', api_project_categories, name='api_project_categories'),
    path('openapi.json', openapi_json, name='openapi_json'),
]
