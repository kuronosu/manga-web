from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$',views.HomeView.as_view(),name = 'home'),
    url(r'^mangas/$', views.MangaListView.as_view(), name = 'list_of_mangas'),
    url(r'^mangas/view/(?P<slug>[-\w]+)/(?P<manga_id>[0-9]+)$', views.MangaDetailView.as_view(), name = 'manga_detail'),
    url(r'^mangas/add$', views.MangaAddView.as_view(), name = 'manga_add'),
    url(r'^mangas/filter$', views.MangaFilterView.as_view(), name = 'manga_filter'),
]
