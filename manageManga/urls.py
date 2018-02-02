"""Urls del app manageManga"""
from django.conf.urls import url
from django.urls import path, include
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
    path(
        '<str:manga_slug>/tomo/add/',
        views.TomoAddView.as_view(),
        name='tomo_add'
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
    path(
        r'<str:manga_slug>/tomo/<str:tomo_number>/',
        views.TomoDetailView.as_view(),
        name='tomo_detail',
    ),
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
        '<str:manga_slug>/tomo/<str:tomo_number>/chapter-<str:chapter_slug>/page-<int:page>/',
        views.PageChapterDetailView.as_view(),
        name='page_detail',
    ),
    path(
        'vote/<str:manga_slug>/',
        views.VoteView.as_view(),
        name='vote_manga'
    ),
    path(
        'my/',
        views.ProfileView.as_view(),
        name='my_mangas'
    ),
]
