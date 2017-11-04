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
                'required': True
            }

    class Meta:
        model = Manga
        # fields = '__all__'
        fields = ['title', 'description', 'state', 'genres']
        widgets = {
            'title': forms.TextInput(
                attrs = {'placeholder': 'Titulo del manga'}
            ),
        }
        # self.fields['title'].widget.attrs = {
        #     'placeholder': 'Titulo del manga'
        # }
        # self.fields['description'].widget.attrs = {
        #     'placeholder': 'Algo aquí'
        # }
        # self.fields['state'].widget.attrs = {
        #     'placeholder': 'Algo más por aquí'
        # }

        # widgets = {
        #     'title': forms.TextInput(
        #         attrs={'id': 'manga-text', 'required': True, 'placeholder': 'Titulo del manga'}
        #     ),
        # }
    def clean(self):
        genres = self.cleaned_data.get('genres')
        max_genres = 7
        if len(genres) > max_genres:
            # Translators: Mensaje que aparece cuando se intenta crear un manga con mas de un numero especifico de generos
            self.add_error('genres', ugettext_lazy('Select maximum {} geners'.format(max_genres)))
        return self.cleaned_data

class FilterForm(forms.Form):
    class Meta:
        fields = ['genres', 'state']
    
    genres = forms.MultipleChoiceField(
        choices = Genre.GENRE_CHOICES,
        widget  = forms.CheckboxSelectMultiple,
    )
    state = forms.ChoiceField(choices = State.STATE_CHOICES,)

    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        self.fields['Genres'].widget.attrs = {
            'onchange': 'validacion()'
            }