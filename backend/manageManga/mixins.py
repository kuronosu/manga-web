"""Mixins"""
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.template import defaultfilters
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.conf import settings
from django.urls import reverse

import requests, json

from .models import Manga, Chapter, Voto, Tomo, Page
from .util import frontend_permission, filter_obj_model
from .forms import PageRegistrationForm

class FilterMixin(object):
    """Mixin Filter for MangaListAndFilterView"""
    def get_queryset(self):
        query = super(FilterMixin, self).get_queryset().filter(verify=True)
        search = self.request.GET.get('search', False)
        state = self.request.GET.get('state', False)
        genres = self.request.GET.getlist('genres', False)
        order = self.request.GET.get('order', False)
        order_options = ['1', '-1', '2', '-2']
        if order and True in [v == order for v in order_options]:
            order = order.replace('1', 'title')
            order = order.replace('2', 'published_date_in_page')
            query = query.order_by(order)

        query = query.filter(title__icontains=search) if search else query

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
        context = super(FilterMixin, self).get_context_data(**kwargs)
        if 'filter_form' not in context:
            context['filter_form'] = self.form_classes['filter_form'](self.request.GET)
        if 'search_form' not in context:
            context['search_form'] = self.form_classes['search_form'](
                self.request.GET,
                initial={'slug': ''}
                )
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

class StaffFormsMixin(object):
    """Mixin para cambiar un formulario en caso de que sea un usuario del staff"""
    def get_form_class(self):
        if self.request.user.is_staff:
            self.form_class = self.staff_form
        return super(StaffFormsMixin, self).get_form_class()

class UserPermissionsMixin(object):
    """Mixin para verificar si un usuario puede acceder a una vista."""
    def dispatch(self, request, *args, **kwargs):
        try:
            model_obj = self.get_object()
            if model_obj is None:
                model_obj = self.get_permissions_object()
        except:
            model_obj = self.get_permissions_object()
        if not (model_obj.author.id == self.request.user.id or self.request.user.is_staff):
            raise PermissionDenied("No tiene acceso.")
        return super(UserPermissionsMixin, self).dispatch(request, *args, **kwargs)

class ChapterMixin:
    """ Mixin para la vista ChapterAddView y ChapterUpdateView """
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        manga = get_object_or_404(Manga, slug=self.kwargs['manga_slug'])
        try:
            chapters = filter_obj_model(Chapter, manga__id=manga.id)
            user_chapter_number = int(self.get_form_kwargs()['data']['user_chapter_number'])
            for i in chapters:
                if i.user_chapter_number == user_chapter_number:
                    if self.get_object() is None:
                        form.add_error('user_chapter_number', _('Chapter number not available'))
                    elif (self.get_object().user_chapter_number == user_chapter_number == i.user_chapter_number):
                        pass
                    else:
                        form.add_error('user_chapter_number', _('Chapter number not available'))
        except ValueError:
            pass

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class TomoMixin:
    """ Mixin para la vista TomoAddView y TomoUpdateView"""
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        manga = get_object_or_404(Manga, slug=self.kwargs['manga_slug'])
        try:
            tomos = filter_obj_model(Tomo, manga__id=manga.id)
            tomo_number = int(self.get_form_kwargs()['data']['number'])
            for i in tomos:
                if i.number == tomo_number:
                    if self.object is None:
                        form.add_error('number', _('Tomo number not available'))
                    elif (self.object.number == tomo_number == i.number):
                        pass
                    else:
                        form.add_error('number', _('Tomo number not available'))
        except ValueError:
            pass
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        manga_slug = self.kwargs['manga_slug']
        manga = get_object_or_404(Manga, slug=manga_slug)
        form.instance.manga = manga
        form.instance.author = self.request.user
        return super(TomoMixin, self).form_valid(form)

class NoEditTomo(object):
    """Mixin para evitar modificar el tomo -1 o default."""
    def dispatch(self, request, *args, **kwargs):
        try:
            tomo_number = int(kwargs['tomo_number'])
            if tomo_number == -1:
                raise Http404("Este tomo no se puede modificar.")
        except ValueError:
            pass
        return super(NoEditTomo, self).dispatch(request, *args, **kwargs) #pylint: disable=E1101

class BackendRenderMixin:
    def get(self, request, *args, **kwargs):
        response = super(BackendRenderMixin, self).get(request, *args, **kwargs)
        try:
            context = self.get_context_data(**kwargs)
            context.update(self.serialize_context_data(context))
            context.update(self.header_data_render(request))
            node_request = requests.post(settings.NODE_SERVER, json=context)
            if node_request.status_code == 200:
                return HttpResponse(node_request)
        except Exception as e:
            print(e)
        return response

    def header_data_render(self, request, to_json=False):
        """
        Funcion que retorna los datos usados en el header para enviar en la peticion al servidor ssr
        """
        if not (hasattr(request, 'path') and isinstance(request.path, str) and hasattr(request, 'user') and hasattr(request, 'COOKIES') and isinstance(request.COOKIES, dict)):
            raise ImproperlyConfigured("Isn't a valid request object.")

        urls = {
            'home': reverse('home'),
            'mangaList': reverse('manageManga:list_of_mangas'),
            'mangaAdd': reverse('manageManga:manga_add'),
            'accountsLogin': reverse('accounts:login') + '?next={}'.format(request.path),
            'accountsSignup': reverse('accounts:singup'),
            'accountsLogout': reverse('accounts:logout') + '?next={}'.format(request.path),
            'accountsPasswordReset': reverse('accounts:password_reset')
        }

        create_item = lambda name, url, url_args='', show=True, **kwargs: {'name': name, 'url': (reverse(url, kwargs=kwargs) + url_args), 'show': show}

        menuItems = [
            create_item(str(_('Lista de mangas')), 'manageManga:list_of_mangas'),
            create_item(str(_('Añadir manga')), 'manageManga:manga_add', show=request.user.is_authenticated),
        ]
        loggedMenu = [
            create_item(request.user.username, 'accounts:user_profile', username=request.user.username),
            create_item(str(_('Editar perfil')), 'accounts:user_profile', username=request.user.username),
            create_item(str(_('Cerrar sesion')), 'accounts:logout', '?next={}'.format(request.path)),
        ] if request.user.is_authenticated else []
        data = {
            'request_url': request.path,
            'csrftoken': request.COOKIES['csrftoken'],
            'isLogged': request.user.is_authenticated,
            'urls': urls,
            'menuItems': menuItems,
            'loggedMenu': loggedMenu,
            'user': {
                'username': request.user.username,
                'isAthenticated': request.user.is_authenticated
            }
        }
        if to_json:
            return json.dumps(data)
        return data
