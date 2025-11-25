from django import forms
from settings.models import *

class websiteSettingForm(forms.ModelForm):
    class Meta:
        model = websiteSetting
        fields = '__all__'
        widgets = {
            'facebook_pixel_code' : forms.Textarea(attrs={'rows':6}),
            'facebook_chat_code' : forms.Textarea(attrs={'rows':6}),
            'map_iframe' : forms.Textarea(attrs={'rows':4}),
            'custom_css' : forms.Textarea(attrs={'rows':6}),
            'custom_js' : forms.Textarea(attrs={'rows':6}),
            'whatsapp_is_active' : forms.CheckboxInput(attrs={'type' : 'checkbox'}),
            'facebook_chat_is_active' : forms.CheckboxInput(attrs={'type' : 'checkbox'}),
            'slider_particle_is_active' : forms.CheckboxInput(attrs={'type' : 'checkbox'}),
            'default_menu_is_active' : forms.CheckboxInput(attrs={'type' : 'checkbox'}),
            'magic_cursor_is_active' : forms.CheckboxInput(attrs={'type' : 'checkbox'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class SeoSettingForm(forms.ModelForm):
    class Meta:
        model = SeoSetting
        fields = '__all__'
        widgets = {
            'meta_description' : forms.Textarea(attrs={'rows':3}),
            'seo_keywords' : forms.Textarea(attrs={'rows':4, 'placeholder' : 'software,application,marketer,developer'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class headerFooterSettingForm(forms.ModelForm):
    class Meta:
        model = headerFooterSetting
        fields = '__all__'
        widgets = {
            'footer_col1_description' : forms.Textarea(attrs={'rows':4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class templateForm(forms.ModelForm):
    class Meta:
        model = templateSettings
        fields = '__all__'