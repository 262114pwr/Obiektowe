from django.db import models
from django.urls import reverse


# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()

class Author(models.Model):
    first_name = models.CharField(max_length=200, verbose_name='Imię')
    last_name = models.CharField(max_length=200, verbose_name='Nazwisko')
    
    def __str__(self):
        return self.last_name + " " + self.first_name


class Book(models.Model):
    first_name = models.CharField(max_length=200, verbose_name='Imię')
    last_name = models.CharField(max_length=200, verbose_name='Nazwisko')
    title = models.CharField(max_length=200, verbose_name='Tytuł')
    description = models.TextField(blank=True, default='', verbose_name='Opis')
    slug = models.SlugField(allow_unicode=True, unique=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ksiegozbior:book_detail', kwargs={"pk": str(self.pk)})

     
    
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Użytkownik', related_name='user_profile')
    pesel = models.CharField(max_length=11, verbose_name='PESEL')
    street = models.CharField(max_length=200, verbose_name='Ulica')
    city = models.CharField(max_length=200, verbose_name='Miasto')
    phone = models.CharField(max_length=20, verbose_name='Telefon')
    post_code = models.CharField(max_length=6, verbose_name='Kod pocztowy')
    house_number = models.CharField(max_length=20, verbose_name='Numer domu')
    can_borrow = models.BooleanField(default=True, verbose_name='Czy może wypożyczać?')

    def __str__(self):
        return self.user.get_full_name() + ',  PESEL: ' + self.pesel
