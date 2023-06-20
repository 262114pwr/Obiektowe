from django import forms
from ksiegozbior import models
from django.contrib.auth.models import User


class KsiazkaForm(forms.ModelForm):
    class Meta:
        model = models.Ksiazka
        fields = ('first_name', 'last_name', 'title', 'description', 'catalog_number', 'status',)
    

    def __init__(self, *args, **kwargs):
        super(KsiazkaForm, self).__init__(*args, **kwargs)

class WypozyczeniaForm(forms.ModelForm):

    

        #current_user = User.username
        #self.fields['user_pk'].choice = [[1, 'current_user']]



    class Meta:
        model = models.Wypozyczenia
        fields = ('user_pk', 'ksiazka_pk',)
        
    def __init__(self, *args, **kwargs):
        super(WypozyczeniaForm, self).__init__(*args, **kwargs)  # wywolaj formularz najpierw żeby ustawić mu pola fields

