from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

class SingUpView(CreateView):
    """SingUp View"""
    template_name = 'accounts/singup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('manageManga:list_of_mangas')

    def form_valid(self, form):
        self.object = form.save()
        password = form.cleaned_data.get('password1')
        username = form.cleaned_data.get('username')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        next_page= self.request.GET.get('next', None)
        if next_page:
            return HttpResponseRedirect(next_page)
        return HttpResponseRedirect(self.get_success_url())
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super(SingUpView, self).dispatch(request, *args, **kwargs)
