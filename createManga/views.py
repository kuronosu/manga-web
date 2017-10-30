from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Manga
from .forms import MangaRegistrationForm

class HomeView(TemplateView):
    template_name = "home.html"

class MangaListView(ListView):
    model = Manga
    template_name = 'createManga/manga_list.html'
    context_object_name = 'mangas_list'
    paginate_by = 5

class MangaDetailView(DetailView):
    model = Manga
    pk_url_kwarg = 'manga_id'
    slug_url_kwarg = 'slug'
    template_name = 'createManga/manga_detail.html'

    def get_queryset(self):
        query = super(MangaDetailView, self).get_queryset()
        return query.filter()

#Vista MangaAddView creada con clases heredando de CreateView
class MangaAddView(LoginRequiredMixin, CreateView):
    login_url = '/admin/login'
    model = Manga
    template_name = 'createManga/manga_add.html'
    form_class = MangaRegistrationForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()

        return HttpResponseRedirect(self.get_success_url())
