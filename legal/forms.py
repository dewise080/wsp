from django import forms 
from legal.models import *

# Terms Form
class termsForm(forms.ModelForm):
    class Meta:
        model = Terms
        fields = '__all__'

# Policy Form
class policyForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = '__all__'