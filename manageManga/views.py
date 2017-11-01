from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Manga
from .forms import MangaRegistrationForm

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

class MangaFilterView(ListView):
    model = Manga
    template_name = 'manageManga/manga_list_filter.html'
    context_object_name = 'mangas_list'
    paginate_by = 5

    def get_queryset (self):
        query = super(MangaFilterView, self).get_queryset()
        search = self.request.GET.get('search', False)
        state = self.request.GET.get('state', False)
        genders = self.request.GET.get('genders', False)
        published_date = self.request.GET.get('published_date', False)
        print(query, search, state, genders, published_date)
        if state:
            try:
                state = int(state)
                query = query.filter(state__state = state)
            except Exception as e:
                query = query.filter(state__name = state)
        if genders:
            try:
                genders = int(genders)
                query = query.filter(genders__gender = genders)
            except Exception as e:
                query = query.filter(genders__name = genders)


        return query
    # def get_context_data(self, **kwargs):
    #     context = super(MyView, self).get_context_data(**kwargs)
    #     context['filter'] = self.request.GET.get('filter', 'give-default-value')
    #     context['orderby'] = self.request.GET.get('orderby', 'give-default-value')
    #     return context

    def get_context_data(self, **kwargs):
        context = super(MangaFilterView, self).get_context_data(**kwargs)
        print(context)
        # context['publisher'] = self.publisher
        return context
