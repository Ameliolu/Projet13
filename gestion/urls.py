from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='accueil'),
    path('legal/', views.legal, name='legal'),
    path('fil/', views.actualite, name='actualite'),
    path('contact/', views.contact, name='contact'),
]