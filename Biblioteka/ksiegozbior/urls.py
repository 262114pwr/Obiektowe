from django.urls import path
from ksiegozbior import views

app_name = 'ksiegozbior' 

urlpatterns = [
    path('lista_ksiazek/',views.ListaKsiazekView.as_view(),name='lista_ksiazek'),
    path('szczegol_ksiazki/<pk>\d+)/', views.SzczegolKsiazkiView.as_view(), name='szczegol_ksiazki'),
    path('dodaj_ksiazke/', views.DodajKsiazkeView.as_view(), name='dodaj_ksiazke'),
    path('wypozyczenia_list/', views.WypozyczeniaListView.as_view(), name='wypozyczenia_list'),
    path('wypozyczenie_create/', views.WypozyczenieListView.as_view(), name='wypozyczenie_create'),

   ]
