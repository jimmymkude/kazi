from django.db import models
from django import forms
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, UserManager

# Create your models here.

class JobTitle(models.Model):
    title = models.CharField(name="title", max_length=60)
    title_lower = models.CharField(name="title_lower", max_length=60, default="n/a")

    def __str__(self):
        return "Job Title: {}".format(self.title)

    def is_valid(self):
        return self.title != ""


class Location(models.Model):
    name = models.CharField(name="name", max_length=100)
    city = models.CharField(name="city", max_length=100)
    region = models.CharField(name="region", max_length=100)
    country = models.CharField(name="country", max_length=100)

    def __str__(self):
        return "Name: {}, City: {}, Region: {}, Country: {}".format(self.name, self.city, self.region, self.country)

    def is_valid(self):
        return self.region != "" and self.country != ""


class CareerInterests(models.Model):
    FULLTIME = 'FT'
    PARTTIME = 'PT'
    INTERNSHIP = 'IN'
    TENDA = 'T'

    JOB_TYPE_CHOICES = (
        (FULLTIME, 'Full-time'),
        (PARTTIME, 'Part-time'),
        (INTERNSHIP, 'Internship'),
        (TENDA, 'Tenda/Contract'),
    )
    # job title user is considering
    job_titles = models.ManyToManyField(JobTitle)
    job_locations = models.ManyToManyField(Location)
    job_types = models.CharField(max_length=10, choices=JOB_TYPE_CHOICES, default=FULLTIME)

    def __str__(self):
        return ("( Job Titles: {} Job Locations: {} Job Types: {})".format(self.job_titles, self.job_locations, self.job_types))


class AjiraUser(User):
    #first_name = models.CharField(max_length=50)
    middle_initial = models.CharField(default='', max_length=1)
    #last_name = models.CharField(max_length=50)
    #email = models.EmailField(name="email")
    #password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    job_title = models.CharField(max_length=50, default="N/A")
    company_name = models.CharField(max_length=30, default="N/A")
    resume = models.FileField(name="resume", max_length=50, default="No resume uploaded", upload_to='media/resumes/%Y/%m/%d')
    career_interests = models.ForeignKey(CareerInterests, on_delete=models.CASCADE, null=True)
    # Use UserManager to get the create_user method, etc.
    objects = UserManager()


    def __str__(self):
        return self.last_name + ", " + self.first_name + " " + self.middle_initial


class Post(models.Model):
    image = models.ImageField(name="image", upload_to='media/%Y/%m/%d')
    title = models.CharField(name="title", max_length=60)
    title_lower = models.CharField(name="title_lower", max_length=60, default="n/a")
    description = models.TextField(name="description", max_length=1000)
    link = models.CharField(name="link", max_length=200)
    company = models.CharField(name="company", default="N/A", max_length=30)
    active_days = models.IntegerField(name='lifetime_in_days', default=30)

    user = models.ForeignKey(AjiraUser, on_delete=models.CASCADE)

    def get_absolute_url(self):
        reverse('ajira:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title + " from " + self.company























