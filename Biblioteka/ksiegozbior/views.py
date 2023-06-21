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
    #fields = ['użytkownik', 'książka']
    context_object_name = "wypozyczenia_list" #human-understandable name of variable to access from templates


    def get_context_data(self):
        context = super().get_context_data()
        context["wypozyczenia_list"] = models.Wypozyczenia.objects.filter(użytkownik=self.request.user)
        return context

    
    
class WypozyczenieListView(LoginRequiredMixin,  generic.CreateView):
    model = models.Wypozyczenia
    form_class = forms.WypozyczeniaForm
    success_url = reverse_lazy("ksiegozbior:lista_ksiazek")
    

    def get_form(self, form_class=None): 
        try:
            self.request.session['ksiazka_pk'] = self.request.GET['ksiazka_pk']
            print('session ',  self.request.session['ksiazka_pk'])
        except:
            pass


        if form_class is None: 
            form_class = self.get_form_class()

        form = super(WypozyczenieListView, self).get_form(form_class)
        ksiazka_do_wypozyczenia = models.Ksiazka.objects.get(pk=self.request.session['ksiazka_pk'])
        form.fields['Książka'].initial = ksiazka_do_wypozyczenia.title
        form.fields['Użytkownik'].initial = self.request.user.username
        return form
    
    def form_valid(self, form):
        WYPOZYCZONA = 'wypożyczona'
        self.object = form.save(commit=False) #wez z formularza stworzony obiekt do wypozyczenia
        ksiazka_do_wypozyczenia = models.Ksiazka.objects.get(pk=self.request.session['wypozyczenie_pk'])
        ksiazka_do_wypozyczenia.status = WYPOZYCZONA           #zmien w obiekcie Ksiazka status na  "wypozyczona" 
        ksiazka_do_wypozyczenia.save() 

        self.object.użytkownik = User.objects.get(id=self.request.user.id)
        self.object.książka = ksiazka_do_wypozyczenia
        self.object = form.save(commit=True) #zapisz wypozyczenie ksiazki w bazie
        return HttpResponseRedirect(self.get_success_url())
    

class WypozyczeniaDeleteListView(LoginRequiredMixin, generic.DeleteView):
    
    model = models.Wypozyczenia
    success_url = reverse_lazy("ksiegozbior:wypozyczenia_list")
    
    def delete(self, wypozyczenie_pk):
        WYPOZYCZONA = 'wolna'
        self.object = self.get(pk=wypozyczenie_pk)
        ksiazka_do_oddania = models.Ksiazka.objects.get(pk=self.request.session['ksiazka_pk'])
        ksiazka_do_oddania.status = WYPOZYCZONA           #zmien w obiekcie Ksiazka status na  "wypozyczona" 
        ksiazka_do_oddania.save() 
        self.object.delete()                 #usun wypozyczenie z bazy
        return HttpResponseRedirect(self.get_success_url())