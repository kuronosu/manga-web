from django.contrib import admin
from .models import Manga, Comment, Gender, State

# Register your models here.

@admin.register(Manga)
class AdminManga(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'description', 'published_date']
    list_display_links = ['id']
    list_filter = ['author__username', 'published_date', 'state', 'genders']
    list_editable = []
    search_fields = ['author__username', 'title']
    ordering = ["id"]

    class Meta:
        model = Manga

@admin.register(Gender)
class AdminGender(admin.ModelAdmin):
    list_display = ['id', 'gender', 'name']
    list_display_links = ['id']
    list_filter = ['gender']
    list_editable = []
    search_fields = ['gender']
    ordering = ["id"]

    class Meta:
        model = Gender

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
