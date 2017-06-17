from django import forms
#from django.contrib.auth.models import User
from .models import AjiraUser, Post, CareerInterests, JobTitle, Location


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


class UserAddCareerInterestsForm(forms.ModelForm):
    job_titles = forms.CharField(required=False)
    job_locations = forms.CharField(required=False)

    class Meta:
        model = CareerInterests
        fields = ['job_types', 'job_titles', 'job_locations']
        labels = {
            "job_titles": "What job titles are you considering?",
            "job_locations": "What locations would you work in?",
            "job_types": "What type of job are seeking?"
        }


class JobTitleForm(forms.ModelForm):
    title = forms.CharField(required=False)
    class Meta:
        model = JobTitle
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Job Title'}),
        }


class LocationForm(forms.ModelForm):
    name = forms.CharField(required=False)
    city = forms.CharField(required=False)
    region = forms.CharField(required=False)
    country = forms.CharField(required=False)

    class Meta:
        model = Location
        fields = ['name', 'city', 'region', 'country']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'region': forms.TextInput(attrs={'placeholder': 'Region'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
        }
