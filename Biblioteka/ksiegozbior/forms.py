from django import forms
from ksiegozbior import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class KsiazkaForm(forms.ModelForm):
    class Meta:
        model = models.Ksiazka
        fields = ('first_name', 'last_name', 'title', 'description', 'catalog_number', 'status',)
    

    def __init__(self, *args, **kwargs):
        super(KsiazkaForm, self).__init__(*args, **kwargs)

class WypozyczeniaForm(forms.ModelForm):

    Użytkownik = forms.CharField()
    Książka = forms.CharField()


    class Meta:
        model = models.Wypozyczenia
        fields = ('Użytkownik', 'Książka',)

    
