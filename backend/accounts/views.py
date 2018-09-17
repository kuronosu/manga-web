from django.contrib.auth import authenticate, login, get_user_model
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.text import capfirst
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    LoginView,
    LogoutView
    )

from .forms import SignUpForm, AuthenticationForm

User = get_user_model()

class RedirectAuthenticatedUser:
    def dispatch(self, request, *args, **kwargs):
        if hasattr(self, 'request'):
            if self.request.user.is_authenticated: # pylint: disable=E1101
                return HttpResponseRedirect('/')
        return super(RedirectAuthenticatedUser, self).dispatch(request, *args, **kwargs) # pylint: disable=E1101

class SingUpView(RedirectAuthenticatedUser, CreateView):
    """SingUp View"""
    template_name = 'accounts/singup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('manageManga:list_of_mangas')

    def form_valid(self, form):
        self.object = form.save()
        password = form.cleaned_data.get('password1')
        username = form.cleaned_data.get('username')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        next_page = self.request.GET.get('next', self.request.POST.get('next', None))
        if next_page:
            return HttpResponseRedirect(next_page)
        return HttpResponseRedirect(self.get_success_url())
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super(SingUpView, self).dispatch(request, *args, **kwargs)

class MyLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    form_class = AuthenticationForm

class MyPasswordResetView(RedirectAuthenticatedUser, PasswordResetView):
    email_template_name = 'accounts/password_reset_email.html'
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')

class MyPasswordResetDoneView(RedirectAuthenticatedUser, PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class MyPasswordResetConfirmView(RedirectAuthenticatedUser, PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:login')
    post_reset_login = True


class ProfileView(DetailView):
    model = User
    template_name = 'accounts/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'userObject'

    # def get_context_object_name