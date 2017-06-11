from django import forms
#from django.contrib.auth.models import User
from .models import AjiraUser


class UploadPostForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.ImageField(label='Select an image')


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = AjiraUser
        fields = ['username', 'password']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = AjiraUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
