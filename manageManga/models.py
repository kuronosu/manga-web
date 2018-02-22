"""Models: Create your models here."""
# from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.template import defaultfilters
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.shortcuts import get_object_or_404
import os

from .funct import filter_obj_model, user_directory_path

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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.name = self.GENRE_CHOICES[self.genre - 1][1]
        return super(Genre, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
            )

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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.name = self.STATE_CHOICES[self.state - 1][1]
        return super(State, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
            )

    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name

class Manga(models.Model):
    """
    Modelo del Manga
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Author'),
        on_delete=models.CASCADE
        )
    title = models.CharField(max_length=100, verbose_name=_('Title'), unique=True)
    description = models.TextField(
        max_length=1000,
        verbose_name=_('Description'),
        validators=[MinLengthValidator(10)]
        )
    published_date_in_page = models.DateField(
        auto_now_add=True,
        auto_now=False,
        verbose_name=_('Published Date')
        )
    state = models.ForeignKey(State, verbose_name=_('State'), on_delete=models.CASCADE)
    slug = models.SlugField(
        max_length=100,
        default=defaultfilters.slugify(title),
        unique=True,
        verbose_name=_('Slug'),
        )
    genres = models.ManyToManyField(Genre, verbose_name=_('Genres'))
    verify = models.BooleanField(default=False, verbose_name=_('Verify'))
    puntaje = models.FloatField(
        verbose_name=_('Puntaje'),
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        default=0
        )
    image = models.ImageField(upload_to='manga/portadas')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = defaultfilters.slugify(self.title)
        return super(Manga, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
            )

    def get_absolute_url(self):
        """Retorna la ulr para cada objeto de este modelo"""
        return reverse('manageManga:manga_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    class Meta:
        """Meta clase"""
        ordering = ["-puntaje"]
        verbose_name = 'Manga'
        verbose_name_plural = 'Mangas'

class Voto(models.Model):
    VOTE_CHOICES = (
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
        (6, 6), (7, 7), (8, 8), (9, 9), (10, 10),
    )
    manga = models.ForeignKey(Manga, verbose_name=_('Manga'), on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Author'),
        on_delete=models.CASCADE
        )
    vote_value = models.IntegerField(
        verbose_name=_('Voto'),
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        choices=VOTE_CHOICES
        )

    def __str__(self):
        return str(self.vote_value)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Voto, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
            )
        manga = get_object_or_404(Manga, id=self.manga.id)
        votos = filter_obj_model(Voto, manga__id=self.manga.id)
        suma = 0
        for i in votos:
            suma += i.vote_value
        prom = suma/len(votos)
        manga.puntaje = prom
        manga.save()

    def get_absolute_url(self):
        """Retorna la detail ulr hacia el manga referente al voto"""
        return reverse(
            'manageManga:manga_detail',
            kwargs={'slug': self.manga.slug}
            )

    class Meta:
        managed = True
        verbose_name = 'Voto'
        verbose_name_plural = 'Votos'

class Tomo(models.Model):
    """ Modelo de los tomos """
    number = models.IntegerField(
        verbose_name=_('Numero del Tomo'),
        validators=[MinValueValidator(-1)]
        )
    manga = models.ForeignKey(Manga, verbose_name=_('Manga'), on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Author'), on_delete=models.CASCADE)

    def get_absolute_url(self):
        """Retorna la detail ulr para cada objeto de este modelo"""
        return reverse(
            'manageManga:manga_detail',
            kwargs={'slug': self.manga.slug}
            )

    def __str__(self):
        return str(self.number)

    def __unicode__(self):
        return str(self.number)

    class Meta:
        """Meta clase"""
        ordering = ["number"]
        verbose_name_plural = _('Tomos')
        verbose_name = _('Tomo')


class Chapter(models.Model):
    """
    Modelo de capitulos
    """
    tomo = models.ForeignKey(Tomo, verbose_name=_('Tomo'), on_delete=models.CASCADE)
    manga = models.ForeignKey(Manga, verbose_name=_('Manga'), on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Author'), on_delete=models.CASCADE)
    content = models.FileField(upload_to=user_directory_path, verbose_name=_('PDF field'), help_text=_("Este no se puede modificar luego."))
    user_chapter_number = models.IntegerField(
        verbose_name=_('Chapter number'),
        validators=[MinValueValidator(1)]
        )
    name = models.CharField(max_length=100, verbose_name=_('Name'), blank=True)
    slug = models.SlugField(
        default=defaultfilters.slugify(user_chapter_number),
        verbose_name=_('Slug'))

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = defaultfilters.slugify(self.user_chapter_number)
        string_name = "%s_%s_%s.pdf"%(
            str(self.manga),
            str(self.tomo),
            str(self.user_chapter_number)
            )
        self.content.name = string_name
        super(Chapter, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
            )

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.BASE_DIR, os.path.join(settings.MEDIA_ROOT, self.content.name)))
        super(Chapter, self).delete(*args,**kwargs)

    def __str__(self):
        return str(self.user_chapter_number)

    def __unicode__(self):
        return str(self.manga)

    def get_absolute_url(self):
        """Retorna la detail ulr para cada objeto de este modelo"""
        return reverse(
            'manageManga:chapter_detail',
            kwargs={'chapter_slug': self.slug, 'manga_slug': self.manga.slug, 'tomo_number': self.tomo}
            )

    class Meta:
        """Meta clase"""
        ordering = ["user_chapter_number"]
        verbose_name_plural = _('Chapters')
        verbose_name = _('Chapter')

class Page(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, verbose_name=_('Capitulo'))
    number = models.IntegerField(
        verbose_name=_('Numero de la Página'),
        validators=[MinValueValidator(1)]
        )
    image = models.ImageField(upload_to=user_directory_path)

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.BASE_DIR, os.path.join(settings.MEDIA_ROOT, self.image.name)))
        super(Page, self).delete(*args,**kwargs)

    def __str__(self):
        return str(self.number)

    def __unicode__(self):
        return str(self.number)

    class Meta:
        """Meta clase"""
        ordering = ["number"]
        verbose_name_plural = _('Pages')
        verbose_name = _('Page')
