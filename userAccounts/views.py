"""Views from userAccounts app"""
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse

def validate_username(request):
    """ Ajax validate username """
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)

class SingUpView(CreateView):
    """SingUp View"""
    template_name = 'userAccounts/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('manageManga:list_of_mangas')

class LogInView(LoginView):
    """LogIn View"""
    template_name = 'userAccounts/login.html'

class LogOutView(LogoutView):
    """LogOut View"""
    pass
