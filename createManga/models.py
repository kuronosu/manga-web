from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Manga(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length = 100)
    description = models.TextField(max_length = 700)
    published_date = models.DateField(auto_now_add = True, auto_now = False)
    state = models.IntegerField(
        default = 1, 
        validators = [
            MinValueValidator(1), 
            MaxValueValidator(3)
            ]
        )
    # periodicity = models.Integerfield()

    def addChapter():
        pass
    
    def addComment():
        pass
    
    def __str__(self):
        return self.title
        
    def __unicode__(self):
        return self.author

class Comment(models.Model):
    manga = models.ForeignKey(Manga)
    author = models.ForeignKey('auth.User')
    comment = models.CharField(max_length = 300)

    def __str__(self):
        return self.author
    def __unicode__(self):
        return self.author

class Chapter(models.Model):
    manga = models.ForeignKey(Manga)


    def __str__(self):
        return 

    def __unicode__(self):
        return 
