from django import forms
from ksiegozbior import models
from django.contrib.auth.models import User

class BookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = ('first_name', 'last_name', 'title', 'description',)
    

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)




class AuthorForm(forms.ModelForm):
    class Meta:
        model = models.Author
        fields = ('first_name', 'last_name',)
        

