from django import forms
#from django.contrib.auth.models import User
from .models import AjiraUser, Post


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['image', 'title', 'description', 'link', 'company', 'lifetime_in_days']


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
