from django.views import generic
from ksiegozbior import forms
from ksiegozbior import models
from django.urls import reverse_lazy
from django.shortcuts import redirect

from braces.views import SuperuserRequiredMixin, LoginRequiredMixin

from django.contrib.auth import get_user_model
User = get_user_model()

#nie dziala

class ListaKsiazekView(generic.ListView):
    model = models.Book
    context_object_name = "lista_ksiazek" 
    paginate_by = 10

    def get_queryset(self):
        query_result = None
        search_query = self.request.GET.get("search_query")
        search_type = self.request.GET.get("search_type")
        if search_query is not None:
            if search_type == "title":
                query_result = models.Book.objects.all().filter(title__icontains=search_query)
            elif search_type == "author":
                authors_result = models.Book.objects.all().filter(authors__first_name__icontains=search_query) | models.Book.objects.all().filter(authors__last_name__icontains=search_query)
                query_result = authors_result           
            return query_result.order_by('title')
        else:
            return models.Book.objects.all().order_by('title')
        
class BookDetailView(generic.DetailView):
    model = models.Book

class CreateBookView(LoginRequiredMixin, SuperuserRequiredMixin, generic.CreateView):
    login_url = reverse_lazy('no_permission')

    form_class = forms.BookForm
    model = models.Book

    def form_valid(self, form):
        self.object = form.save(commit=True) #zapisz egzemplarz ksiazki w bazie
        book_instance = self.object   #wez zapisany egzemplarz

        #dla kazdej nowo utworzonej ksiazki stworz jej egzemplarz
        models.BookCopy.objects.create(book=book_instance)
        return redirect(self.get_success_url())
    
