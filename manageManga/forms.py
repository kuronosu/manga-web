from django import forms
from .models import Manga, Genre, State
from django.utils.translation import ugettext_lazy as _, ugettext_noop
from django.utils.translation import ugettext

class MangaRegistrationForm(forms.ModelForm):

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
        model = Manga
        fields = ['title', 'description', 'state', 'genres']
        widgets = {'genres': forms.CheckboxSelectMultiple()}

    def clean(self):
        genres = self.cleaned_data.get('genres')
        max_genres = 7
        if genres:
            if len(genres) > max_genres:
                # Translators: Mensaje que aparece cuando se intenta crear un manga con mas de un numero especifico de generos
                self.add_error('genres', _('Select maximum {} geners'.format(max_genres)))
            return self.cleaned_data

class FilterForm(forms.ModelForm):
    class Meta:
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
                # Translators: Mensaje que aparece cuando se intenta filtar con mas de un numero especifico de generos
                self.add_error('genres', _('Select maximum {} geners'.format(max_genres)))
            return self.cleaned_data