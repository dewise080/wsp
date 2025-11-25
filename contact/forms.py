from django import forms 
from contact.models import *

# # # # # # # # # # # # # # # # # #
    # Contact Form #
# # # # # # # # # # # # # # # # # #
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# # # # # # # # # # # # # # # # # #
    # Subscriber Form #
# # # # # # # # # # # # # # # # # #
class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# # # # # # # # # # # # # # # # # #
    # Contact Page SEO Form #
# # # # # # # # # # # # # # # # # #
class contactPageSEOForm(forms.ModelForm):
    class Meta:
        model = contactPageSEO
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'