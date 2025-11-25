from django import forms
from pricing.models import *

# Pricing Form
class pricingForm(forms.ModelForm):
    class Meta:
        model = pricingSection
        fields = '__all__'
        widgets = {
            'is_featured' : forms.CheckboxInput(attrs={'type' : 'checkbox'})
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'   
            
class pricingPageSEOForm(forms.ModelForm):
    class Meta:
        model = pricingPageSEO
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'   