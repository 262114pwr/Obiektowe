
from django.urls import path
from django.contrib.auth import views as auth_views
from uzytkownicy import views

app_name = 'uzytkownicy' 

urlpatterns = [ 
    path('login/', views.CustomLoginView.as_view(template_name="uzytkownicy/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), 
    
]  

