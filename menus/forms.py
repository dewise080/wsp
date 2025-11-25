from django import forms 
from menus.models import *

class primaryMenuForm(forms.ModelForm):
    class Meta:
        model = primaryMenu
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class subMenuForm(forms.ModelForm):
    class Meta:
        model = subMenu
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'