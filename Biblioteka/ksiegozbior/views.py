from django.views import generic
from ksiegozbior import forms
from ksiegozbior import models
from django.urls import reverse_lazy
# from django.shortcuts import redirect
from django.http import HttpResponseRedirect

from braces.views import SuperuserRequiredMixin, LoginRequiredMixin

from django.contrib.auth import get_user_model
User = get_user_model()

WYPOZYCZENIA_LIMIT = 5

class ListaKsiazekView(generic.ListView):
    model = models.Ksiazka
    context_object_name = "lista_ksiazek" #human-understandable name of variable to access from templates
    paginate_by = 10

    def get_queryset(self):
        query_result = None
        
        search_query = self.request.GET.get("search_query")
        search_type = self.request.GET.get("search_type")
        if search_query is not None:
            if search_type == "title":
                query_result = models.Ksiazka.objects.all().filter(title__icontains=search_query)
            elif search_type == "author":
                authors_result = models.Ksiazka.objects.all().filter(first_name__icontains=search_query) | models.Ksiazka.objects.all().filter(last_name__icontains=search_query)
                query_result = authors_result           
            return query_result.order_by('title')
        else:
            return models.Ksiazka.objects.all().order_by('title')
        
class DodajKsiazkeView(LoginRequiredMixin, SuperuserRequiredMixin, generic.CreateView):
    success_url = reverse_lazy("ksiegozbior:lista_ksiazek")
    form_class = forms.KsiazkaForm
    model = models.Ksiazka

    def form_valid(self, form):
        self.object = form.save(commit=True) #zapisz egzemplarz ksiazki w bazie
        return HttpResponseRedirect(self.get_success_url())

class SzczegolKsiazkiView(generic.DetailView):
    success_url = reverse_lazy("ksiegozbior:lista_ksiazek")
    model = models.Ksiazka    

class WypozyczeniaListView(LoginRequiredMixin, generic.ListView):
    model = models.Wypozyczenia
    fields = ['user_pk', 'ksiazka_pk']
    context_object_name = "wypozyczenia_list" #human-understandable name of variable to access from templates
    
    
    def get_queryset(self):
        queryset = models.Wypozyczenia.objects.filter(user=self.request.user)
        return queryset
    
    def get_context_data(self):
        context = super().get_context_data()
        context["wypozyczenia_list"] = models.Wypozyczenia.objects.filter(user=self.request.user)
        return context
    
class WypozyczenieListView(LoginRequiredMixin,  generic.CreateView):
    model = models.Wypozyczenia
    form_class = forms.WypozyczeniaForm
    success_url = reverse_lazy("ksiegozbior:lista_ksiazek")
    ilosc_wypozyczen = 0

    def get_queryset(self):
        queryset = models.Wypozyczenia.objects.filter(user=self.request.user)
        return queryset
    
    #ilosc_wypozyczen = get_queryset()
    #print('Ilosc: ' + str(ilosc_wypozyczen))

    def form_valid(self, form):
        self.object = form.save(commit=True) #zapisz egzemplarz ksiazki w bazie
        return HttpResponseRedirect(self.get_success_url())