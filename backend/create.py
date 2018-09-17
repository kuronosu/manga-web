from manageManga.models import Genre, State
from manageManga.funct import filter_obj_model
from django.http import JsonResponse
from django import forms

def create():
    
    query = filter_obj_model(Genre)
    query2 = filter_obj_model(State)
    if len(query) > 0 and len(query2) > 0:
        return JsonResponse({
            "text": "Error.",
            "code": 0
            })

    class GenreForm(forms.ModelForm):
        class Meta:
            model = Genre
            fields = ['genre']
    class StateForm(forms.ModelForm):
        class Meta:
            model = State
            fields = ['state']

    for i in Genre.GENRE_CHOICES:
        genero = GenreForm({'genre':i[0]})
        genero.save()
    for i in State.STATE_CHOICES:
        state = StateForm({'state':i[0]})
        state.save()
    return JsonResponse({
            "text": "Completado.",
            "code": 1
            })