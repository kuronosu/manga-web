from django.contrib import admin
from .models import Manga

# Register your models here.

@admin.register(Manga)
class AdminModel(admin.ModelAdmin):
    list_display = ['author', 'title', 'description', 'published_date']
    list_display_links = ['author']
    list_filter = ['author', 'published_date']
    list_editable = []
    search_fields = ['author__username', 'title']

    class Meta:
        model = Manga
