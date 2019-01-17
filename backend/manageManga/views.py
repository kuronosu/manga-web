"""Views: Create your views here."""
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.db.models.fields.files import FieldFile
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
from django.shortcuts import get_object_or_404, render
from django.template import defaultfilters
from django.core.mail import EmailMessage
from django.conf import settings
from django.core import serializers

import os, json

from .models import Manga, Chapter, Voto, Tomo, Page
from .util import filter_obj_model, frontend_permission
from .pdfManager import convertPdf
from .mixins import (
    FilterMixin,
    StaffFormsMixin,
    UserPermissionsMixin,
    ChapterMixin,
    TomoMixin,
    NoEditTomo,
    BackendRenderMixin
    )
from .forms import (
    FilterForm,
    SearchForm,
    MangaRegistrationForm,
    MangaEditForm,
    ChapterRegistrationForm,
    VoteMangaForm,
    TomoCreationForm,
    PageRegistrationForm,
    ChapterUpdateForm,
# Staff forms
    StaffMangaEditForm,
    StaffTomoEditForm
    )

class HomeView(BackendRenderMixin, TemplateView):
    """Vista del home"""
    template_name = "home.html"
    
    def serialize_context_data(self, context):
        return {'view': 'Home'}

######################
#Vistas de los mangas#
######################
def safe_execute(function, default, exception=Exception, *args, **kwargs):
    try:
        return function(*args)
    except exception:
        return default

class MangaListAndFilterView(BackendRenderMixin, FilterMixin, ListView):
    """Vista para listar y filtrar mangas"""
    model = Manga
    template_name = 'manageManga/manga_list.html'
    context_object_name = 'mangas_list'
    paginate_by = 8
    form_classes = {
        'filter_form': FilterForm,
        'search_form': SearchForm
    }

    def serialize_context_data(self, context):        
        paginator = dict(context['paginator'].__dict__)
        paginator.update({
            'count': context['paginator'].count,
            'num_pages': context['paginator'].num_pages,
            'page_range': list(context['paginator'].page_range),
            'object_list': json.loads(serializers.serialize('json', context['paginator'].object_list))
        })

        page_obj = dict(context['page_obj'].__dict__)
        page_obj.update({
            'has_previous': context['page_obj'].has_previous(),
            'previous_page_number': safe_execute(context['page_obj'].previous_page_number, None, Exception),
            'number': context['page_obj'].number,
            'has_next': context['page_obj'].has_next(),
            'next_page_number': safe_execute(context['page_obj'].next_page_number, None, Exception),
            'paginator': paginator,
            'object_list': json.loads(serializers.serialize('json', context['page_obj'].object_list))
        })

        object_list = json.loads(serializers.serialize('json', context['object_list']))

        return {
            'paginator': paginator,
            'page_obj': page_obj,
            'object_list': object_list,
            'view': 'MangaList',
            'mangas_list': None,
            'filter_form': None,
            'search_form': None,
        }

class MangaAddView(LoginRequiredMixin, CreateView):
    """Vista de para crear un manga"""
    login_url = reverse_lazy('accounts:login')
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
            context['form_vote_files'] = list(range(1, 6))
        if 'tomos' not in context:
            context['tomos'] = filter_obj_model(Tomo, manga=self.object)
        if 'vote_form' not in context:
            try:
                vote_object = get_object_or_404(Voto ,manga=self.object,author=self.request.user)
                context['vote_form'] = VoteMangaForm(dict(vote_value=vote_object.vote_value))
            except:
                context['vote_form'] = VoteMangaForm()
        if 'frontend_permission' not in context:
            context['frontend_permission'] = frontend_permission(self)

        puntaje = str(round(context['manga'].puntaje, 1)).replace(',', '.')
        context['manga'].puntaje = puntaje
        return context

class MangaUpdateView(LoginRequiredMixin, UserPermissionsMixin, StaffFormsMixin, UpdateView):
    """Vista de para actualizar un manga"""
    login_url = reverse_lazy('accounts:login')
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
    login_url = reverse_lazy('accounts:login')
    model = Manga
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True
    success_url = reverse_lazy('manageManga:list_of_mangas')
    permissions_slug_url_kwarg = 'slug'
    permissions_model = Manga

#####################
#Vistas de los votos#
#####################

