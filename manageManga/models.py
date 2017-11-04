from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.template import defaultfilters
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Genre(models.Model):
    GENRE_CHOICES = (
        (1, 'Acción',),
        (2, 'Apocalíptico',),
        (3, 'Artes Marciales',),
        (4, 'Aventura',),
        (5, 'Ciencia Ficción',),
        (6, 'Comedia',),
        (7, 'Cyberpunk',),
        (8, 'Demonios',),
        (9, 'Deportes',),
        (10, 'Drama',),
        (11, 'Ecchi',),
        (12, 'Fantasía',),
        (13, 'Gender Bender',),
        (14, 'Gore',),
        (15, 'Harem',),
        (16, 'Histórico',),
        (17, 'Horror',),
        (18, 'Magia',),
        (19, 'Mecha',),
        (20, 'Militar',),
        (21, 'Misterio',),
        (22, 'Musical',),
        (23, 'Parodia',),
        (24, 'Policial',),
        (25, 'Psicológico',),
        (26, 'Realidad Virtual',),
        (27, 'Recuentos de la vida',),
        (28, 'Reencarnación',),
        (29, 'Romance',),
        (30, 'Samurai',),
        (31, 'Sobrenatural',),
        (32, 'Super Poderes',),
        (33, 'Supervivencia',),
        (34, 'Suspense',),
        (35, 'Tragedia',),
        (36, 'Vampiros',),
        (37, 'Vida Escolar',),
        (38, 'Yaoi',),
        (39, 'Yuri',),
    )
    genre = models.IntegerField(choices = GENRE_CHOICES, unique = True,validators = [MinValueValidator(1), MaxValueValidator(39)])
    name = models.CharField(max_length = 20, default = 'DEFAULT')

    def save(self, *args, **kwargs):
        if not self.id:
            self.name = self.GENRE_CHOICES[self.genre - 1][1]
            super(Genre, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name

class State(models.Model):
    STATE_CHOICES = (
        (1, 'Emision'),
        (2, 'Finalizado'),
        (3, 'Pausado'),
        (4, 'Cancelado'),
    )
    state = models.IntegerField(choices = STATE_CHOICES, unique = True,validators = [MinValueValidator(1), MaxValueValidator(4)])
    name = models.CharField(max_length = 10, default = 'DEFAULT')

    def save(self, *args, **kwargs):
        if not self.id:
            self.name = self.STATE_CHOICES[self.state - 1][1]
            super(State, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class Manga(models.Model):
    #author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Author'))
    title = models.CharField(max_length = 100, verbose_name=_('Title'))
    description = models.TextField(max_length = 700, verbose_name=_('Description'))
    published_date = models.DateField(auto_now_add = True, auto_now = False, verbose_name=_('Published Date'))
    state = models.ForeignKey(State, verbose_name=_('State'))
    slug = models.SlugField(max_length=100, default = defaultfilters.slugify(title), verbose_name=_('Slug'))
    genres = models.ManyToManyField(Genre, verbose_name=_('Genres'))

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
