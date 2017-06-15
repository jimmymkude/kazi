from django import forms
#from django.contrib.auth.models import User
from .models import AjiraUser, Post


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'description', 'company', 'link', 'lifetime_in_days', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post Title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description...(max 1000 characters).'}),
            'company': forms.TextInput(attrs={'placeholder': 'Company'}),
            'link': forms.TextInput(attrs={'placeholder': 'Job url'}),
        }


class PostEditForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'description', 'company', 'link', 'lifetime_in_days', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post Title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description...(max 1000 characters).'}),
            'company': forms.TextInput(attrs={'placeholder': 'Company'}),
            'link': forms.TextInput(attrs={'placeholder': 'Job url'}),
        }


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = AjiraUser
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
        }


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = AjiraUser
        fields = ['first_name', 'last_name',  'email', 'username', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
        }


class UserEditProfileForm(forms.ModelForm):

    class Meta:
        model = AjiraUser
        fields = ['first_name', 'last_name', 'email', 'job_title', 'company_name', 'resume']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
            'job_title': forms.TextInput(attrs={'placeholder': 'Job Title'}),
            'company_name': forms.TextInput(attrs={'placeholder': 'Company Name'}),
        }
