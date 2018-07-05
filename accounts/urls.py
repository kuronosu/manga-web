from django.contrib.auth.views import logout
from django.urls import path
from django.urls import reverse_lazy

from .views import SingUpView, MyLoginView, MyPasswordResetView, MyPasswordResetDoneView, MyPasswordResetConfirmView

app_name = 'accounts'

urlpatterns = [
    path('login', MyLoginView.as_view(), name = 'login'),
    path('logout', logout, {'next_page': '/'}, name = 'logout'),
    path('singup', SingUpView.as_view(), name='singup'),
    path('password/reset', MyPasswordResetView.as_view(), name="password_reset"),
    path('password/complete', MyPasswordResetDoneView.as_view(), name = 'password_reset_done'),
    path('password/reset/confirm/<str:uidb64>/<str:token>', MyPasswordResetConfirmView.as_view(), name = 'password_reset_confirm')
]
