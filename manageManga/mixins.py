"""Mixins"""
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from .models import Manga, Chapter, Voto
from .funct import frontend_permission, filter_obj_model

class FilterMixin(object):
    """Mixin Filter for MangaListAndFilterView"""
    def get_queryset(self):
        query = super(FilterMixin, self).get_queryset().filter(verify=True)
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
        return self.form_class

class UserPermissionsMixin(object):
    """Mixin para verificar si un usuario puede hacer modificaciones con respecto a un modelo"""
    def dispatch(self, request, *args, **kwargs):
        slug = self.kwargs[self.permissions_slug_url_kwarg]
        model_obj = get_object_or_404(self.permissions_model, slug=slug)
        if not (model_obj.author.id == self.request.user.id or self.request.user.is_staff):
            return redirect('manageManga:manga_detail', slug=slug)
        return super(UserPermissionsMixin, self).dispatch(request, *args, **kwargs)

class ExtraContextMixin(object):
    def get_context_data(self, **kwargs):
        context = super(ExtraContextMixin, self).get_context_data(**kwargs)
        for key, val in self.extra_context.items():
            if key not in context:
                if val[0] == 'filter':
                    filter_dic = {}
                    for i, j in val[2].items():
                        if j == 'id':
                            filter_dic[i] = self.object.id
                    context_value = filter_obj_model(val[1], **filter_dic)
                elif val[0] == 'frontend_permission':
                    context_value = frontend_permission(self)
                elif val[0] == 'vote_form':
                    vote_object = filter_obj_model(
                        Voto,
                        manga__id=self.object.id,
                        author__id=self.request.user.id
                        )
                    try:
                        context_value = val[1](dict(vote_value=vote_object[0].vote_value))
                    except IndexError as error:
                        print(error)
                        context_value = val[1]()
            context[key] = context_value
        return context

class ChapterAddMixin:
    """ Mixin para la vista ChapterAddView """
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
            chapters = filter_obj_model(Chapter, manga__id=manga.id)
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
        return super(ChapterAddMixin, self).form_valid(form)
