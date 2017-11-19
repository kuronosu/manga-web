"""Forms: Create your forms here."""
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Manga, Chapter
# from django.utils.translation import ugettext, ugettext_noop

def set_field_html_name(obj, new_name):
    """
    This creates wrapper around the normal widget rendering,
    allowing for a custom field name (new_name).
    """
    old_render = obj.widget.render
    def _widget_render_wrapper(name, value, attrs=None):
        return old_render(new_name, value, attrs)

    obj.widget.render = _widget_render_wrapper

class MangaRegistrationForm(forms.ModelForm):
    """Formulario para la creacion de mangas"""

    def __init__(self, *args, **kwargs):
        super(MangaRegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {
                'class': 'form-control',
                'required': True,
            }
        self.fields['title'].widget.attrs['placeholder'] = _('Titulo del manga')
        self.fields['description'].widget.attrs['placeholder'] = _('Description del manga')
        self.fields['genres'].widget.attrs = {'onchange': 'validacion()'}

    class Meta:
        """Meta clase"""
        model = Manga
        fields = ['title', 'description', 'state', 'genres']
        widgets = {'genres': forms.CheckboxSelectMultiple()}

    def clean(self):
        genres = self.cleaned_data.get('genres')
        max_genres = 7
        if genres:
            if len(genres) > max_genres:
                # Translators: Mensaje que aparece cuando
                # Translators: se intenta crear un manga con mas de un numero especifico de generos
                self.add_error('genres', _('Select maximum {} geners'.format(max_genres)))
            return self.cleaned_data

class FilterForm(forms.ModelForm):
    """Formulario para filtrar mangas"""
    class Meta:
        """Meta clase"""
        model = Manga
        fields = ['genres', 'state']
        widgets = {'genres': forms.CheckboxSelectMultiple()}

    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        self.fields['state'].required = False
        self.fields['genres'].widget.attrs = {'onchange': 'validacion()'}

    def clean(self):
        genres = self.cleaned_data.get('genres')
        max_genres = 7
        if genres:
            if len(genres) > max_genres:
                # Translators: Mensaje que aparece cuando
                # Translators: se intenta filtar con mas de un numero especifico de generos
                self.add_error('genres', _('Select maximum {} geners'.format(max_genres)))
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
        set_field_html_name(self.fields['slug'], 'search')

class ChapterRegistrationForm(forms.ModelForm):
    """Formulario para la creacion de capitulos"""
    class Meta:
        """Meta clase"""
        model = Chapter
        fields = ['content', 'user_chapter_number']

    def clean(self):
        return self.cleaned_data