class VoteView(ModelFormMixin, ProcessFormView):
    """ Vista para manejar los votos de un manga """
    model = Voto
    form_class = VoteMangaForm
    login_url = reverse_lazy('accounts:login')

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
        return Http404('Invalid Method')

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
        return JsonResponse({'state': False, 'message': _("Errores en el formulario."),})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            if request.is_ajax():
                return JsonResponse({
                'state': False,
                'message': _("Inicia sesion para poder votar. "),
                })
        return super().dispatch(request, *args, **kwargs)

#####################
#Vistas de los tomos#
#####################

class TomoAddView(LoginRequiredMixin, TomoMixin, UserPermissionsMixin, CreateView):
    """Vista de para crear un tomo de un manga"""
    login_url = reverse_lazy('accounts:login')
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
        except ValueError:
            raise Http404()
        manga = get_object_or_404(Manga, slug=manga_slug)
        tomo = get_object_or_404(Tomo, number=tomo_number, manga=manga)
        return tomo

class TomoUpdateView(LoginRequiredMixin, NoEditTomo, UserPermissionsMixin, TomoMixin, UpdateView):
    """Vista de para actualizar un tomo de un manga"""
    login_url = reverse_lazy('accounts:login')
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
        except ValueError:
            raise Http404()
        manga = get_object_or_404(Manga, slug=manga_slug)
        tomo = get_object_or_404(Tomo, number=tomo_number, manga=manga)
        return tomo

class TomoDeleteView(LoginRequiredMixin, NoEditTomo, UserPermissionsMixin, DeleteView):
    model = Tomo
    login_url = reverse_lazy('accounts:login')
    success_url = reverse_lazy('manageManga:list_of_mangas')
    permissions_slug_url_kwarg = 'manga_slug'
    permissions_model = Manga

    def get_object(self, queryset=None):
        manga_slug = self.kwargs['manga_slug']
        tomo_number = self.kwargs['tomo_number']
        try:
            tomo_number = int(tomo_number)
        except ValueError:
            raise Http404()
        manga = get_object_or_404(Manga, slug=manga_slug)
        tomo = get_object_or_404(Tomo, number=tomo_number, manga=manga)
        return tomo
    
    def get_permissions_object(self, *args, **kwargs):
        slug = self.kwargs[self.permissions_slug_url_kwarg]
        manga = get_object_or_404(self.permissions_model, slug=slug)
        return manga

#########################
#Vistas de los capitulos#
#########################

class ChapterAddView(LoginRequiredMixin, ChapterMixin, UserPermissionsMixin, CreateView):
    """Vista de para crear un capitulo de un manga"""
    login_url = reverse_lazy('accounts:login')
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
        except ValueError:
            raise Http404()
        manga = get_object_or_404(Manga, slug=manga_slug)
        queryset = filter_obj_model(Tomo, number=tomo_number, manga=manga)
        try:
            queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No coincide el tomo del manga y el manga peroporcionado")
        return super(ChapterAddView, self).dispatch(request, *args, **kwargs)
    
    def get_permissions_object(self, *args, **kwargs):
        slug = self.kwargs[self.permissions_slug_url_kwarg]
        manga = get_object_or_404(self.permissions_model, slug=slug)
        return manga

    def form_valid(self, form):
        manga_slug = self.kwargs['manga_slug']
        tomo_number = self.kwargs['tomo_number']
        manga = get_object_or_404(Manga, slug=manga_slug)
        tomo = get_object_or_404(Tomo, manga=manga, number=tomo_number)
        form.instance.manga = manga
        form.instance.tomo = tomo
        form.instance.author = self.request.user
        form.instance.content.name = defaultfilters.slugify(form.instance.content.name)
        self.object = form.save() 
        try:
            created_pages = convertPdf(self.object.content.name)
        except Exception as e:
            body = str(e)
            email = EmailMessage(
                subject="error",
                body=body+"\nviews.py",
                to=['andresfelipe.2031@gmail.com']
                )
            email.content_subtype = 'html'
            email.send()
            created_pages = []
        if len(created_pages) > 0:
            for i in created_pages:
                page_form = PageRegistrationForm({'number': i.number})
                page_form.instance.chapter = self.object
                page_form.instance.image = i.url
                page_form.save()
            if self.request.is_ajax():
                context = {
                    'redirect_url': self.object.get_absolute_url(),
                    'ajax_status': 1
                }
                return JsonResponse(context)
            return HttpResponseRedirect(self.get_success_url())
        else:
            self.object.delete()
            form.add_error('content', _('Error al procesar el archivo'))
            context = self.get_context_data()
            context['form'] = form
            if self.request.is_ajax():
                form.errors['ajax_status'] = 0
                return JsonResponse(form.errors)
            return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = None
        return super(ChapterAddView, self).post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return None
    
    def form_invalid(self, form):
        if self.request.is_ajax():
            form.errors['ajax_status'] = 0
            return JsonResponse(form.errors)
        return super(ChapterAddView, self).form_invalid(form)

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
        except ValueError:
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
    
    def get_context_data(self, **kwargs):
        context = super(ChapterDetailView, self).get_context_data(**kwargs)
        query = filter_obj_model(Page, chapter=self.object)
        if 'pages' not in context:
            pages = query
            context['pages'] = pages
        if 'page' not in context:
            number_page = self.get_page(self.request)
            len_query = len(query)
            try:
                if len_query > 0 and number_page <= len_query:
                    page = query.get(number = number_page)
                else:
                    page = query.get(number = 1)
            except Exception:
                raise Http404()

            if page.number == len(query):
                page.nexPage = page.number
            else:
                page.nexPage = page.number + 1
            if page.number == 1:
                page.backPage = page.number
            else:
                page.backPage = page.number -1
            context['page'] =  page
        return context
    
    def get_page(self, request):
        try:
            if ( request.GET.get("page") is not None) and (int(request.GET.get("page")) >= 1):
                page = int(request.GET.get("page"))
            else:
                page = 1
        except Exception:
            page = 1
        return page

