from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.template import defaultfilters
from django.conf import settings

# Create your models here.

class Gender(models.Model):
    GENDER_CHOICES = (
        ('Acción', 'Acción',),
        ('Apocalíptico', 'Apocalíptico',),
        ('Artes Marciales', 'Artes Marciales',),
        ('Aventura', 'Aventura',),
        ('Ciencia Ficción', 'Ciencia Ficción',),
        ('Comedia', 'Comedia',),
        ('Cyberpunk', 'Cyberpunk',),
        ('Demonios', 'Demonios',),
        ('Deportes', 'Deportes',),
        ('Drama', 'Drama',),
        ('Ecchi', 'Ecchi',),
        ('Fantasía', 'Fantasía',),
        ('Gender Bender', 'Gender Bender',),
        ('Gore', 'Gore',),
        ('Harem', 'Harem',),
        ('Histórico', 'Histórico',),
        ('Horror', 'Horror',),
        ('Magia', 'Magia',),
        ('Mecha', 'Mecha',),
        ('Militar', 'Militar',),
        ('Misterio', 'Misterio',),
        ('Musical', 'Musical',),
        ('Parodia', 'Parodia',),
        ('Policial', 'Policial',),
        ('Psicológico', 'Psicológico',),
        ('Realidad Virtual', 'Realidad Virtual',),
        ('Recuentos de la vida', 'Recuentos de la vida',),
        ('Reencarnación', 'Reencarnación',),
        ('Romance', 'Romance',),
        ('Samurai', 'Samurai',),
        ('Sobrenatural', 'Sobrenatural',),
        ('Super Poderes', 'Super Poderes',),
        ('Supervivencia', 'Supervivencia',),
        ('Suspense', 'Suspense',),
        ('Tragedia', 'Tragedia',),
        ('Vampiros', 'Vampiros',),
        ('Vida Escolar', 'Vida Escolar',),
        ('Yaoi', 'Yaoi',),
        ('Yuri', 'Yuri',),
    )
    gender = models.CharField(max_length = 20, choices = GENDER_CHOICES, unique = True, blank=True, null=True)

    def __str__(self):
        return self.gender
    def __unicode__(self):
        return self.gender

class State(models.Model):
    STATE_CHOICES = (
        ('Emision', 'Emision'),
        ('Finalizado', 'Finalizado'),
        ('Pausado', 'Pausado'),
        ('Cancelado', 'Cancelado'),
    )
    state = models.CharField(max_length = 10, choices = STATE_CHOICES, unique = True, blank=True, null=True)

    def __str__(self):
        return self.state

    def __unicode__(self):
        return self.state

class Manga(models.Model):
    #author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length = 100)
    description = models.TextField(max_length = 700)
    published_date = models.DateField(auto_now_add = True, auto_now = False)
    state = models.ForeignKey(State)
    slug = models.SlugField(max_length=100, default = defaultfilters.slugify(title))
    genders = models.ManyToManyField(Gender, blank=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = defaultfilters.slugify(self.title)
            super(Manga, self).save(*args, **kwargs)
    
    # periodicity = models.Integerfield()

    def addChapter():
        pass
    
    def addComment():
        pass
    
    def __str__(self):
        return self.title
        
    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["published_date"]
        verbose_name_plural = 'Mangas'

class Comment(models.Model):
    manga = models.ForeignKey(Manga)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
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
