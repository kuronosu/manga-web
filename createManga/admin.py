from django.contrib import admin
from .models import Manga, Comment

# Register your models here.

@admin.register(Manga)
class AdminModel(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'description', 'published_date']
    list_display_links = ['id']
    list_filter = ['author__username', 'published_date']
    list_editable = []
    search_fields = ['author__username', 'title']
    ordering = ["id"]

    class Meta:
        model = Manga
        
@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ['manga', 'author']
    list_display_links = ['manga']
    list_filter = ['manga__title', 'author__username']
    list_editable = []
    search_fields = ['author__username', 'manga__title']

    class Meta:
        model = Comment