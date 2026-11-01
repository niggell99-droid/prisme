from django.urls import path
from . import views

app_name = 'projets'

urlpatterns = [
    # URL de la liste des projets : /projets/
    path('', views.projet_list, name='projet_list'),

    # URL de soumission d'un projet : /projets/soumettre/
    path('soumettre/', views.submit_projet, name='submit'),
    
    # URL de detail du projet : /projet/mon-slug-projet/
    path('<slug:slug>/', views.projet_detail, name='projet_detail'), 
]