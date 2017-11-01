from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.edit import FormMixin
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Manga
from .forms import MangaRegistrationForm, FilterForm
from .validations import max_genders

class HomeView(TemplateView):
    template_name = "home.html"

class MangaListView(ListView):
    model = Manga
    template_name = 'manageManga/manga_list.html'
    context_object_name = 'mangas_list'
    paginate_by = 5

class MangaDetailView(DetailView):
    model = Manga
    pk_url_kwarg = 'manga_id'
    slug_url_kwarg = 'slug'
    template_name = 'manageManga/manga_detail.html'

    def get_queryset(self):
        query = super(MangaDetailView, self).get_queryset()
        return query.filter()

#Vista MangaAddView creada con clases heredando de CreateView
class MangaAddView(LoginRequiredMixin, CreateView):
    login_url = '/admin/login'
    model = Manga
    template_name = 'manageManga/manga_add.html'
    form_class = MangaRegistrationForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()

        return HttpResponseRedirect(self.get_success_url())

class MangaFilterView(FormMixin, ListView):
    model = Manga
    template_name = 'manageManga/manga_list_filter.html'
    context_object_name = 'mangas_list'
    paginate_by = 5
    form_class = FilterForm

    def get_queryset (self):
        query = super(MangaFilterView, self).get_queryset()
        search = self.request.GET.get('search', False)
        state = self.request.GET.get('state', False)
        genders = self.request.GET.getlist('genders', False)
        published_date = self.request.GET.get('published_date', False)
        if state:
            try:
                query = query.filter(state__state = int(state))
            except Exception as e:
                query = query.filter(state__name = state)
        if genders:
            # max_genders(genders)
            try:
                query = query.filter(genders__gender__in = genders)
                query = list(set(query))
            except Exception as e:
                query = query.filter(genders__name__in = genders)

        return query

    def get_context_data(self, **kwargs):
        context = super(MangaFilterView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
