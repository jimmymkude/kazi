from django.db import models
from django import forms
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# Create your models here.


class AjiraUser(User):
    #first_name = models.CharField(max_length=50)
    middle_initial = models.CharField(default='', max_length=1)
    #last_name = models.CharField(max_length=50)
    #email = models.EmailField(name="email")
    #password = forms.CharField(max_length=32, widget=forms.PasswordInput)

    def __str__(self):
        return self.last_name + ", " + self.first_name + " " + self.middle_initial


class Post(models.Model):
    image = models.ImageField(name="image", upload_to='media/%Y/%m/%d')
    title = models.CharField(name="title", max_length=50)
    description = models.TextField(name="description", max_length=1000)
    link = models.CharField(name="link", max_length=200)
    company = models.CharField(name="company", default="N/A", max_length=50)
    active_days = models.IntegerField(name='lifetime_in_days', default=30)

    user = models.ForeignKey(AjiraUser, on_delete=models.CASCADE)

    def get_absolute_url(self):
        reverse('ajira:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title + " from " + self.company



