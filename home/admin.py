from django.contrib import admin
from home.models import *

# Sliders Admin Register
admin.site.register(sliderSection)

# Services Admin Register
admin.site.register(serviceSection)

# About Admin Register
admin.site.register(aboutSection)

# Funfact Admin Register
admin.site.register(funFactSection)

# Project Category and Section Admin Register
admin.site.register(projectCategory)
admin.site.register(projectSection)

# Clinets Admin Register
admin.site.register(clientSection)

# Testimonial Admin Register
admin.site.register(testimonialsSection)

# Home Page SEO Admin Register
admin.site.register(homePageSEO)