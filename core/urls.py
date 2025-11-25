from django.contrib import admin
from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from core.sitemaps import generate_sitemap

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path('oldadmin/', admin.site.urls),
    path('admin/' , RedirectView.as_view(pattern_name="adminHome"), name='adminRedirect'),
    path('dashboard/' , RedirectView.as_view(pattern_name="adminHome"), name='adminRedirect2'),
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
    path('sitemap.xml', generate_sitemap, name='generate_sitemap'),
]

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
