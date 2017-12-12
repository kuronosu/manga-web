"""Models: Create your models here."""
# from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.template import defaultfilters
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

def user_directory_path(instance, filename):
    """
    Funcion que añade retorna una path segun los datos y usuario y archivo
    """
    # file will be uploaded to MEDIA_ROOT/manga/chapter/user_<id>/<filename>
    return 'manga/chapter/user_{0}_{1}/{2}'.format(instance.owner.id, instance.owner.username, filename)

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
    verify = models.BooleanField(default=False, verbose_name=_('Verify'))

    def save(self, *args, **kwargs):
        self.slug = defaultfilters.slugify(self.title)
        super(Manga, self).save(*args, **kwargs)

    # def add_chapter(self, chapter_id, *args, **kwargs):
    #     """
    #     Metodo para añadir capitulos al atributo chapters del modelo Manga
    #     """
    #     chapters_instance = self.get_chapters()
    #     if not chapter_id in chapters_instance:
    #         chapters_instance.append(chapter_id)
    #         chapters_instance_str = ''.join(str(e)+';' for e in chapters_instance)
    #         self.chapters = chapters_instance_str

    # def get_chapters(self):
    #     """
    #     Metodo para obtener los capitulos del atributo chapters del modelo Manga
    #     """
    #     chapters_instance = self.chapters
    #     chapters_instance = chapters_instance.split(';')
    #     chapters_instance.remove('')
    #     return chapters_instance

    # def update_chapters(self, *args, **kwargs):
    #     """
    #     Metodo para actualizar los capitulos del atributo chapters del modelo Manga
    #     """
    #     if kwargs['chapter_id']:
    #         self.add_chapter(kwargs['chapter_id'])
    #     self.save(*args, **kwargs)


    def get_absolute_url(self):
        """Retorna la ulr para cada objeto de este modelo"""
        return reverse('manageManga:manga_detail', kwargs={'slug': self.slug, 'manga_id': self.pk})

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
    user_chapter_number = models.IntegerField(
        verbose_name=_('Chapter number'),
        validators=[MinValueValidator(1)]
        )
    name = models.CharField(max_length=100, verbose_name=_('Name'), blank=True)
#chapter_number=models.IntegerField(default=0,blank=True,null=True,verbose_name=_('Chapter number'))

    # def save(self, *args, **kwargs):
    #     self._set_manga_chapter()
    #     super(Chapter, self).save(*args, **kwargs)

    # def _set_manga_chapter(self):
    #     chapters_of_manga = self.manga.get_chapters()
    #     chapter_number = self._create_chapter_number(chapters_of_manga)
    #     self.chapter_number = chapter_number

    # def _create_chapter_number(self, chapters_of_manga):
    #     number = len(chapters_of_manga)+1
    #     if not number in chapters_of_manga:
    #         return int(number)
    #     else:
    #         return None

    def __str__(self):
        return str(self.manga)

    def __unicode__(self):
        return str(self.manga)

    def get_absolute_url(self):
        """Retorna la ulr para cada objeto de este modelo"""
        return reverse(
            'manageManga:chapter_detail',
            kwargs={'chapter_id': self.pk, 'manga_slug': self.manga.slug, 'manga_id': self.manga.id}
            )
