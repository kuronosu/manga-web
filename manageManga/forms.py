from django import forms
from .models import Manga, Gender

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
        fields = ['title', 'description', 'state', 'genders']
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