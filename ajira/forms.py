from django import forms
from django.contrib.auth.models import User


class UploadPostForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.ImageField(label='Select an image')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
