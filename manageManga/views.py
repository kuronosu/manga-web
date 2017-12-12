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

"""
Vistas de los mangas
"""
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
        query = super(MangaListAndFilterView, self).get_queryset().filter(verify=True)
        search = self.request.GET.get('search', False)
        state = self.request.GET.get('state', False)
        genres = self.request.GET.getlist('genres', False)
        order = self.request.GET.get('order', False)
        queryset = None
        if order:
            if order == '0':
                pass
            else:
                if order == '1':
                    query = query.order_by('title')
                if order == '-1':
                    query = query.order_by('-title')
                if order == '-2':
                    query = query.order_by('published_date')
                if order == '2':
                    query = query.order_by('-published_date')
        if search:
            query = query.filter(title__icontains=search)
        if state:
            try:
                query = query.filter(state__state=int(state))
            except ValueError as _error:
                pass
        if genres:
            try:
                query = query.filter(genres__genre__in=genres)
            except ValueError as _error:
                pass

        queryset = []
        query_sin_repeticiones = query.in_bulk()
        for i in query_sin_repeticiones:
            queryset.append(query_sin_repeticiones[i])

        return queryset

    def get_context_data(self, **kwargs):
        context = super(MangaListAndFilterView, self).get_context_data(**kwargs)
        if 'filter_form' not in context:
            context['filter_form'] = self.form_classes['filter_form'](self.request.GET)
        if 'search_form' not in context:
            context['search_form'] = self.form_classes['search_form'](self.request.GET, initial={'slug': ''})
        if 'get_arg' not in context:
            search = self.request.GET.get('search', False)
            state = self.request.GET.get('state', False)
            genres = self.request.GET.getlist('genres', False)
            order = self.request.GET.get('order', False)
            args_get = ''
            if search:
                args_get += '&search='+search
            if state:
                args_get += '&state='+state
            if genres:
                for i in genres:
                    args_get += '&genres='+i
            if order:
                args_get += '&order='+order
            context['args_get'] = args_get

        return context

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
            if manga.author.id == self.request.user.id or self.request.user.is_staff:
                context['add_valid'] = True
            else:
                context['add_valid'] = False
        return context

    def get_queryset(self):
        query = super(MangaDetailView, self).get_queryset()
        return query.filter()

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

"""
Vistas de los capitulos
"""

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
            if manga.author.id == self.request.user.id or self.request.user.is_staff:
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

class ProfileView(ListView):
    """Vista para los mangas del usuario logeado"""
    model = Manga
    template_name = 'manageManga/manga_list_filter.html'
    context_object_name = 'mangas_list'

    def get_queryset(self):
        query = super(ProfileView, self).get_queryset()
        eventos_usuario = query.filter(author=self.request.user)
        return eventos_usuario
