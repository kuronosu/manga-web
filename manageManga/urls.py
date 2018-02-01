"""Urls del app manageManga"""
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
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
        r'^manga/add/$',
        views.MangaAddView.as_view(),
        name='manga_add'
    ),
    url(
        r'^manga-(?P<slug>[-\w]+)/$',
        views.MangaDetailView.as_view(),
        name='manga_detail'
    ),
    url(
        r'^manga-(?P<slug>[-\w]+)/edit/$',
        views.MangaUpdateView.as_view(),
        name='manga_update'
    ),
    url(
        r'^manga-(?P<slug>[-\w]+)/delete/$',
        views.MangaDeleteView.as_view(),
        name='manga_delete'
    ),
    url(
        r'^manga-(?P<manga_slug>[-\w]+)/tomo/add/$',
        views.TomoAddView.as_view(),
        name='tomo_add'
    ),
    url(
        r'^manga-(?P<manga_slug>[-\w]+)/tomo-(?P<tomo_number>\d+)/edit/$',
        views.TomoUpdateView.as_view(),
        name='tomo_update'
    ),
    url(
        r'^manga-(?P<manga_slug>[-\w]+)/tomo-(?P<tomo_number>\d+)/delete/$',
        views.TomoDeleteView.as_view(),
        name='tomo_delete'
    ),
    url(
        r'^manga-(?P<manga_slug>[-\w]+)/tomo-(?P<tomo_number>[-\w]+)/$',
        views.TomoDetailView.as_view(),
        name='tomo_detail',
    ),
    url(
        r'^manga-(?P<manga_slug>[-\w]+)/tomo-(?P<tomo_number>[-\w]+)/chapter/add/$',
        views.ChapterAddView.as_view(),
        name='chapter_add'
    ),
    url(
        r'^manga-(?P<manga_slug>[-\w]+)/tomo-(?P<tomo_number>[-\w]+)/chapter-(?P<chapter_slug>[-\w]+)/$',
        views.ChapterDetailView.as_view(),
        name='chapter_detail',
    ),
    url(
        r'^manga-(?P<manga_slug>[-\w]+)/tomo-(?P<tomo_number>[-\w]+)/chapter-(?P<chapter_slug>[-\w]+)/page-(?P<page>[0-9]+)/$',
        views.PageChapterDetailView.as_view(),
        name='page_detail',
    ),
    url(
        r'^vote-manga-(?P<manga_slug>[-\w]+)/$',
        views.VoteView.as_view(),
        name='vote_manga'
    ),
    url(
        r'^my/$',
        views.ProfileView.as_view(),
        name='my_mangas'
    )
    # url(r'^manga/filter$', views.MangaFilterView.as_view(), name = 'manga_filter'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
