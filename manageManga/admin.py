"""Admin: Register your models here."""
from django.contrib import admin
from .models import Manga, Genre, State, Chapter, Voto


class AdminManga(admin.ModelAdmin):
    """Clase para registrar el modelo Manga"""
    list_display = ['id', 'author', 'title', 'description', 'published_date_in_page', 'verify', 'puntaje']
    list_display_links = ['id']
    list_filter = ['author__username', 'published_date_in_page', 'state', 'genres', 'verify']
    list_editable = []
    search_fields = ['author__username', 'title']
    ordering = ["-puntaje"]

class AdminChapter(admin.ModelAdmin):
    """Clase para registrar el modelo Chapter"""
    list_display = ['id', 'manga', 'author', 'user_chapter_number']
    list_display_links = ['id']
    list_filter = ['manga', 'author__username']
    list_editable = []
    search_fields = ['author__username', 'manga']
    ordering = ["id"]

class AdminGenre(admin.ModelAdmin):
    """Clase para registrar el modelo Genre"""
    list_display = ['id', 'genre', 'name']
    list_display_links = ['id']
    list_filter = ['genre']
    list_editable = []
    search_fields = ['genre']
    ordering = ["id"]

class AdminState(admin.ModelAdmin):
    """Clase para registrar el modelo State"""
    list_display = ['id', 'state', 'name']
    list_display_links = ['id']
    list_filter = ['state']
    list_editable = []
    search_fields = ['state']
    ordering = ["id"]

class AdminVoto(admin.ModelAdmin):
    list_display = ['id', 'vote_value', 'author', 'manga']
    list_display_links = ['id']
    list_filter = ['vote_value', 'author', 'manga']
    search_fields = ['vote_value', 'author']
    ordering = ["id"]

admin.site.register(Manga, AdminManga)
admin.site.register(Chapter, AdminChapter)
admin.site.register(Genre, AdminGenre)
admin.site.register(State, AdminState)
admin.site.register(Voto, AdminVoto)
