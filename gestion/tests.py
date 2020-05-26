from django.test import TestCase, RequestFactory

from unittest.mock import patch

from .views import *
from .models import Cours, Actualite, CustomUser
from .admin import *

from .forms import CourrielForm

from django.contrib.admin.sites import AdminSite
from django.contrib.admin.options import ModelAdmin
from django.db import models
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

class TestPublicView(TestCase):
    """catégorie de tests sur l'affichage des vues"""

    def test_home(self):
        """Vérification de la page d'accueil"""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'base.html', 'accueil.html')
        self.assertEqual(response.status_code, 200)

    def test_actualite(self):
        """Vérification de la page d'actualités"""
        response = self.client.get('/fil/')
        self.assertTemplateUsed(response, 'base.html', 'actualite.html')
        self.assertEqual(response.status_code, 200)

    def test_legal(self):
        """Vérification de la page des mentions légales"""
        response = self.client.get('/legal/')
        self.assertTemplateUsed(response, 'base.html', 'legal.html')
        self.assertEqual(response.status_code, 200)

    def test_contact(self):
        """Vérification de la page de contact"""
        response = self.client.get('/contact/')
        self.assertTemplateUsed(response, 'base.html', 'contact.html')
        self.assertEqual(response.status_code, 200)
        
class TestInscriptionNews(TestCase): 
    """catégorie de test sur l'inscription à la newsletter"""
    
    @classmethod
    def setUpDataTest(cls):
        CustomUser.objects.create(email="test1@mail.com")
        CustomUser.objects.create(email="test3@mail.com", newsletter="o")
    
    def test_home_inscription(self):
        """vérification de l'inscription à la newsletter si l'email n'existe pas"""
        response = self.client.post('/', {'email': 'test2@mail.com'})
        self.assertTrue(CustomUser.objects.filter(email="test2@mail.com").filter(newsletter="o").exists())

    def test_home_inscription2(self):
        """vérification de l'inscription à la newsletter si l'email existe mais pas encore inscrit"""
        response = self.client.post('/', {'email': 'test1@mail.com'})
        self.assertTrue(CustomUser.objects.filter(email="test1@mail.com").filter(newsletter="o").exists())

    def test_home_inscription3(self):
        """vérification de l'inscription à la newsletter si l'email existe et est inscrit"""
        response = self.client.post('/', {'email': 'test3@mail.com'})
        self.assertTrue(CustomUser.objects.filter(email="test3@mail.com").filter(newsletter="o").exists())
        
class MockSuperUser:
    def has_perm(self, perm):
        return True

request_factory = RequestFactory()
request = request_factory.get('/admin')
request.user = MockSuperUser()
newPhoto = SimpleUploadedFile(name='test_image.jpg', content=open("gestion/static/img/traditions.jpg", 'rb').read(), content_type='image/jpeg')

        
class TestMyAdminCours(TestCase):
    """catégorie de test sur la partie administration, model Cours"""
    
    def setUp(self):
        self.cours = Cours.objects.create(date=timezone.now(), adresse = "La rue.", texte_etudie = "Des mots.", heure="14:30:00")
        self.site = AdminSite()
        self.admin = ModelAdmin(Cours, self.site)
        
    def test_delete_Cours(self):
        obj = Cours.objects.get(pk=1)
        self.admin.delete_model(request, obj)

        deleted = Cours.objects.filter(pk=1).first()
        self.assertEqual(deleted, None)
        
    def test_fiels_Cours(self):
        ma = ModelAdmin(Cours, self.site)
        self.assertEqual(list(ma.get_form(request).base_fields), ['date', 'heure', 'adresse', 'texte_etudie'])
        self.assertEqual(list(ma.get_fields(request)), ['date', 'heure', 'adresse', 'texte_etudie'])
        self.assertEqual(list(ma.get_fields(request, self.cours)), ['date', 'heure', 'adresse', 'texte_etudie'])
    
class TestMyAdminActualite(TestCase):
    """catégorie de test sur la partie administration, model Cours"""
    
    def setUp(self):
        self.actualite = Actualite.objects.create(nom="La première", texte="Du latin", image=newPhoto, date=timezone.now())
        self.site = AdminSite()
        self.admin = ModelAdmin(Actualite, self.site)
        
    def test_delete_Actualite(self):
        obj = Actualite.objects.get(pk=1)
        self.admin.delete_model(request, obj)

        deleted = Actualite.objects.filter(pk=1).first()
        self.assertEqual(deleted, None)
        
    def test_fiels_Actualite(self):
        ma = ModelAdmin(Actualite, self.site)
        self.assertEqual(list(ma.get_form(request).base_fields), ['nom', 'texte', 'image', 'date'])
        self.assertEqual(list(ma.get_fields(request)), ['nom', 'texte', 'image', 'date'])
        self.assertEqual(list(ma.get_fields(request, self.actualite)), ['nom', 'texte', 'image', 'date'])
