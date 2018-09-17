from django import forms
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import  get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserCreationForm
)

UserModel = get_user_model()


class SignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('username', 'email', 'password1', 'password2', )

class AuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=None, *args, **kwargs)
        self.fields['username'].label = capfirst(_('Username or Email'))
    
    @property
    def username_placeholder(self):
        return capfirst(_('Enter your Username or Email'))
