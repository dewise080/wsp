from django.db import models
from ckeditor.fields import RichTextField

class websiteSetting(models.Model):
    # General Settings
    name = models.CharField(max_length=500, default='Application Name', blank=True, null=True)
    author = models.CharField(max_length=200, default='Author Name', blank=True, null=True)
    currency_name = models.CharField(max_length=100, blank=True, null=True, default='Currency Name')
    currency_symbol = models.CharField(max_length=150, blank=True, null =True, default='Currency Symbol')
    show_call_now_widget = models.BooleanField(default=True)

    # Logo Settings
    logo_light = models.ImageField(upload_to='app_config/', blank=True, null=True)
    logo_dark = models.ImageField(upload_to='app_config/', blank=True, null=True)
    favicon = models.ImageField(upload_to='app_config/', blank=True, null=True)
    
    # Contact Settings
    email_address = models.EmailField(max_length=500, default='test@gmail.com', blank=True, null=True)
    phone = models.CharField(max_length=20, default='88012454784', blank=True, null=True)
    price_ragne = models.CharField(max_length=50, default='60$ to 7000$', blank=True, null=True)
    address = models.CharField(max_length=700, default='Your Address', blank=True, null=True)
    city = models.CharField(max_length=200, default='Your City', blank=True, null=True)
    country = models.CharField(max_length=300, default='Your Country', blank=True, null=True)
    state = models.CharField(max_length=200, default='Your State', blank=True, null=True)
    postal = models.IntegerField(default=12345, blank=True, null=True)
    map_iframe = models.TextField(blank=True, null=True)
    contact_form_image = models.ImageField(upload_to='app_config/', blank=True, null=True)
    
    analytics_code = models.CharField(max_length=300, blank=True, null=True, default="GA_MEASUREMENT_ID")
    facebook_pixel_code = models.TextField(blank=True, null=True)
    facebook_chat_code = models.TextField(blank=True, null=True)

    whatsapp_is_active = models.BooleanField(default=True)
    facebook_chat_is_active = models.BooleanField(default=True)
    slider_particle_is_active = models.BooleanField(default=True)
    default_menu_is_active = models.BooleanField(default=True)
    magic_cursor_is_active = models.BooleanField(default=True)

    custom_css = models.TextField(blank=True, null=True)
    custom_js = models.TextField(blank=True, null=True)
    
    twilio_sid = models.CharField(max_length=500, blank=True, null=True)
    twilio_auth_token = models.CharField(max_length=500, blank=True, null=True)
    twilio_from_number = models.CharField(max_length=15, blank=True, null=True)
    
    def getLogoLight(self):
        if self.logo_light:
            return self.logo_light.url
        return ''
    
    def getLogoDark(self):
        if self.logo_dark:
            return self.logo_dark.url
        return ''
    
    def getFavicon(self):
        if self.favicon:
            return self.favicon.url
        return ''
    
    def __str__(self):
        return 'Website Setting Configs'

class SeoSetting(models.Model):
    meta_title = models.CharField(max_length=500, blank=True, null=True)
    tag_line = models.CharField(max_length=600, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    seo_keywords = models.TextField(default='software,application,marketer,developer', blank=True, null=True)
    meta_image = models.ImageField(upload_to='app_config/', blank=True, null=True)

    def __str__(self):
        return 'SEO Setting Configs'

class headerFooterSetting(models.Model):
    header_button_text = models.CharField(max_length=200, blank=True, null=True)
    header_button_url = models.CharField(max_length=1000, blank=True, null=True)

    footer_col1_description = models.TextField(blank=True, null=True)
    
    social1_icon = models.CharField(max_length=200, blank=True, null=True)
    social1_link = models.CharField(max_length=1000, blank=True, null=True)
    
    social2_icon = models.CharField(max_length=200, blank=True, null=True)
    social2_link = models.CharField(max_length=1000, blank=True, null=True)
    
    social3_icon = models.CharField(max_length=200, blank=True, null=True)
    social3_link = models.CharField(max_length=1000, blank=True, null=True)
    
    social4_icon = models.CharField(max_length=200, blank=True, null=True)
    social4_link = models.CharField(max_length=1000, blank=True, null=True)

    footer_copyright = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return 'Header Footer Setting Configs'
    
class templateSettings(models.Model):
    template1 = models.BooleanField(default=True)
    template2 = models.BooleanField(default=False)
    
