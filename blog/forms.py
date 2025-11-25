from django import forms
from blog.models import *

class blogFrom(forms.ModelForm):
    class Meta:
        model = Blogs
        fields = '__all__'
        widgets = {
            'slug' : forms.TextInput(attrs={'readonly':'readonly'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class blogCategoryForm(forms.ModelForm):
    class Meta:
        model = blogCategory
        fields = '__all__'
        widgets = {
            'slug' : forms.TextInput(attrs={'readonly':'readonly'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class blogPageSEOForme(forms.ModelForm):
    class Meta:
        model = blogPageSEO
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'