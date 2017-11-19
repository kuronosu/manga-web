"""Urls del app manageManga"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^$', views.HomeView.as_view(),
        name='home'
    ),
    url(
        r'^manga/$',
        views.MangaListAndFilterView.as_view(),
        name='list_of_mangas'
    ),
    url(
        r'^manga/add$',
        views.MangaAddView.as_view(),
        name='manga_add'
    ),
    url(
        r'^manga/(?P<slug>[-\w]+)/(?P<manga_id>[0-9]+)$',
        views.MangaDetailView.as_view(),
        name='manga_detail'
    ),
    url(
        r'^manga/(?P<slug>[-\w]+)/(?P<manga_id>[0-9]+)/update$',
        views.MangaUpdateView.as_view(),
        name='manga_update'
    ),
    url(
        r'^manga/(?P<slug>[-\w]+)/(?P<manga_id>[0-9]+)/delete$',
        views.MangaDeleteView.as_view(),
        name='manga_delete'
    ),
    url(
        r'^manga/(?P<manga_slug>[-\w]+)/(?P<manga_id>[0-9]+)/chapter/add$',
        views.ChapterAddView.as_view(),
        name='chapter_add'
    ),
    url(
        r'^manga/(?P<manga_slug>[-\w]+)/(?P<manga_id>[0-9]+)/chapter/(?P<chapter_id>[-\w]+)$',
        views.ChapterDetailView.as_view(),
        name='chapter_detail',
    ),
    url(
        r'^my$',
        views.ProfileView.as_view(),
        name='my_mangas'
    )
    # url(r'^manga/filter$', views.MangaFilterView.as_view(), name = 'manga_filter'),
]
