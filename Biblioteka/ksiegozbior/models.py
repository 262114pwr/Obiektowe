from django.db import models
from django.urls import reverse


# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()

class Ksiazka(models.Model):

    WOLNA = 'wolna'
    WYPOZYCZONA = 'wypożyczona'

    STATUS_KSIĄŻKI = (
        (WOLNA, 'Wolna'),
        (WYPOZYCZONA, 'Wypożyczona')

    )


    first_name = models.CharField(max_length=200, verbose_name='Imię Autora')
    last_name = models.CharField(max_length=200, verbose_name='Nazwisko Autora')
    title = models.CharField(max_length=200, verbose_name='Tytuł książki')
    description = models.TextField(blank=True, default='', verbose_name='Opis książki')
    status = models.CharField(max_length=20, choices=STATUS_KSIĄŻKI, default=WOLNA, verbose_name='Status książki')
    catalog_number = models.IntegerField(blank=True, default=0, verbose_name='Numer katalogowy')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ksiegozbior:lista_ksiazek', kwargs={"pk": str(self.pk)})

class Wypozyczenia(models.Model):
    user_pk = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Wypożycz dla')
    ksiazka_pk = models.ForeignKey(Ksiazka, on_delete=models.CASCADE, related_name="wypozyczona_ksiazka", verbose_name='Książka')
 
   # def __str__(self):
   #     return "user_pk=" + self.user.pk + " ksiazka_pk= " + str(self.ksiazka_id)      
    

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Użytkownik', related_name='user_profile')
   

    def __str__(self):
        return self.user.get_full_name()
