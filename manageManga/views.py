from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.views.generic import View, ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.edit import FormMixin
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from .models import Manga, Chapter
from .forms import MangaRegistrationForm, FilterForm, SearchForm, ChapterRegistrationForm

class HomeView(TemplateView):
    template_name = "home.html"

class MangaListAndFilterView(ListView):
    model = Manga
    template_name = 'manageManga/manga_list.html'
    context_object_name = 'mangas_list'
    paginate_by = 5
    form_classes = {
        'filter_form': FilterForm,
        'search_form': SearchForm
    }

    def get_queryset (self):
        query = super(MangaListAndFilterView, self).get_queryset()
        search = self.request.GET.get('search', False)
        state = self.request.GET.get('state', False)
        genres = self.request.GET.getlist('genres', False)
        published_date = self.request.GET.get('published_date', False)
        if search:
            query = query.filter(title__icontains = search)
        if state:
            try:
                query = query.filter(state__state = int(state))
            except Exception as e:
                query = query.filter(state__name = state)
        if genres:
            try:
                query = query.filter(genres__genre__in = genres)
                query = list(set(query))
            except Exception as e:
                query = query.filter(genres__name__in = genres)
        return query

    def get_context_data(self, **kwargs):
        context = super(MangaListAndFilterView, self).get_context_data(**kwargs)
        if 'filter_form' not in context:
            context['filter_form'] = self.form_classes['filter_form']()
        if 'search_form' not in context:
            context['search_form'] = self.form_classes['search_form'](initial={'slug': ''})
        return context

    def  form_invalid ( self , ** kwargs ):
        return  self .render_to_response ( self .get_context_data ( ** kwargs))

class MangaDetailView(DetailView):
    model = Manga
    pk_url_kwarg = 'manga_id'
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True
    template_name = 'manageManga/manga_detail.html'

    def get_queryset(self):
        query = super(MangaDetailView, self).get_queryset()
        return query.filter()

#Vista MangaAddView creada con clases heredando de CreateView
class MangaAddView(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Manga
    template_name = 'manageManga/manga_add.html'
    form_class = MangaRegistrationForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()
        
        return HttpResponseRedirect(self.get_success_url())


class ChapterAddView(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Chapter
    template_name = 'manageManga/chapter_add.html'
    form_class = ChapterRegistrationForm
    success_url = '/'

    def form_valid(self, form):
        manga_id = self.kwargs['manga_id']# forma de obtener el id # forma de obtener el id
        form.instance.manga = Manga.objects.get(id=manga_id)
        form.instance.owner = self.request.user
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

class ProfileView(ListView):
    model = Manga
    template_name = 'manageManga/manga_list.html'
    context_object_name = 'mangas_list'

    def get_queryset(self):
        query = super(ProfileView, self).get_queryset()
        eventos_usuario = query.filter(author = self.request.user)
        return eventos_usuario