class ChapterUpdateView(LoginRequiredMixin, ChapterMixin, UserPermissionsMixin, UpdateView):
    """Vista de para crear un capiCreatetulo de un manga"""
    login_url = reverse_lazy('accounts:login')
    model = Chapter
    template_name_suffix = '_update'
    form_class = ChapterUpdateForm
    permissions_slug_url_kwarg = 'manga_slug'
    permissions_model = Manga

    def get_object(self, queryset=None):
        manga_slug = self.kwargs['manga_slug']
        tomo_number = self.kwargs['tomo_number']
        try:
            tomo_number = int(tomo_number)
        except ValueError:
            raise Http404()
        chapter_slug = self.kwargs['chapter_slug']
        manga = get_object_or_404(Manga, slug=manga_slug)
        tomo = get_object_or_404(Tomo, number=tomo_number, manga__id=manga.id)
        queryset = self.get_queryset().filter(
            manga=manga,
            slug=chapter_slug,
            tomo=tomo
            )
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No coincide el tomo del manga y el manga peroporcionado")
        return obj

    def get_permissions_object(self, *args, **kwargs):
        slug = self.kwargs[self.permissions_slug_url_kwarg]
        manga = get_object_or_404(self.permissions_model, slug=slug)
        return manga
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ChapterUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        manga_slug = self.kwargs['manga_slug']
        tomo_number = self.kwargs['tomo_number']
        manga = get_object_or_404(Manga, slug=manga_slug)
        tomo = get_object_or_404(Tomo, manga=manga, number=tomo_number)
        form.instance.tomo = tomo
        form.instance.manga = manga
        form.instance.author = self.request.user
        form.instance.content = self.get_object().content
        return super(ChapterUpdateView, self).form_valid(form)

class ChapterDeleteView(LoginRequiredMixin,UserPermissionsMixin , DeleteView):
    model = Chapter
    login_url = reverse_lazy('accounts:login')
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
        chapter_slug = self.kwargs['chapter_slug']
        manga = get_object_or_404(Manga, slug=manga_slug)
        tomo = get_object_or_404(Tomo, number=tomo_number, manga__id=manga.id)
        queryset = self.get_queryset().filter(
            manga=manga,
            slug=chapter_slug,
            tomo=tomo
            )
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No coincide el tomo del manga y el manga peroporcionado")
        return obj
    
    def get_permissions_object(self, *args, **kwargs):
        slug = self.kwargs[self.permissions_slug_url_kwarg]
        manga = get_object_or_404(self.permissions_model, slug=slug)
        return manga


def ajax(request):
    """ Vista para hacer pruebas de las peticiones con ajax"""
    if request.is_ajax():
        print("Ajax")
        data = {"con": True}
        print(request.GET)
        print(request.POST)
        print(request.FILES)
        return JsonResponse(data)
    else:
        print("Not Ajax")
        return render(request, "test.html")
