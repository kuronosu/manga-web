"""Forms: Create your forms here."""
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe
from .models import Manga, Chapter, Voto, Tomo, Page
from .util import filter_obj_model
# from django.utils.translation import ugettext, ugettext_noop

def set_field_html_name(obj, new_name):
    """
    This creates wrapper around the normal widget rendering,
    allowing for a custom field name (new_name).
    """
    old_render = obj.widget.render
    def _widget_render_wrapper(name, value, attrs=None):
        name = new_name
        return old_render(name, value, attrs)

    obj.widget.render = _widget_render_wrapper

###############################################
# Formularios de busquedas y filtro de mangas #
###############################################

class FilterForm(forms.ModelForm):
    """Formulario para filtrar mangas"""
    CHOICES = [
        ('0', 'Default'),
        ('1', 'Name a-z'),
        ('-1', 'Name z-a'),
        ('2', 'New'),
        ('-2', 'Old')
        ]
    MAXGENRES = 7
    class Meta:
        """Meta clase"""
        model = Manga
        fields = ['genres', 'state']
        widgets = {'genres': forms.CheckboxSelectMultiple()}

    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        self.fields['order'] = forms.ChoiceField(choices=self.CHOICES, widget=forms.RadioSelect())
        self.fields['state'].widget.attrs['class'] = " custom-select"
        self.fields['state'].required = False
        self.fields['order'].required = False

    def clean(self):
        genres = self.cleaned_data.get('genres')
        if genres:
            if len(genres) > self.MAXGENRES:
                # Translators: Mensaje que aparece cuando
                # Translators: se intenta filtar con mas de un numero especifico de generos
                self.add_error('genres', _('Select maximum {} geners'.format(self.MAXGENRES)))
            return self.cleaned_data

class SearchForm(forms.ModelForm):
    """Formulario para buscar mangas"""
    class Meta:
        """Meta clase"""
        model = Manga
        fields = ['slug']

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['slug'].required = False
        self.fields['slug'].label = _('Search')
        self.fields['slug'].widget.attrs['placeholder'] = _('Search')
        # set_field_html_name(self.fields['slug'], 'search')

#############################
# Formularios de los mangas #
#############################

class RenderUpdateImage:
    def render_image(self):
        template = """
        <div class="mb-3">
            <p>{current}</p>
            <img class="current-image" src="/media/{url}" alt="{alt}">
        </div>
        <div class="custom-file">
            <input type="file" name="image" class="custom-file-input" id="id_image">
            <label class="custom-file-label" for="id_image">{label}</label>
        </div>
        """.format(
            url = self.initial['image'],
            alt = _("Image of ") + self.initial['title'],
            current = _("Current image: "),
            label = _("New image")
        )
        return mark_safe(template)

class MangaRegistrationForm(forms.ModelForm):
    """Formulario para la creacion de mangas"""
    MAXGENRES = 7

    class Meta:
        """Meta clase"""
        model = Manga
        fields = ['title', 'description', 'state', 'genres', 'image']
        widgets = {'genres': forms.CheckboxSelectMultiple()}

    def __init__(self, *args, **kwargs):
        super(MangaRegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {
                'class': 'form-control',
            }
        self.fields['title'].widget.attrs['placeholder'] = _('Titulo del manga')
        self.fields['description'].widget.attrs['placeholder'] = _('Description of manga')
        self.fields['state'].widget.attrs['class'] = 'custom-select'

    def clean(self):
        genres = self.cleaned_data.get('genres')
        if genres:
            if len(genres) > self.MAXGENRES:
                # Translators: Mensaje que aparece cuando
                # Translators: se intenta crear un manga con mas de un numero especifico de generos
                self.add_error('genres', _('Select maximum {} geners'.format(self.MAXGENRES)))
        slug_text = slugify(self.cleaned_data.get('title'))
        if filter_obj_model(Manga, slug=slug_text).exists():
            self.add_error('title', _('Title not available'))

        return super(MangaRegistrationForm, self).clean()

class MangaEditForm(forms.ModelForm, RenderUpdateImage):
    """Formulario para editar mangas"""

    class Meta:
        """Meta clase"""
        model = Manga
        fields = ['title', 'description', 'state', 'genres', 'image']
        widgets = {'genres': forms.CheckboxSelectMultiple()}

    def __init__(self, *args, **kwargs):
        super(MangaEditForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {
                'class': 'form-control',
            }
        self.fields['description'].widget.attrs['placeholder'] = _('Description of manga')

    def clean(self):
        genres = self.cleaned_data.get('genres')
        max_genres = 7
        if genres:
            if len(genres) > max_genres:
                # Translators: Mensaje que aparece cuando
                # Translators: se intenta editar un manga con mas de un numero especifico de generos
                self.add_error('genres', _('Select maximum {} geners'.format(max_genres)))
        return super(MangaEditForm, self).clean()

class StaffMangaEditForm(MangaEditForm, RenderUpdateImage):
    """ MangaEditForm para el sstaff """
    class Meta:
        """Meta clase"""
        model = Manga
        fields = ['title', 'description', 'state', 'genres', 'image', 'verify']
        widgets = {'genres': forms.CheckboxSelectMultiple()}
    

class VoteMangaForm(forms.ModelForm):
    class Meta:
        model = Voto
        fields = ['vote_value']

################################
# Formularios de los Tomos #
################################

class TomoCreationForm(forms.ModelForm):
    """Formulario para crear o actualizar tomos"""
    class Meta:
        """Meta clase"""
        model = Tomo
        fields = ['number']

class StaffTomoEditForm(TomoCreationForm):
    """TomoCreationForm para el staff"""
    class Meta:
        """Meta clase"""
        model = Tomo
        fields = '__all__'


################################
# Formularios de los capitulos #
################################

class ChapterRegistrationForm(forms.ModelForm):
    """Formulario para la creacion de capitulos"""
    class Meta:
        """Meta clase"""
        model = Chapter
        fields = ['content', 'user_chapter_number', 'name']

    def clean(self):
        content = self.cleaned_data.get('content')
        content_file_name = str(content)
        split_str = content_file_name.split('.')
        tipo = split_str[-1]
        if tipo.lower() != 'pdf':
            self.add_error('content', _('Por favor suba un archivo pdf.'))
        return super(ChapterRegistrationForm, self).clean()
    
class ChapterUpdateForm(forms.ModelForm):
    """" Formulario para actualizar capitulos """
    class Meta:
        """Meta clase"""
        model = Chapter
        fields = ['user_chapter_number', 'name']

################################
# Formularios de las paginas   #
################################

class PageRegistrationForm(forms.ModelForm):
    """Formulario para la creacion de capitulos"""
    class Meta:
        """Meta clase"""
        model = Page
        fields = ['number']
