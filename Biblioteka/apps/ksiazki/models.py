from django.contrib.auth.models import User
from django.db import models

class Ksiazka(models.Model):
        Wolna = 'Wolna'
        Wypozyczona = 'Wypozyczona'

        CHOICES_STATUS = (
            (Wolna, 'Wolna'),
            (Wypozyczona, 'Wypozyczona')  
        )

        autor = models.CharField(max_length=255)
        title = models.CharField(max_length=255)
        katalog_number = models.CharField(max_length=255)
        status = models.CharField(max_length=20, choices=CHOICES_STATUS, default=Wolna)

        def __str__(self):
            return self.title
