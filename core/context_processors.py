from settings.models import *
from accounts.models import UserProfile
from menus.models import *
from home.models import serviceSection, projectSection
from django.conf import settings

# Website Setting Context
def website_settings_context(request):
    settings = websiteSetting.objects.first()
    return {'settings': settings}

def seo_settings_context(request):
    seo_settings = SeoSetting.objects.first()
    return {'seo_settings': seo_settings}

def header_footer_context(request):
    header_footer = headerFooterSetting.objects.first()
    return {'header_footer': header_footer}

# Menu Context
def menu_data(request):
    primary_menus = primaryMenu.objects.all()
    sub_menus = subMenu.objects.all()

    return {
        'primary_menus': primary_menus,
        'sub_menus': sub_menus,
    }

## User Profile Context Processor
def user_profile_context(request):
    user_profile = None
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.filter(user=request.user).first()
    return {
        'user_profile': user_profile
    }

# Service Context Processor
def service_context(request):
    services = serviceSection.objects.all()
    return {
       'fservices': services,
    }

# Project Context Processor
def project_context(request):
    projects = projectSection.objects.all().order_by('?')
    return {
       'fprojects': projects,
    }

## Demo Mode Template Context Proccessor
def demo_mode_enabled(request):
    return {'demo_mode_enabled': 'core.middleware.middleware.DemoModeMiddleware' in settings.MIDDLEWARE}