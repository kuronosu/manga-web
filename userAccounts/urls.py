"""Urls del app userAccounts"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/', views.LogInView.as_view(), name='login'),
    url(r'^logout/', views.LogOutView.as_view(), name='logout'),
    url(
        r'^singup/$', views.SingUpView.as_view(),
        name='singup'
    )
]
