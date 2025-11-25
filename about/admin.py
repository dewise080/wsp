from django.contrib import admin
from about.models import *

# About Page Admin
admin.site.register(aboutPage)

# Team section admin
admin.site.register(teamSection)

# About page SEO admin
admin.site.register(aboutPageSEO)