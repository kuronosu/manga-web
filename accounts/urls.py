from django.contrib.auth.views import login, logout
from django.urls import path

from .views import SingUpView

app_name = 'accounts'

urlpatterns = [
    path('login', login, {'template_name': 'accounts/login.html'}, name = 'login'),
    path('logout', logout, {'next_page': '/'}, name = 'logout'),
    path('singup', SingUpView.as_view(), name='singup')
]