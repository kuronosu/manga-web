"""Views: Create your views here."""
from django.http import HttpResponseRedirect, HttpResponse #, HttpResponseNotFound
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
    ModelFormMixin,
    ProcessFormView
    )
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404

from .models import Manga, Chapter, Voto
from .funct import filter_obj_model
from .mixins import (
    FilterMixin,
    StaffFormsMixin,
    UserPermissionsMixin,
    ExtraContextMixin,
    ChapterAddMixin
    )
from .forms import (
    FilterForm,
    SearchForm,
    MangaRegistrationForm,
    MangaEditForm,
    ChapterRegistrationForm,
    VoteMangaForm,
    )
# Staff forms
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

class MangaDetailView(ExtraContextMixin, DetailView):
    """Vista de detalles de los mangas"""
    model = Manga
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True
    template_name = 'manageManga/manga_detail.html'
    extra_context = {
        'chapters': ['filter', Chapter, {'manga__id': 'id'}],
        'frontend_permission': ['frontend_permission'],
        'vote_form': ['vote_form', VoteMangaForm]
    }

    def get_context_data(self, **kwargs):
        context = super(MangaDetailView, self).get_context_data(**kwargs)
        if 'form_vote_files' not in context:
            context['form_vote_files'] = list(range(1,11))
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

class VoteView(LoginRequiredMixin, ModelFormMixin, ProcessFormView):
    """ Vista para manejar los votos de un manga """
    model = Voto
    form_class = VoteMangaForm
    login_url = reverse_lazy('userAccounts:login')

    def post(self, request, *args, **kwargs):
        votos = filter_obj_model(
            Voto,
            manga__slug=kwargs['manga_slug'], author__id=self.request.user.id
            )
        if len(votos) < 1:
            self.object = None
        else:
            self.object = get_object_or_404(
                Voto,
                manga__slug=kwargs['manga_slug'], author__id=self.request.user.id
                )
        return super(VoteView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponse('Invalid Method')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.manga = get_object_or_404(Manga, slug=self.kwargs['manga_slug'])
        return super(VoteView, self).form_valid(form)

    def form_invalid(self, form):
        return HttpResponseRedirect(
            reverse_lazy('manageManga:manga_detail', kwargs={'slug': self.kwargs['manga_slug']})
            )

"""
Vistas de los capitulos
"""

class ChapterAddView(LoginRequiredMixin, ChapterAddMixin, UserPermissionsMixin, CreateView):
    """Vista de para crear un capitulo de un manga"""
    login_url = reverse_lazy('userAccounts:login')
    model = Chapter
    template_name_suffix = '_add'
    form_class = ChapterRegistrationForm
    permissions_slug_url_kwarg = 'manga_slug'
    permissions_model = Manga

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

    def get_queryse(self):
        query = super(ProfileView, self).get_queryset()
        eventos_usuario = query.filter(author=self.request.user)
        return eventos_usuario
