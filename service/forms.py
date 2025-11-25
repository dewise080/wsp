from django import forms 
from service.models import *

# Service Page SEO Form
class servicePageSEOForm(forms.ModelForm):
    class Meta:
        model = servicePageSEO
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'