from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from django.template import loader
from django.contrib.auth.decorators import login_required

from .models import Manga
from .forms import MangaRegistrationForm

class HomeView(TemplateView):
    template_name = "home.html"

class MangaListView(ListView):
    model = Manga
    template_name = 'createManga/manga_list.html'
    context_object_name = 'mangas_list'
    paginate_by = 5

class MangaDetailView(DetailView):
    model = Manga
    pk_url_kwarg = 'manga_id'
    slug_url_kwarg = 'slug'
    template_name = 'createManga/manga_detail.html'

    def get_queryset(self):
        query = super(MangaDetailView, self).get_queryset()
        return query.filter()

#Esta clase no tine uso de momento, tiene por objetivo el hacer la vista de MangaAddView con clases y no con funciones
class classMangaAddView(CreateView):
    model = Manga
    template_name = 'createManga/manga_add.html'
    form_class = MangaRegistrationForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        # Llamamos ala implementacion primero del  context
        context = super(MangaAddView, self).get_context_data(**kwargs)
        # Agregamos el author
        context['author'] = self.request.user.id
        return context

    def get_form_kwargs(self):
        kwargs = super(MangaAddView, self).get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
            #kwargs['data'].add({'author': self.request.user})
            print(kwargs['data'])
        # if kwargs['data']:
        #     kwargs.update({'data': {'author': self.request.user.id} } )
        return kwargs

@login_required()
def MangaAddView(request):
    if request.method == 'POST':
        form = MangaRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST.get('title')
            description = request.POST.get('description')
            state = request.POST.get('state')
            author = request.user
            
            manga = Manga.objects.create(author = author, title = title, description = description, state = state)
            #manga.save()
            return HttpResponseRedirect('/')
        else:
            form = MangaRegistrationForm(request.POST, request.FILES)
            context = {'form': form}
            template = loader.get_template('createManga/manga_add.html')
            return HttpResponse(template.render(context, request))
    else:
        form = MangaRegistrationForm()
    template = loader.get_template('createManga/manga_add.html')
    context = {
        'form': form
    }
    return HttpResponse(template.render(context, request))

#Vista MangaAddView creada con clases, pero sin heredar de CreateView
class ClassMangaAddView(View):
    def get(self, request):
        form = MangaRegistrationForm()
        context = {'form': form}
        template = loader.get_template('createManga/manga_add.html')
        return HttpResponse(template.render(context, request))
    def post(self, request):
        form = MangaRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST.get('title')
            description = request.POST.get('description')
            state = request.POST.get('state')
            author = request.user
            
            manga = Manga.objects.create(author = author, title = title, description = description, state = state)
            #manga.save()
            return HttpResponseRedirect('/')
        else:
            form = MangaRegistrationForm(request.POST, request.FILES)
            context = {'form': form}
            template = loader.get_template('createManga/manga_add.html')
            return HttpResponse(template.render(context, request))