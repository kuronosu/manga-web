from django.contrib import admin
from .models import Manga, Comment, Genre, State, Chapter

# Register your models here.

@admin.register(Manga)
class AdminManga(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'description', 'published_date']
    list_display_links = ['id']
    list_filter = ['author__username', 'published_date', 'state', 'genres']
    list_editable = []
    search_fields = ['author__username', 'title']
    ordering = ["id"]

    class Meta:
        model = Manga
    
@admin.register(Chapter)
class AdminManga(admin.ModelAdmin):
    list_display = ['id', 'manga', 'owner']
    list_display_links = ['id']
    list_filter = ['manga__title', 'owner__username']
    list_editable = []
    search_fields = ['owner__username', 'manga__title']
    ordering = ["id"]

    class Meta:
        model = Chapter

@admin.register(Genre)
class AdminGenre(admin.ModelAdmin):
    list_display = ['id', 'genre', 'name']
    list_display_links = ['id']
    list_filter = ['genre']
    list_editable = []
    search_fields = ['genre']
    ordering = ["id"]

    class Meta:
        model = Genre

@admin.register(State)
class AdminState(admin.ModelAdmin):
    list_display = ['id', 'state', 'name']
    list_display_links = ['id']
    list_filter = ['state']
    list_editable = []
    search_fields = ['state']
    ordering = ["id"]

    class Meta:
        model = State

@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ['manga', 'author']
    list_display_links = ['manga']
    list_filter = ['manga__title', 'author__username']
    list_editable = []
    search_fields = ['author__username', 'manga__title']

    class Meta:
        model = Comment
