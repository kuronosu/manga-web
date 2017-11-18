"""Models: Create your models here."""
# from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.template import defaultfilters
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

def user_directory_path(instance, filename):
    """
    Funcion que añade retorna una path segun los datos y usuario y archivo
    """
    # file will be uploaded to MEDIA_ROOT/manga/chapter/user_<id>/<filename>
    return 'manga/chapter/user_{0}/{1}'.format(instance.owner.id, filename)

class Genre(models.Model):
    """
    Modelo de los generos
    """
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
    genre = models.IntegerField(
        choices=GENRE_CHOICES,
        unique=True,
        validators=[MinValueValidator(1), MaxValueValidator(39)]
        )
    name = models.CharField(max_length=20, default='DEFAULT')

    def save(self, *args, **kwargs):
        self.name = self.GENRE_CHOICES[self.genre - 1][1]
        super(Genre, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name

class State(models.Model):
    """
    Modelo de los estados
    """
    STATE_CHOICES = (
        (1, 'Emision'),
        (2, 'Finalizado'),
        (3, 'Pausado'),
        (4, 'Cancelado'),
    )
    state = models.IntegerField(
        choices=STATE_CHOICES,
        unique=True,
        validators=[MinValueValidator(1), MaxValueValidator(4)]
        )
    name = models.CharField(max_length=10, default='DEFAULT')

    def save(self, *args, **kwargs):
        self.name = self.STATE_CHOICES[self.state - 1][1]
        super(State, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class Manga(models.Model):
    """
    Modelo del Manga
    """
    #author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Author'))
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    description = models.TextField(max_length=700, verbose_name=_('Description'))
    published_date = models.DateField(
        auto_now_add=True,
        auto_now=False,
        verbose_name=_('Published Date')
        )
    state = models.ForeignKey(State, verbose_name=_('State'))
    slug = models.SlugField(
        max_length=100,
        default=defaultfilters.slugify(title),
        verbose_name=_('Slug'))
    genres = models.ManyToManyField(Genre, verbose_name=_('Genres'))
    # chapters = ArrayField(models.IntegerField())
    chapters = []

    def save(self, *args, **kwargs):
        self.slug = defaultfilters.slugify(self.title)
        super(Manga, self).save(*args, **kwargs)

    # periodicity = models.Integerfield()

    def add_chapter(self, chapter_id, *args, **kwargs):
        """
        Metodo para añadir capitulos al atributo chapters del modelo Manga
        """
        chapters_instance = self.chapters
        chapters_instance.append(chapter_id)
        self.chapters = chapters_instance
        return self, args, kwargs

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    class Meta:
        """Meta clase"""
        ordering = ["published_date"]
        verbose_name_plural = 'Mangas'

class Chapter(models.Model):
    """
    Modelo de capitulos
    """
    manga = models.ForeignKey(Manga)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Author'))
    content = models.FileField(upload_to=user_directory_path)

    def __str__(self):
        return str(self.manga)

    def __unicode__(self):
        return str(self.manga)
