"""Urls del app manageManga"""
from django.conf.urls import url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

from django.urls import resolvers

app_name = 'manageManga'

urlpatterns = [
    path(
        '',
        views.MangaListAndFilterView.as_view(),
        name='list_of_mangas'
    ),
    #Urls para los mangas
    path(
        'add/',
        views.MangaAddView.as_view(),
        name='manga_add'
    ),
    path(
        '<str:slug>/',
        views.MangaDetailView.as_view(),
        name='manga_detail'
    ),
    path(
        '<str:slug>/edit/',
        views.MangaUpdateView.as_view(),
        name='manga_update'
    ),
    path(
        '<str:slug>/delete/',
        views.MangaDeleteView.as_view(),
        name='manga_delete'
    ),
    #Urls para los tomos
    path(
        '<str:manga_slug>/tomo/add/',
        views.TomoAddView.as_view(),
        name='tomo_add'
    ),
    path(
        r'<str:manga_slug>/tomo/<str:tomo_number>/',
        views.TomoDetailView.as_view(),
        name='tomo_detail',
    ),
    path(
        '<str:manga_slug>/tomo-<str:tomo_number>/edit/',
        views.TomoUpdateView.as_view(),
        name='tomo_update'
    ),
    path(
        '<str:manga_slug>/tomo-<str:tomo_number>/delete/',
        views.TomoDeleteView.as_view(),
        name='tomo_delete'
    ),
    #Urls para los capitulos
    path(
        '<str:manga_slug>/tomo/<str:tomo_number>/chapter/add/',
        views.ChapterAddView.as_view(),
        name='chapter_add'
    ),
    path(
        '<str:manga_slug>/tomo/<str:tomo_number>/chapter-<str:chapter_slug>/',
        views.ChapterDetailView.as_view(),
        name='chapter_detail',
    ),
    path(
        '<str:manga_slug>/tomo/<str:tomo_number>/chapter-<str:chapter_slug>/edit',
        views.ChapterUpdateView.as_view(),
        name='chapter_update'
    ),
    path(
        '<str:manga_slug>/tomo/<str:tomo_number>/chapter-<str:chapter_slug>/delete',
        views.ChapterDeleteView.as_view(),
        name='chapter_delete'
    ),
    #Url para votar
    path(
        '<str:manga_slug>/vote/',
        views.VoteView.as_view(),
        name='vote_manga'
    ),
]
