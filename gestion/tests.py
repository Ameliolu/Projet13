from django.test import TestCase

from unittest.mock import patch

from .views import *
from .models import Cours, Actualite, CustomUser
from .admin import Courriels

from django.contrib.admin.sites import AdminSite
from django.contrib.admin.options import ModelAdmin
from django.db import models
# from gestion.models import MyModel
# from gestion.admin import MyModelAdmin

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
