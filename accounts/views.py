from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    LoginView,
    LogoutView
    )

from .forms import SignUpForm

class RedirectAuthenticatedUser:
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super(RedirectAuthenticatedUser, self).dispatch(request, *args, **kwargs)

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

class MyLogoutView(LogoutView):
    next_page = '/'

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
