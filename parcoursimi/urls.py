from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from parcoursimi import views

# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^courses/$',
        views.CoursesList.as_view(),
        name='courses-list'),
    url(r'^option/$',
        views.OptionList.as_view(),
        name='option-list'),
    url(r'^userprofile/$',
        views.UserProfileList.as_view(),
        name='userprofile-list'),
    url(r'^master/$',
        views.MasterList.as_view(),
        name='master-list'),
    url(r'^master/(?P<pk>[0-9]+)/$',
        views.MasterDetail.as_view(),
        name='master-detail'),
    url(r'^users/(?P<pk>[0-9]+)/$',
        views.UserProfileDetail.as_view(),
        name='userprofile-detail'),
    url(r'^courses/(?P<pk>[0-9]+)/$',
        views.CoursesDetail.as_view(),
        name='courses-detail'),
    url(r'^$', views.api_root),
])
