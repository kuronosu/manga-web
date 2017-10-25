from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic import View, ListView, DetailView
from django.core.urlresolvers import reverse_lazy
from django.template import loader

from .models import Manga
from .forms import RegForm

class HomeView(TemplateView):
    template_name = "home.html"

class MangaListView(ListView):
    model = Manga
    template_name = 'createManga/manga_list.html'
    context_object_name = 'mangas_list'
    paginate_by = 5

class MangaDetailView(DetailView):
    model = Manga
    pk_url_kwarg = 'id'
    slug_field = 'title'
    slug_url_kwarg = 'title'
    query_pk_and_slug = True
    template_name = 'createManga/manga_detail.html'
    
    def get_queryset(self):
        query = super(MangaDetailView, self).get_queryset()
        print(query)
        return query

# class ModelNameDetail(DetailView):
#     model = ModelName
#     template_name=''

# class HomeView(View):
#     class Meta:
#         template_name = "home.html"        
#     def get(self, request):
#         return HttpResponse('result')
