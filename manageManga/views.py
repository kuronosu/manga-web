"""Views: Create your views here."""
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
    ModelFormMixin,
    ProcessFormView,
    BaseDetailView,
    )
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from .models import Manga, Chapter, Voto, Tomo
from .funct import filter_obj_model, frontend_permission
from .mixins import (
    FilterMixin,
    StaffFormsMixin,
    UserPermissionsMixin,
    ChapterAddMixin,
    TomoAddMixin
    )
from .forms import (
    FilterForm,
    SearchForm,
    MangaRegistrationForm,
    MangaEditForm,
    ChapterRegistrationForm,
    VoteMangaForm,
    TomoCreationForm
    )
# Staff forms
from .forms import (
    StaffMangaEditForm,
    StaffTomoEditForm
    )

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
        self.object = form.save()
        tomo = TomoCreationForm({'number':-1})
        tomo.instance.manga = self.object
        tomo.instance.author = self.request.user
        tomo.save()
        return HttpResponseRedirect(self.get_success_url())

class MangaDetailView(DetailView):
    """Vista de detalles de los mangas"""
    model = Manga
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True
    template_name = 'manageManga/manga_detail.html'

    def dispatch(self, request, *args, **kwargs):
        manga = self.get_object()
        user_access = ((manga.author.id == self.request.user.id) or self.request.user.is_staff)
        if not (manga.verify or user_access):
            return HttpResponse('Este manga aun no se verifica.')
        return super(MangaDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MangaDetailView, self).get_context_data(**kwargs)
        if 'form_vote_files' not in context:
            context['form_vote_files'] = list(range(1, 11))
        if 'tomos' not in context:
            tomos = filter_obj_model(Tomo, manga=self.object)
            context['tomos'] = tomos
        if 'vote_form' not in context:
            try:
                vote_object = get_object_or_404(Voto ,manga=self.object,author=self.request.user)
                context['vote_form'] = VoteMangaForm(dict(vote_value=vote_object.vote_value))
            except:
                context['vote_form'] = VoteMangaForm()
        if 'frontend_permission' not in context:
            context['frontend_permission'] = frontend_permission(self)

        puntaje = str(round(context['manga'].puntaje, 2)).replace(',', '.')
        context['manga'].puntaje = puntaje
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
Vistas de los votos
"""

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
        self.object = form.save()
        manga = get_object_or_404(Manga, slug=self.kwargs['manga_slug'])
        vote_value = self.object.vote_value
        puntaje = manga.puntaje
        return JsonResponse({
            'state': True,
            'vote_value': vote_value,
            'puntaje': puntaje,
            })

    def form_invalid(self, form):
        return JsonResponse({'state': False})

"""
Vistas de los tomos
"""

class TomoAddView(LoginRequiredMixin, TomoAddMixin, UserPermissionsMixin, CreateView):
    """Vista de para crear un tomo de un manga"""
    login_url = reverse_lazy('userAccounts:login')
    model = Tomo
    template_name_suffix = '_add'
    form_class = TomoCreationForm
    permissions_slug_url_kwarg = 'manga_slug'
    permissions_model = Manga

    def get_permissions_object(self, *args, **kwargs):
        slug = self.kwargs[self.permissions_slug_url_kwarg]
        manga = get_object_or_404(self.permissions_model, slug=slug)
        return manga

    def post(self, request, *args, **kwargs):
        self.object = None
        return super(TomoAddView, self).post(request, *args, **kwargs)

class TomoDetailView(BaseDetailView):
    """
    Vista para mostrar los detalles de un tomo, incluyendo los capitulos asociados a él
    """
    model = Tomo

    def get(self, request, *args, **kwargs):
        raise Http404('No se puede acceder por get')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        chapters_query = filter_obj_model(Chapter, tomo=self.object)
        chapters = []
        for i in chapters_query:
            data_kwargs = {
                'manga_slug': self.object.manga.slug,
                'tomo_number': self.object.number,
                'chapter_slug': i.slug
                }
            url = reverse_lazy('manageManga:chapter_detail', kwargs=data_kwargs)
            chapters.append({
                'number': i.user_chapter_number,
                'name': i.name,
                'url': url
                })
        url_add = reverse_lazy('manageManga:chapter_add', kwargs={
            'manga_slug': self.object.manga.slug,
            'tomo_number': self.object.number,
            })
        context = {
            'chapters': chapters,
            'url_add': url_add
        }
        return JsonResponse(context)

    def get_object(self, queryset=None):
        manga_slug = self.kwargs['manga_slug']
        tomo_number = self.kwargs['tomo_number']
        try:
            tomo_number = int(tomo_number)
        except Exception:
            raise Http404()
        manga = get_object_or_404(Manga, slug=manga_slug)
        tomo = get_object_or_404(Tomo, number=tomo_number, manga=manga)
        return tomo

class TomoUpdateView(LoginRequiredMixin, UserPermissionsMixin, TomoAddMixin, UpdateView):
    """Vista de para actualizar un tomo de un manga"""
    login_url = reverse_lazy('userAccounts:login')
    model = Tomo
    form_class = TomoCreationForm
    template_name_suffix = '_update'
    staff_form = StaffTomoEditForm
    permissions_slug_url_kwarg = 'manga_slug'
    permissions_model = Manga

    def get_permissions_object(self, *args, **kwargs):
        slug = self.kwargs[self.permissions_slug_url_kwarg]
        manga = get_object_or_404(self.permissions_model, slug=slug)
        return manga

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(TomoUpdateView, self).post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        manga_slug = self.kwargs['manga_slug']
        tomo_number = self.kwargs['tomo_number']
        try:
            tomo_number = int(tomo_number)
        except Exception:
            raise Http404()
        manga = get_object_or_404(Manga, slug=manga_slug)
        tomo = get_object_or_404(Tomo, number=tomo_number, manga=manga)
        return tomo

class TomoDeleteView(LoginRequiredMixin, UserPermissionsMixin, DeleteView):
    model = Tomo
    login_url = reverse_lazy('userAccounts:login')
    success_url = reverse_lazy('manageManga:list_of_mangas')
    permissions_slug_url_kwarg = 'manga_slug'
    permissions_model = Manga

    def get_object(self, queryset=None):
        manga_slug = self.kwargs['manga_slug']
        tomo_number = self.kwargs['tomo_number']
        try:
            tomo_number = int(tomo_number)
        except Exception:
            raise Http404()
        manga = get_object_or_404(Manga, slug=manga_slug)
        tomo = get_object_or_404(Tomo, number=tomo_number, manga=manga)
        return tomo
    
    def get_permissions_object(self, *args, **kwargs):
        slug = self.kwargs[self.permissions_slug_url_kwarg]
        manga = get_object_or_404(self.permissions_model, slug=slug)
        return manga

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

    def dispatch(self, request, *args, **kwargs):
        manga_slug = self.kwargs['manga_slug']
        tomo_number = self.kwargs['tomo_number']
        try:
            tomo_number = int(tomo_number)
        except Exception:
            raise Http404()
        manga = get_object_or_404(Manga, slug=manga_slug)
        queryset = filter_obj_model(Tomo, number=tomo_number, manga__id=manga.id)
        try:
            queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No coincide el tomo del manga y el manga peroporcionado")
        return super(ChapterAddView, self).dispatch(request, *args, **kwargs)
    
    def get_permissions_object(self, *args, **kwargs):
        slug = self.kwargs[self.permissions_slug_url_kwarg]
        manga = get_object_or_404(self.permissions_model, slug=slug)
        return manga

    def post(self, request, *args, **kwargs):
        self.object = None
        return super(ChapterAddView, self).post(request, *args, **kwargs)

class ChapterDetailView(DetailView):
    """Vista de detalles de los mangas"""
    model = Chapter
    pk_url_kwarg = 'chapter_id'
    template_name_suffix = '_detail'
    slug_url_kwarg = 'chapter_slug'
    query_pk_and_slug = True

    def get_object(self, queryset=None):
        manga_slug = self.kwargs['manga_slug']
        tomo_number = self.kwargs['tomo_number']
        try:
            tomo_number = int(tomo_number)
        except Exception:
            raise Http404()
        chapter_slug = self.kwargs['chapter_slug']
        manga = get_object_or_404(Manga, slug=manga_slug)
        tomo = get_object_or_404(Tomo, number=tomo_number, manga__id=manga.id)
        queryset = self.get_queryset().filter(
            manga=manga,
            slug=chapter_slug,
            tomo=tomo
            )
        return super(ChapterDetailView, self).get_object(queryset=queryset)

"""
Vistas Extras
"""

class PageChapterDetailView(ChapterDetailView):
    def get_context_data(self, **kwargs):
        context = super(PageChapterDetailView, self).get_context_data(**kwargs)
        if 'page' not in context:
            context['page'] = self.kwargs['page']
        return context

class ProfileView(ListView):
    """Vista para los mangas del usuario logeado"""
    model = Manga
    template_name = 'manageManga/manga_list_filter.html'
    context_object_name = 'mangas_list'

    def get_queryse(self):
        query = super(ProfileView, self).get_queryset()
        eventos_usuario = query.filter(author=self.request.user)
        return eventos_usuario


from django import forms
from django.conf.urls import url
from django.http import HttpResponse
from .models import Genre

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['genre']

def create_genres(request):
    for i in Genre.GENRE_CHOICES:
        genero = GenreForm({'genre':i[0]})
        genero.save()
    return HttpResponse()