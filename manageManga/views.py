"""Views: Create your views here."""
# from django.http import HttpResponse#, HttpResponseRedirect# , HttpResponseNotFound
from django.views.generic import ListView, DetailView # View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404

from .models import Manga, Chapter
from .mixins import FilterMixin, StaffFormsMixin, UserPermissionsMixin
from .forms import (
    FilterForm,
    SearchForm,
    MangaRegistrationForm,
    MangaEditForm,
    ChapterRegistrationForm,
    )
#Staff forms
from .forms import (
    StaffMangaEditForm
    )

class My404(TemplateView):
    """Vista del error 404"""
    template_name = "404.html"

class HomeView(TemplateView):
    """Vista del home"""
    template_name = "home.html"

"""
Vistas de los mangas
"""
class MangaListAndFilterView(FilterMixin, ListView):
    """Vista para listar y filtrar mangas"""
    model = Manga
    template_name = 'manageManga/manga_list.html'
    context_object_name = 'mangas_list'
    paginate_by = 5
    form_classes = {
        'filter_form': FilterForm,
        'search_form': SearchForm
    }

class MangaAddView(LoginRequiredMixin, CreateView):
    """Vista de para crear un manga"""
    login_url = reverse_lazy('userAccounts:login')
    model = Manga
    template_name = 'manageManga/manga_add.html'
    form_class = MangaRegistrationForm
    # success_url = reverse_lazy('manageManga:list_of_mangas')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(MangaAddView, self).form_valid(form)

class MangaDetailView(DetailView):
    """Vista de detalles de los mangas"""
    model = Manga
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True
    template_name = 'manageManga/manga_detail.html'

    def get_context_data(self, **kwargs):
        context = super(MangaDetailView, self).get_context_data(**kwargs)
        manga = self.object
        if 'chapters' not in context:
            chapters = Chapter.objects.all()
            query = chapters.filter(manga__id=manga.id)
            context['chapters'] = query
        if 'add' not in context:
            if manga.author.id == self.request.user.id or self.request.user.is_staff:
                context['add'] = True
            else:
                context['add'] = False
        return context

class MangaUpdateView(LoginRequiredMixin, UserPermissionsMixin, StaffFormsMixin, UpdateView):
    """Vista de para actualizar un manga"""
    login_url = reverse_lazy('userAccounts:login')
    model = Manga
    form_class = MangaEditForm
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True
    template_name_suffix = '_update'
    staff_form = StaffMangaEditForm
    permissions_slug_url_kwarg = 'slug'
    permissions_model = Manga

class MangaDeleteView(LoginRequiredMixin, UserPermissionsMixin, DeleteView):
    """Vista de para eliminar un manga"""
    login_url = reverse_lazy('userAccounts:login')
    model = Manga
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True
    success_url = reverse_lazy('manageManga:list_of_mangas')
    permissions_slug_url_kwarg = 'slug'
    permissions_model = Manga

"""
Vistas de los capitulos
"""

class ChapterAddView(LoginRequiredMixin, UserPermissionsMixin, CreateView):
    """Vista de para crear un capitulo de un manga"""
    login_url = reverse_lazy('userAccounts:login')
    model = Chapter
    template_name_suffix = '_add'
    form_class = ChapterRegistrationForm
    permissions_slug_url_kwarg = 'manga_slug'
    permissions_model = Manga

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        ###
        Y verifica si se crea un capitulo referenciado a un manga con un
        numero de capitulo repetido.
        """
        form = self.get_form()
        manga = get_object_or_404(Manga, slug=self.kwargs['manga_slug'])
        try:
            chapters = Chapter.objects.all().filter(manga__id=manga.id)
            user_chapter_number = int(self.get_form_kwargs()['data']['user_chapter_number'])
            for i in chapters:
                if i.user_chapter_number == user_chapter_number:
                    form.add_error('user_chapter_number', _('Chapter number not available'))
        except ValueError:
            form.add_error('user_chapter_number', _('Error interno.'))

        self.object = None
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        manga_slug = self.kwargs['manga_slug']
        manga = get_object_or_404(Manga, slug=manga_slug)
        form.instance.manga = manga
        form.instance.author = self.request.user
        return super(ChapterAddView, self).form_valid(form)

class ChapterDetailView(DetailView):
    """Vista de detalles de los mangas"""
    model = Chapter
    pk_url_kwarg = 'chapter_id'
    template_name_suffix = '_detail'
    slug_url_kwarg = 'chapter_slug'
    query_pk_and_slug = True

    def get_object(self, queryset=None):
        manga_slug = self.kwargs['manga_slug']
        chapter_slug = self.kwargs['chapter_slug']
        manga = get_object_or_404(Manga, slug=manga_slug)
        queryset = self.get_queryset().filter(manga__id=manga.id).filter(slug=chapter_slug)
        return super(ChapterDetailView, self).get_object(queryset=queryset)

class ProfileView(ListView):
    """Vista para los mangas del usuario logeado"""
    model = Manga
    template_name = 'manageManga/manga_list_filter.html'
    context_object_name = 'mangas_list'

    def get_queryset(self):
        query = super(ProfileView, self).get_queryset()
        eventos_usuario = query.filter(author=self.request.user)
        return eventos_usuario
