
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
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
    # ajira/login
    url(r'^login/$', views.UserLoginFormView.as_view(), name='login'),
    # ajira/logout
    url(r'^logout/$', views.logout_view, name='logout'),

    # REST API URLs
    url(r'^api/posts', views.PostAPIView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)

