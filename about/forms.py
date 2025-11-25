from django import forms
from about.models import *

# About Page Form
class aboutPageForm(forms.ModelForm):
    class Meta:
        model = aboutPage
        fields = '__all__'
        widgets = {
            'description' : forms.Textarea(attrs={'rows' : 4})
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control' 
        
# Team Section Form
class teamSectionForm(forms.ModelForm):
    class Meta:
        model = teamSection
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'  

# About Page SEO Form
class aboutPageSEOForm(forms.ModelForm):
    class Meta:
        model = aboutPageSEO
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
