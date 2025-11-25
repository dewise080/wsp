from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from accounts.models import *

# # # # # # # # # # # # # # # # # #
    # User Profile Form #
# # # # # # # # # # # # # # # # # #
class UserProfileForm(forms.ModelForm):
    role = forms.ChoiceField(choices=get_user_model().Role.choices, required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs:
            user = kwargs['instance'].user
            self.fields['role'].initial = user.role
        self.fields['role'].choices = get_user_model().Role.choices

    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'name', 'slug', 'role', 'email', 'phone', 'address', 'city', 'state', 'country', 'zipcode', 'facebook', 'instagram', 'linkedin')
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'facebook': forms.TextInput(attrs={'class': 'form-control'}),
            'instagram': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            user = instance.user
            user.role = self.cleaned_data['role']
            user.save()
            instance.save()
        return instance

# # # # # # # # # # # # # # # # # #
    # User Creation Form #
# # # # # # # # # # # # # # # # # #
class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=255)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-select'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].choices = get_user_model().Role.choices

    class Meta:
        model = get_user_model()
        fields = ['name', 'username', 'password1', 'password2', 'email', 'role']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

# # # # # # # # # # # # # # # # # #
    # Password Form #
# # # # # # # # # # # # # # # # # #
class UserPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User