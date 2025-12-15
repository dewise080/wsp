from django.contrib import admin
from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.conf.urls.i18n import i18n_patterns
from core.sitemaps import generate_sitemap
from core import views_admin
from core import views_ai
from home import views as home_views
from blog import views as blog_views
from sampleconversations import views as sc_views
from workflows import views as workflow_views

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path("rosetta/", include("rosetta.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/translations/", views_admin.translation_overview, name="translation_overview"),
    path('sitemap.xml', generate_sitemap, name='generate_sitemap'),
]

# Non-i18n API endpoints to avoid locale redirects stripping POST bodies
urlpatterns += [
    path("api/services/", home_views.api_services, name="api_services_plain"),
    path("api/testimonials/", home_views.api_testimonials, name="api_testimonials_plain"),
    path("api/about/", home_views.api_about, name="api_about_plain"),
    path("api/project-categories/", home_views.api_project_categories, name="api_project_categories_plain"),
    path("api/projects/", home_views.api_projects, name="api_projects_plain"),
    path("api/blog-categories/", blog_views.api_blog_categories, name="api_blog_categories_plain"),
    path("api/blogs/", blog_views.api_blogs, name="api_blogs_plain"),
    path(
        "api/blog-sample-conversations/",
        sc_views.BlogSampleConversationAPIView.as_view(),
        name="blog_sample_conversation_api_plain",
    ),
    path("api/workflows/", workflow_views.api_workflows, name="api_workflows_plain"),
    path(
        "api/workflows/<slug:slug>/json/",
        workflow_views.workflowJsonApi,
        name="workflowJsonApi_plain",
    ),
]

urlpatterns += i18n_patterns(
    path('oldadmin/', admin.site.urls),
    path('admin/' , RedirectView.as_view(pattern_name="adminHome"), name='adminRedirect'),
    path('dashboard/' , RedirectView.as_view(pattern_name="adminHome"), name='adminRedirect2'),
    path('api/ai/enrich/', views_ai.ai_enrich, name='ai_enrich'),
    path('', include('adminapp.urls')),
    path('', include('accounts.urls')),
    path('', include('home.urls')),
    path('', include('about.urls')),
    path('', include('pricing.urls')),
    path('', include('blog.urls')),
    path('', include('contact.urls')),
    path('', include('service.urls')),
    path('', include('project.urls')),
    path('', include('legal.urls')),
    path('', include('marketing.urls')),
    path('', include('workflows.urls')),
    path('', include('custompage.urls')),
    path('', include('sampleconversations.urls')),
)

handler404 = 'accounts.views.error_404'
handler404 = 'adminapp.views.error_404'
handler404 = 'home.views.error_404'
handler404 = 'service.views.error_404'
handler404 = 'project.views.error_404'
handler404 = 'contact.views.error_404'
handler404 = 'about.views.error_404'
handler404 = 'blog.views.error_404'
handler404 = 'settings.views.error_404'
handler404 = 'legal.views.error_404'

handler500 = 'adminapp.views.error_500'

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static
# from django.views.generic import RedirectView
# from django.conf.urls.i18n import i18n_patterns  # Import i18n_patterns

# from core.sitemaps import generate_sitemap

# urlpatterns = [
#     # Your non-i18n patterns here
#     path('oldadmin/', admin.site.urls),
#     path('admin/', RedirectView.as_view(pattern_name="adminHome"), name='adminRedirect'),
#     path('dashboard/', RedirectView.as_view(pattern_name="adminHome"), name='adminRedirect2'),
#     path('sitemap.xml', generate_sitemap, name='generate_sitemap'),
# ]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# # Wrap existing URL patterns with i18n_patterns
# urlpatterns += i18n_patterns(
#     # Include your app's URL patterns here
#     path('', include('adminapp.urls')),
#     path('', include('accounts.urls')),
#     path('', include('home.urls')),
#     path('', include('about.urls')),
#     path('', include('pricing.urls')),
#     path('', include('blog.urls')),
#     path('', include('contact.urls')),
#     path('', include('service.urls')),
#     path('', include('project.urls')),
#     path('', include('legal.urls')),
#     path('', include('marketing.urls')),
#     path('', include('custompage.urls')),
# )

# handler404 = 'accounts.views.error_404'
# handler404 = 'adminapp.views.error_404'
# handler404 = 'home.views.error_404'
# handler404 = 'service.views.error_404'
# handler404 = 'project.views.error_404'
# handler404 = 'contact.views.error_404'
# handler404 = 'about.views.error_404'
# handler404 = 'blog.views.error_404'
# handler404 = 'settings.views.error_404'
# handler404 = 'legal.views.error_404'

# handler500 = 'adminapp.views.error_500'
