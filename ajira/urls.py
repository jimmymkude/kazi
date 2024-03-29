
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

    # ajira/search_list
    url(r'^search_list/$', views.AjiraSearchListView.as_view(), name='ajira_search_list_view'),

    # ajira/add/post
    url(r'^add/post/$', views.PostCreateView.as_view(), name='add_post'),

    # ajira/pk/edit/posts
    url(r'^edit/posts/$', views.UserPostListView.as_view(), name='edit_posts'),

    # ajira/pk/edit/post
    url(r'^(?P<pk>[0-9]+)/edit/post/$', views.UserPostEditView.as_view(), name='edit_post'),

    # ajira/edit/post/pk/delete
    url(r'^edit/post/(?P<pk>[0-9]+)/delete/$', views.UserPostDeleteView.as_view(), name='delete_post'),

    # ajira/view/profile/3
    url(r'^view/profile/(?P<pk>[0-9]+)/$', views.UserProfileView.as_view(), name='view_profile'),

    # ajira/edit/profile/3
    url(r'^edit/profile/(?P<pk>[0-9]+)/$', views.UserProfileEditView.as_view(), name='edit_profile'),

    # ajira/view/resume
    url(r'^view/resume/(?P<pk>[0-9]+)$', views.view_resume, name='view_resume'),

    # ajira/career-interests
    url(r'^career-interests/(?P<pk>[0-9]+)/$', views.AddCareerInterests.as_view(), name='career_interests'),

    # ajira/login
    url(r'^login/$', views.UserLoginFormView.as_view(), name='login'),

    # ajira/logout
    url(r'^logout/$', views.logout_view, name='logout'),


    # REST API URLs
    url(r'^api/posts', views.PostAPIView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)

