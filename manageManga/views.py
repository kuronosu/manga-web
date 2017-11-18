"""Views: Create your views here."""
# from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
# from django.http import Http404
from django.views.generic import ListView, DetailView # View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView #, FormView
# from django.views.generic.edit import FormMixin
from django.template import loader
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.utils.decorators import method_decorator
# from django.utils.translation import ugettext_lazy as _
# from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404

from .models import Manga, Chapter
from .forms import MangaRegistrationForm, FilterForm, SearchForm, ChapterRegistrationForm

class HomeView(TemplateView):
    """Vista del home"""
    template_name = "home.html"

class MangaListAndFilterView(ListView):
    """Vista para listar y filtrar mangas"""
    model = Manga
    template_name = 'manageManga/manga_list.html'
    context_object_name = 'mangas_list'
    paginate_by = 5
    form_classes = {
        'filter_form': FilterForm,
        'search_form': SearchForm
    }

    def get_queryset(self):
        query = super(MangaListAndFilterView, self).get_queryset()
        search = self.request.GET.get('search', False)
        state = self.request.GET.get('state', False)
        genres = self.request.GET.getlist('genres', False)
        published_date = self.request.GET.get('published_date', False)
        if search:
            query = query.filter(title__icontains=search)
        if state:
            try:
                query = query.filter(state__state=int(state))
            except Exception:
                query = query.filter(state__name=state)
        if genres:
            try:
                query = query.filter(genres__genre__in=genres)
                query = list(set(query))
            except Exception:
                query = query.filter(genres__name__in=genres)
        return query

    def get_context_data(self, **kwargs):
        context = super(MangaListAndFilterView, self).get_context_data(**kwargs)
        if 'filter_form' not in context:
            context['filter_form'] = self.form_classes['filter_form']()
        if 'search_form' not in context:
            context['search_form'] = self.form_classes['search_form'](initial={'slug': ''})
        return context

    def form_invalid(self, **kwargs):
        """form invalid method"""
        return self.render_to_response(self.get_context_data(**kwargs))

class MangaDetailView(DetailView):
    """Vista de detalles de los mangas"""
    model = Manga
    pk_url_kwarg = 'manga_id'
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True
    template_name = 'manageManga/manga_detail.html'

    def get_context_data(self, **kwargs):
        context = super(MangaDetailView, self).get_context_data(**kwargs)
        manga = self.object
        if 'chapters' not in context:
            querry = Chapter.objects.all()
            querry = querry.filter(manga__author__id=manga.id)
            print(querry)
            context['chapters'] = querry
        return context

    def get_queryset(self):
        query = super(MangaDetailView, self).get_queryset()
        return query.filter()

#Vista MangaAddView creada con clases heredando de CreateView
class MangaAddView(LoginRequiredMixin, CreateView):
    """Vista de para crear un manga"""
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
    """Vista de para crear un chapitulo de un manga"""
    login_url = '/login'
    model = Chapter
    template_name = 'manageManga/chapter_add.html'
    form_class = ChapterRegistrationForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        manga_id = self.kwargs['manga_id']
        manga = get_object_or_404(Manga, id=manga_id)
        if manga:
            if manga.author.id == self.request.user.id:
                return super(ChapterAddView, self).get(request)
            else:
                template = loader.get_template('manageManga/restricted_access.html')
                context = {}
                return HttpResponse(template.render(context, request))

    def post(self, request, *args, **kwargs):
        manga_id = self.kwargs['manga_id']
        manga = get_object_or_404(Manga, id=manga_id)
        if manga:
            if manga.author.id == self.request.user.id:
                return super(ChapterAddView, self).post(request)
            else:
                template = loader.get_template('manageManga/restricted_access.html')
                context = {}
                return HttpResponse(template.render(context, request))


    def form_valid(self, form):
        manga_id = self.kwargs['manga_id']# forma de obtener el id
        manga = Manga.objects.get(id=manga_id)
        form.instance.manga = manga
        form.instance.owner = self.request.user
        self.object = form.save()
        manga.add_chapter(self.object.id)
        return HttpResponseRedirect(self.get_success_url())

class ProfileView(ListView):
    """Vista para los mangas del usuario logeado"""
    model = Manga
    template_name = 'manageManga/manga_list.html'
    context_object_name = 'mangas_list'

    def get_queryset(self):
        query = super(ProfileView, self).get_queryset()
        eventos_usuario = query.filter(author=self.request.user)
        return eventos_usuario
