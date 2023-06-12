from django.urls import path
from ksiegozbior import views

app_name = 'ksiegozbior' 

urlpatterns = [
    path('lista_ksiazek/',views.ListaKsiazekView.as_view(),name='lista_ksiazek'),
    path('szczegol_ksiazki/d+)/', views.BookDetailView.as_view(), name='szczegol_ksiazki'),
    path('dodaj_ksiazke/', views.CreateBookView.as_view(), name='dodaj_ksiazke'),

   ]
