from django import forms 
from project.models import *

# About Page SEO Form
class projectPageSEOForm(forms.ModelForm):
    class Meta:
        model = projectPageSEO
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'