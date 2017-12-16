"""Urls del app manageManga"""
from django.contrib.auth.views import login, logout
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/', login, name='login'),
    url(r'^logout/', logout, name='logout'),
    url(
        r'^singup/$', views.SingUpView.as_view(),
        name='singup'
    ),
    url(
        r'^ajax/validate_username/$',
        views.validate_username,
        name='validate_username'
    ),
]
