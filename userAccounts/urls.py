"""Urls del app userAccounts"""
from django.conf.urls import url
from . import views

app_name = 'userAccounts'

urlpatterns = [
    url('login/', views.LogInView.as_view(), name='login'),
    url('logout/', views.LogOutView.as_view(), name='logout'),
    url(
        'singup/', views.SingUpView.as_view(),
        name='singup'
    )
]
