from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$',views.HomeView.as_view(),name = 'home'),
    url(r'^mangas/$', views.MangaListView.as_view(), name = 'list_of_mangas'),
    url(r'manga/(?P<id>[0-9]+)/(?P<slug>[-\w]+)$', views.MangaDetailView.as_view(), name = 'manga_detail'),
    #r'(?P<manga_id>\d+)/(?P<slug>[-\w]+)$'
    # r'^manga/(?P<pk>[0-9]+)/$'
    # r'^manga/(?P<slug>[-\w]+)/(?P<pk>\d+)/$'
]