from django.contrib import admin
from ksiegozbior import models

#Register your models here.
class KsiazkaAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'title', 'description', 'status',)
    search_fields = ('first_name', 'last_name', 'title')
    raw_id_fields = ('first_name', 'last_name', 'title')
    

    
admin.site.register(models.Ksiazka)
admin.site.register(models.Wypozyczenia)
