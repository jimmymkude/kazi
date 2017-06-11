
from django.conf.urls import url
from ajira import views

app_name = 'ajira'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ajira/register
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    # ajira/about
    url(r'^about/$', views.AboutPageView.as_view(), name='about'),
    # ajira/3
    url(r'^(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    # ajira/add/post
    url(r'^add/post/$', views.PostCreateView.as_view(), name='add_post'),
    # ajira/3/upload
    url(r'^(?P<pk>[0-9]+)/upload/$', views.upload_file, name='upload_post')
]
