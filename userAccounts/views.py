"""Views from userAccounts app"""
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from .mixins import AjaxableResponseMixin
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

class SingUpView(AjaxableResponseMixin, CreateView):
    """SingUp View"""
    template_name = 'core/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('manageManga:list_of_mangas')