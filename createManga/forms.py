from django import forms
from .models import Manga

class MangaRegistrationForm(forms.ModelForm):
    class Meta:
        model = Manga
        # fields = '__all__'
        fields = ['title', 'description', 'state']
        widgets = {
            'title': forms.TextInput(
                attrs = {'class': 'form-control', 'required': True, 'placeholder': 'Titulo del manga'}
            ),
            #'author': forms.HiddenInput(attrs = {}),
        }

    def __init__(self, *args, **kwargs):
        super(MangaRegistrationForm, self).__init__(*args, **kwargs)    
        for field in self.fields:
            self.fields[field].widget.attrs = {
                'class': 'form-control', 
                'required': True
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