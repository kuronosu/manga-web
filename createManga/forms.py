from django import forms

class RegForm(forms.Form):
    name = forms.CharField(max_length = 100)
    age = forms.IntegerField()