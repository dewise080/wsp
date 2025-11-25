from django.urls import path 
from blog.views import *

urlpatterns = [
    path('blogs/', blogPageFront, name='blogPageFront'),
    path('blog/<str:slug>/', blogDetails, name='blogDetails'),
    path('blog/category/<slug:category_slug>/', blogsByCategory, name='blogsByCategory'),
    path('api/blogs/', api_blogs, name='api_blogs'),
    path('api/blog-categories/', api_blog_categories, name='api_blog_categories'),
]
