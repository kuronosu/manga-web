"""Views: Create your views here."""
# from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect# , HttpResponseNotFound
# from django.http import Http404
from django.views.generic import ListView, DetailView # View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView #, FormView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
# from django.views.defaults import page_not_found
# from django.views.generic.edit import FormMixin
from django.template import loader
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.utils.decorators import method_decorator
# from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response

from .models import Manga, Chapter
from .forms import MangaRegistrationForm, FilterForm, SearchForm, ChapterRegistrationForm

class My404(TemplateView):
    """Vista del error 404"""
    template_name = "404.html"

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
        query = query.filter(verify=True)
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
            chapters = Chapter.objects.all()
            querry = chapters.filter(manga__id=manga.id)
            context['chapters'] = querry
        if 'add_valid' not in context:
            if manga.author.id == self.request.user.id:
                context['add_valid'] = True
            else:
                context['add_valid'] = False
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
    # success_url = reverse_lazy('manageManga:list_of_mangas')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(MangaAddView, self).form_valid(form)

class MangaUpdateView(LoginRequiredMixin, UpdateView):
    """Vista de para actualizar un manga"""
    login_url = '/login'
    model = Manga
    form_class = MangaRegistrationForm
    pk_url_kwarg = 'manga_id'
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True
    template_name_suffix = '_update'

class MangaDeleteView(DeleteView):
    """Vista de para eliminar un manga"""
    model = Manga
    pk_url_kwarg = 'manga_id'
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True
    success_url = reverse_lazy('manageManga:list_of_mangas')

class ChapterAddView(LoginRequiredMixin, CreateView):
    """Vista de para crear un chapitulo de un manga"""
    login_url = '/login'
    model = Chapter
    template_name_suffix = '_add'
    form_class = ChapterRegistrationForm
    # success_url = reverse_lazy('manageManga:manga_detail')
    # success_url = '/'

    def get(self, request, *args, **kwargs):
        manga_id = self.kwargs['manga_id']
        manga_slug = self.kwargs['manga_slug']
        manga = get_object_or_404(Manga, id=manga_id)
        if manga.slug == manga_slug:
            if manga.author.id == self.request.user.id:
                return super(ChapterAddView, self).get(request)
            else:
                template = loader.get_template('manageManga/restricted_access.html')
                context = {}
                return HttpResponse(template.render(context, request))
        else:
            return render_to_response('404.html', {})

    def form_valid(self, form):
        manga_id = self.kwargs['manga_id']# forma de obtener el id
        manga = Manga.objects.get(id=manga_id)
        form.instance.manga = manga
        form.instance.owner = self.request.user
        self.object = form.save()
        manga.add_chapter(self.object.id)
        return HttpResponseRedirect(self.get_success_url())

class ChapterDetailView(DetailView):
    """Vista de detalles de los mangas"""
    model = Chapter
    pk_url_kwarg = 'chapter_id'
    template_name_suffix = '_detail'

    def get(self, request, *args, **kwargs):
        manga_id = self.kwargs['manga_id']
        manga_slug = self.kwargs['manga_slug']
        manga = get_object_or_404(Manga, id=manga_id)
        chapter = get_object_or_404(Chapter, id=self.get_object().id)
        if manga.slug == manga_slug:
            if chapter.manga.id == manga.id:
                return super(ChapterDetailView, self).get(request)
            else:
                return render_to_response('404.html', {})
        else:
            return render_to_response('404.html', {})


    # def get_context_data(self, **kwargs):
    #     context = super(ChapterDetailView, self).get_context_data(**kwargs)
    #     return context

    # def get_queryset(self):
    #     query = super(ChapterDetailView, self).get_queryset()
    #     return query.filter()

class ProfileView(ListView):
    """Vista para los mangas del usuario logeado"""
    model = Manga
    template_name = 'manageManga/manga_list.html'
    context_object_name = 'mangas_list'

    def get_queryset(self):
        query = super(ProfileView, self).get_queryset()
        eventos_usuario = query.filter(author=self.request.user)
        return eventos_usuario
