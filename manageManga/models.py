from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.template import defaultfilters
from django.conf import settings

# Create your models here.

class Gender(models.Model):
    GENDER_CHOICES = (
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
    gender = models.IntegerField(choices = GENDER_CHOICES, unique = True,validators = [MinValueValidator(1), MaxValueValidator(39)])
    name = models.CharField(max_length = 20, default = 'DEFAULT')

    def save(self, *args, **kwargs):
        if not self.id:
            self.name = self.GENDER_CHOICES[self.gender - 1][1]
            super(Gender, self).save(*args, **kwargs)

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
