from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='Numer karty bibliotecznej',
        widget=forms.TextInput(attrs={'autofocus': True})
    )

