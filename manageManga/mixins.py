"""Mixins"""
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
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
    def get(self, request, *args, **kwargs):
        slug = self.kwargs[self.permissions_slug_url_kwarg]
        model_obj = get_object_or_404(self.permissions_model, slug=slug)
        if model_obj.author.id == self.request.user.id or self.request.user.is_staff:
            return super(UserPermissionsMixin, self).get(request, *args, **kwargs)
        else:
            return redirect('manageManga:manga_detail', slug=slug)
