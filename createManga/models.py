from django.db import models

# Create your models here.

class Manga(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length = 100)
    description = models.TextField(max_length = 700)
    published_date = models.DateTimeField(auto_now_add = True, auto_now = False)

    class Meta:
        verbose_name_plural = 'Mangas'
    
    def __str__(self):
        return self.title